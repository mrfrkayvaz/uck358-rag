#!/usr/bin/env python3
"""
graphrag2.py — GraphRAG: SORGULAMA (Graph + Vector Hibrit Retrieval)

Bu script graphrag1.py'nin oluşturduğu bilgi grafi + embedding'leri kullanarak
soruları cevaplar. İki aşamalı retrieval yapar:

  1. Graph Traversal:  Sorgudaki entity'leri bul, grafikte dolaş, komşu entity'leri topla
  2. Vector Search:    Sorguyu embed et, entity embedding'lerde benzer ara
  3. Hibrit Skor:      İki bulguyu birleştir, en alakalı entity + chunk context'ini al
  4. LLM Cevap:        Context + soru ile LLM'den cevap üret

Kullanım:
    uv run python3 graphrag/graphrag2.py "What is longitudinal stability?"
    uv run python3 graphrag/graphrag2.py --top_k 10 "aileron roll"
    uv run python3 graphrag/graphrag2.py --interactive
    uv run python3 graphrag/graphrag2.py --llm openrouter "dihedral effect"
    uv run python3 graphrag/graphrag2.py --stats        # graph istatistikleri
"""

import argparse
import json
import logging
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("graphrag2")


# ──────────────────────────────────────────────────────────
# YAPILANDIRMA
# ──────────────────────────────────────────────────────────
@dataclass
class GraphQueryConfig:
    graph_dir: str = "graphrag/graph_store"
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_device: str = "auto"
    llm_backend: str = "ollama"                      # ollama / openrouter
    llm_model: str = "qwen3:1.7b"
    openrouter_model: str = "deepseek/deepseek-v4-flash"
    top_k_entities: int = 10                         # vektör aramasında
    top_k_relationships: int = 5                     # graf dolaşmada
    graph_walk_depth: int = 2                        # graf derinliği
    vector_weight: float = 0.4                       # hibrit skorda vector ağırlığı
    graph_weight: float = 0.6                        # hibrit skorda graph ağırlığı
    similarity_threshold: float = 0.2
    max_context_chars: int = 6000
    temperature: float = 0.7
    show_sources: bool = True


# ──────────────────────────────────────────────────────────
# GPU OTOMATİK TESPİT
# ──────────────────────────────────────────────────────────
def auto_device(prefer: str = "") -> str:
    if prefer and prefer != "auto":
        return prefer
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
    except ImportError:
        pass
    return "cpu"


# ──────────────────────────────────────────────────────────
# GRAF + EMBEDDING YÜKLEME
# ──────────────────────────────────────────────────────────
def load_graph(config: GraphQueryConfig):
    """
    Kaydedilmiş grafik, embedding ve metadata'yı yükler.
    """
    import networkx as nx
    import numpy as np

    gdir = Path(config.graph_dir)
    if not gdir.exists():
        log.error(f"❌ {config.graph_dir} bulunamadı. Önce graphrag1.py çalıştırın.")
        sys.exit(1)

    # 1. Graf
    graph_path = gdir / "graph.json"
    if not graph_path.exists():
        log.error(f"❌ {graph_path} yok.")
        sys.exit(1)
    with open(graph_path, encoding="utf-8") as f:
        graph_data = json.load(f)
    G = nx.node_link_graph(graph_data)
    log.info(f"📂 Graf yüklendi: {G.number_of_nodes()} düğüm, {G.number_of_edges()} kenar")

    # 2. Community
    comm_path = gdir / "community.json"
    communities = {}
    if comm_path.exists():
        with open(comm_path) as f:
            communities = json.load(f)
    log.info(f"📂 Community: {len(set(communities.values())) if communities else '?'} adet")

    # 3. Entity embeddings
    emb_path = gdir / "entity_embeddings.npy"
    if not emb_path.exists():
        log.error(f"❌ {emb_path} yok.")
        sys.exit(1)
    entity_embeddings = np.load(str(emb_path))
    log.info(f"📂 Embedding: {entity_embeddings.shape}")

    # 4. Entity isim listesi
    meta_path = gdir / "entity_metadata.json"
    with open(meta_path, encoding="utf-8") as f:
        entity_names = json.load(f)
    log.info(f"📂 Entity list: {len(entity_names)} adet")

    # 5. Chunk-entity map
    cem_path = gdir / "chunk_entity_map.json"
    chunk_entity_map = {}
    if cem_path.exists():
        with open(cem_path, encoding="utf-8") as f:
            chunk_entity_map = json.load(f)
    log.info(f"📂 Chunk-entity map: {len(chunk_entity_map)} chunk")

    return G, communities, entity_names, entity_embeddings, chunk_entity_map


# ──────────────────────────────────────────────────────────
# EMBEDDING
# ──────────────────────────────────────────────────────────
_embed_model = None

def get_embedding_model(model_name: str, device: str):
    global _embed_model
    if _embed_model is not None:
        return _embed_model
    from sentence_transformers import SentenceTransformer
    log.info(f"🧠 Embedding model: {model_name} ({device})")
    _embed_model = SentenceTransformer(model_name, device=device)
    return _embed_model


def embed_query(query: str, config: GraphQueryConfig):
    import numpy as np
    model = get_embedding_model(config.embedding_model, auto_device(config.embedding_device))
    emb = model.encode(query, normalize_embeddings=True)
    return emb.astype(np.float32).reshape(1, -1)


# ──────────────────────────────────────────────────────────
# 1. GRAPH TRAVERSAL
# ──────────────────────────────────────────────────────────
def graph_traversal(query_emb, entity_names, entity_embeddings, G, config: GraphQueryConfig):
    """
    Önce vektör benzerliğiyle sorguyla alakalı entity'leri bul,
    sonra grafikte dolaşarak komşu entity'leri topla.
    """
    import numpy as np
    import networkx as nx

    # Vektör araması — sorguya en yakın entity'ler
    similarities = entity_embeddings @ query_emb.T  # (N, 1)
    top_indices = np.argsort(similarities.flatten())[::-1][:config.top_k_entities]

    seed_entities = []
    for idx in top_indices:
        score = float(similarities[idx])
        if score < config.similarity_threshold:
            continue
        name = entity_names[idx]
        if name in G:
            seed_entities.append((name, score))

    if not seed_entities:
        return [], []

    log.info(f"   Seed entity: {len(seed_entities)} adet")

    # Grafik dolaşma
    visited = set()
    graph_entities = []
    for name, score in seed_entities:
        visited.add(name)
        graph_entities.append({"name": name, "score": score, "source": "vector"})

        # BFS derinlik
        for neighbor, edge_data in nx.bfs_edges(G, name, depth_limit=config.graph_walk_depth):
            if neighbor not in visited:
                visited.add(neighbor)
                decay = 0.5 ** (nx.shortest_path_length(G, name, neighbor) - 1)
                graph_entities.append({
                    "name": neighbor,
                    "score": score * decay,
                    "source": f"graph({name})",
                })

    # Skora göre sırala
    graph_entities.sort(key=lambda x: x["score"], reverse=True)
    graph_entities = graph_entities[:config.top_k_entities * 2]

    return seed_entities, graph_entities


# ──────────────────────────────────────────────────────────
# 2. HİBRİT SKOR + CONTEXT
# ──────────────────────────────────────────────────────────
def build_graph_context(
    seed_entities: list,
    graph_entities: list,
    chunk_entity_map: dict,
    G,
    config: GraphQueryConfig,
) -> str:
    """
    Graph traversal sonuçlarından zengin context oluşturur:
    - Entity descriptions
    - Community bilgisi
    - İlişkiler
    """
    import networkx as nx

    parts = []
    total_chars = 0

    # Entity descriptions
    entity_section = "### Alakalı Kavramlar\n\n"
    for ent in graph_entities[:10]:
        name = ent["name"]
        desc = G.nodes[name].get("description", "")
        freq = G.nodes[name].get("frequency", 1)
        entity_section += f"- **{name}** (frekans: {freq})"
        if desc:
            entity_section += f": {desc[:200]}"
        entity_section += f" [skor: {ent['score']:.2f}]\n"

    parts.append(entity_section)
    total_chars += len(entity_section)

    # İlişkiler
    rel_section = "\n### Alakalı İlişkiler\n\n"
    rel_count = 0
    for ent in graph_entities[:config.top_k_entities]:
        name = ent["name"]
        if name not in G:
            continue
        for neighbor in G.neighbors(name):
            edge = G[name][neighbor]
            rtype = edge.get("type", "related_to")
            descs = edge.get("descriptions", [])
            desc_str = descs[0][:150] if descs else ""
            rel_section += f"- **{name}** --[{rtype}]--> **{neighbor}**"
            if desc_str:
                rel_section += f": {desc_str}"
            rel_section += "\n"
            rel_count += 1
            if rel_count >= config.top_k_relationships:
                break
        if rel_count >= config.top_k_relationships:
            break

    if rel_count > 0:
        parts.append(rel_section)
        total_chars += len(rel_section)

    # Chunk bağlantıları (eğer chunk_entity_map varsa)
    if chunk_entity_map:
        chunk_section = "\n### İlgili Bölümler\n\n"
        chunk_refs = set()
        for ent_name, _ in seed_entities:
            for chunk_path, entities in chunk_entity_map.items():
                if ent_name in entities:
                    chunk_refs.add(chunk_path)
        for i, cp in enumerate(sorted(chunk_refs)[:5]):
            chunk_section += f"- {Path(cp).parent.name}/{Path(cp).name}\n"
        if chunk_refs:
            parts.append(chunk_section)

    context = "".join(parts)
    return context[:config.max_context_chars]


# ──────────────────────────────────────────────────────────
# 3. FULL TEXT CHUNK'LARI YÜKLE (opsiyonel)
# ──────────────────────────────────────────────────────────
def load_relevant_chunks(
    seed_entities: list,
    chunk_entity_map: dict,
    chunks_dir: str = "book/chunks",
    max_chunks: int = 3,
) -> str:
    """
    Entity'lerle ilişkili chunk'ların orijinal metinlerini yükler.
    """
    if not chunk_entity_map:
        return ""

    # Hangi chunk'lar hangi entity'leri içeriyor
    relevant_chunks = set()
    for ent_name, _ in seed_entities:
        for chunk_path, entities in chunk_entity_map.items():
            if ent_name in entities:
                relevant_chunks.add(chunk_path)

    parts = []
    count = 0
    for cp in sorted(relevant_chunks):
        if count >= max_chunks:
            break
        try:
            content = Path(cp).read_text(encoding="utf-8")
            parts.append(f"### {Path(cp).parent.name}/{Path(cp).name}\n\n{content[:2000]}")
            count += 1
        except Exception:
            continue

    return "\n\n".join(parts)


# ──────────────────────────────────────────────────────────
# 4. LLM CEVAPLAMA
# ──────────────────────────────────────────────────────────
def call_ollama(prompt: str, model: str, config: GraphQueryConfig) -> str:
    import urllib.request
    import json as _json
    payload = _json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": config.temperature,
        "options": {"num_predict": 1024},
    }).encode()
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = _json.loads(resp.read())
            return data.get("response", "").strip()
    except Exception as e:
        return f"[Ollama hatası: {e}]"


def call_openrouter(prompt: str, config: GraphQueryConfig) -> str:
    import urllib.request
    import json as _json
    api_key = None
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY"):
                    api_key = line.split("=", 1)[1].strip().strip("\"'")
                    break
    if not api_key:
        return "[HATA: OPENROUTER_API_KEY yok]"
    payload = _json.dumps({
        "model": config.openrouter_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": config.temperature,
        "max_tokens": 1024,
    }).encode()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload, headers=headers, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = _json.loads(resp.read())
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[OpenRouter hatası: {e}]"


def get_graphrag_answer(
    query: str,
    graph_context: str,
    chunk_text: str,
    config: GraphQueryConfig,
) -> str:
    """
    Graph context + chunk text + soru ile LLM'den cevap üretir.
    """
    system_prompt = (
        "You are an expert aerospace engineering tutor. "
        "Answer the question using the knowledge graph context and textbook excerpts below. "
        "Explain relationships between concepts when relevant. "
        "If the context is insufficient, say so clearly."
    )

    context = ""
    if graph_context:
        context += f"=== KNOWLEDGE GRAPH CONTEXT ===\n{graph_context}\n\n"
    if chunk_text:
        context += f"=== TEXTBOOK EXCERPTS ===\n{chunk_text}\n\n"

    full_prompt = f"{system_prompt}\n\n{context}=== QUESTION ===\n{query}\n\n=== ANSWER ==="

    model = config.llm_model if config.llm_backend == "ollama" else config.openrouter_model
    log.info(f"🤖 LLM: {config.llm_backend}/{model}")

    t0 = time.time()
    if config.llm_backend == "ollama":
        answer = call_ollama(full_prompt, config.llm_model, config)
    else:
        answer = call_openrouter(full_prompt, config)

    elapsed = time.time() - t0
    log.info(f"   Süre: {elapsed:.1f}s | Yanıt: {len(answer)} karakter")

    return answer


# ──────────────────────────────────────────────────────────
# SORGU AKIŞI
# ──────────────────────────────────────────────────────────
def answer_query(
    query: str,
    G,
    entity_names: list,
    entity_embeddings,
    chunk_entity_map: dict,
    config: GraphQueryConfig,
):
    """GraphRAG sorgu akışını çalıştırır."""
    log.info("=" * 60)
    log.info(f"❓ SORU: {query}")
    log.info("=" * 60)

    # 1. Embed query
    log.info("\n🔎 Embedding...")
    query_emb = embed_query(query, config)

    # 2. Graph traversal
    log.info("🔗 Graph traversal...")
    seed_entities, graph_entities = graph_traversal(
        query_emb, entity_names, entity_embeddings, G, config,
    )

    if not graph_entities:
        log.warning("⚠ Grafikte alakalı entity bulunamadı.")

    log.info(f"   Seed: {len(seed_entities)} | Graph toplam: {len(graph_entities)}")
    for ent in graph_entities[:5]:
        log.info(f"     {ent['name']:35s} skor={ent['score']:.3f} ({ent['source']})")

    # 3. Graph context
    log.info("\n📦 Graph context oluşturuluyor...")
    graph_context = build_graph_context(
        seed_entities, graph_entities, chunk_entity_map, G, config,
    )
    log.info(f"   Graph context: {len(graph_context)} karakter")

    # 4. Chunk text
    log.info("📄 Chunk metinleri yükleniyor...")
    chunk_text = load_relevant_chunks(seed_entities, chunk_entity_map)
    log.info(f"   Chunk text: {len(chunk_text)} karakter")

    # 5. LLM cevabı
    log.info("")
    answer = get_graphrag_answer(query, graph_context, chunk_text, config)

    # 6. Kaynaklar
    if config.show_sources:
        sources = []
        for ent in graph_entities[:5]:
            sources.append(f"🧠 {ent['name']} (skor: {ent['score']:.2f})")
        answer += f"\n\n---\n**GraphRAG Kaynaklar:**\n" + "\n".join(sources)

    return answer


# ──────────────────────────────────────────────────────────
# İSTATİSTİK
# ──────────────────────────────────────────────────────────
def show_graph_stats(G, entity_names, chunk_entity_map: dict):
    import networkx as nx
    degrees = [d for _, d in G.degree()]
    top = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:10]

    print("\n" + "=" * 60)
    print("📊 GRAPH ISTATISTIKLERI")
    print(f"   Düğüm:            {G.number_of_nodes()}")
    print(f"   Kenar:            {G.number_of_edges()}")
    print(f"   Ort. derece:      {sum(degrees)/len(degrees):.2f}" if degrees else "   Ort. derece: 0")
    print(f"   Entity embedding: {len(entity_names)}")
    print(f"   Chunk bağlantısı: {len(chunk_entity_map)} chunk")
    print(f"\n   En bağlantılı 10 entity:")
    for name, deg in top:
        desc = G.nodes[name].get("description", "")[:60]
        print(f"     {name:35s} {deg:2d} bağlantı  {desc}")
    print("=" * 60)


# ──────────────────────────────────────────────────────────
# INTERAKTİF
# ──────────────────────────────────────────────────────────
def interactive_mode(G, entity_names, entity_embeddings, chunk_entity_map, config):
    print("\n" + "=" * 60)
    print("💬 GraphRAG Sorgulama — Interaktif Mod")
    print("   'exit' çıkış, 'stats' istatistik")
    print("=" * 60)
    while True:
        try:
            q = input("\n🔍 SORU: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q:
            continue
        if q.lower() in ("exit", "quit", "q"):
            break
        if q.lower() == "stats":
            show_graph_stats(G, entity_names, chunk_entity_map)
            continue
        ans = answer_query(q, G, entity_names, entity_embeddings, chunk_entity_map, config)
        print(f"\n💡 CEVAP:\n{ans}\n")


# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="GraphRAG Sorgulama — Bilgi grafi + vektör hibrit arama"
    )
    parser.add_argument("query", nargs="?", type=str, default=None)
    parser.add_argument("--top_k", "-k", type=int, default=10)
    parser.add_argument("--depth", type=int, default=2, help="Graf dolaşma derinliği")
    parser.add_argument("--llm", choices=["ollama", "openrouter"], default="ollama")
    parser.add_argument("--interactive", "-i", action="store_true")
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--device", type=str, default="auto")
    parser.add_argument("--graph_dir", type=str, default="graphrag/graph_store")
    args = parser.parse_args()

    config = GraphQueryConfig(
        top_k_entities=args.top_k,
        graph_walk_depth=args.depth,
        llm_backend=args.llm,
        embedding_device=args.device,
        graph_dir=args.graph_dir,
    )

    # Grafik yükle
    G, communities, entity_names, entity_embeddings, chunk_entity_map = load_graph(config)

    if args.stats:
        show_graph_stats(G, entity_names, chunk_entity_map)
        return

    if args.interactive:
        interactive_mode(G, entity_names, entity_embeddings, chunk_entity_map, config)
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    answer = answer_query(
        args.query, G, entity_names, entity_embeddings, chunk_entity_map, config,
    )
    print(f"\n💡 CEVAP:\n{answer}\n")


if __name__ == "__main__":
    main()
