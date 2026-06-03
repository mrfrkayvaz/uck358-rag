#!/usr/bin/env python3
"""
graphrag1.py — GraphRAG: BİLGİ GRAFI OLUŞTURMA

Bu script book/chunks/ içindeki .md dosyalarından entity'ler ve ilişkiler
çıkararak bir bilgi grafi (knowledge graph) oluşturur. Grafik + embedding'ler
birlikte kaydedilir, böylece graphrag2.py hibrit (graph + vector) sorgulama yapabilir.

Kullanım:
    uv run python3 graphrag/graphrag1.py                                   # tüm chunks
    uv run python3 graphrag/graphrag1.py --limit 5                         # ilk 5 chunk
    uv run python3 graphrag/graphrag1.py --force                           # varsa sil yeniden yap
    uv run python3 graphrag/graphrag1.py --llm openrouter                  # API ile extraction

Çıktı:
    graphrag/graph_store/
        graph.json               # NetworkX grafi (entity + relationship)
        community.json           # Community (topluluk) bilgileri
        entity_embeddings.npy    # Entity embedding vektörleri
        entity_metadata.json     # Entity isim-listesi
        chunk_entity_map.json    # Hangi chunk hangi entity'leri içeriyor
"""

import argparse
import json
import logging
import re
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("graphrag1")


# ──────────────────────────────────────────────────────────
# YAPILANDIRMA
# ──────────────────────────────────────────────────────────
@dataclass
class GraphConfig:
    chunks_dir: str = "book/chunks"
    output_dir: str = "graphrag/graph_store"
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_device: str = "auto"
    llm_backend: str = "ollama"            # ollama / openrouter
    llm_model: str = "qwen3:1.7b"          # entity extraction için
    openrouter_model: str = "deepseek/deepseek-v4-flash"
    batch_size: int = 8                    # extraction batch
    force_rebuild: bool = False
    limit_chunks: int = 0                  # 0 = tümü
    min_entity_freq: int = 1               # en az 1 chunk'ta geçen entity'ler


# ──────────────────────────────────────────────────────────
# GPU OTOMATİK TESPİT
# ──────────────────────────────────────────────────────────
def auto_device(prefer: str = "") -> str:
    if prefer and prefer != "auto":
        return prefer
    try:
        import torch
        if torch.cuda.is_available():
            log.info(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
            return "cuda"
    except ImportError:
        pass
    log.info("💻 GPU yok, CPU kullanılıyor.")
    return "cpu"


# ──────────────────────────────────────────────────────────
# CHUNK TARAMA
# ──────────────────────────────────────────────────────────
def scan_chunks(chunks_dir: str, limit: int = 0) -> list[dict]:
    """book/chunks/ içindeki .md dosyalarını tara, metadata çıkar."""
    base = Path(chunks_dir)
    if not base.exists():
        log.error(f"❌ {chunks_dir} bulunamadı.")
        sys.exit(1)

    chapter_dirs = sorted(
        [d for d in base.iterdir() if d.is_dir() and d.name.isdigit()],
        key=lambda p: int(p.name),
    )

    if not chapter_dirs:
        log.error(f"❌ {chunks_dir}/ içinde chapter klasörü yok.")
        sys.exit(1)

    chunks = []
    for ch_dir in chapter_dirs:
        chapter_no = int(ch_dir.name)
        for md_file in sorted(ch_dir.glob("*.md")):
            stem = md_file.stem
            if stem == f"{chapter_no}-intro":
                heading_no = f"{chapter_no}.0"
            else:
                m = re.match(rf"{chapter_no}-(\d+)", stem)
                if m:
                    heading_no = f"{chapter_no}.{m.group(1)}"
                else:
                    continue

            content = md_file.read_text(encoding="utf-8").strip()
            if not content:
                continue

            # İlk başlık
            title = ""
            for line in content.split("\n"):
                s = line.strip()
                if s.startswith("#"):
                    title = s.lstrip("#").strip()
                    break

            chunks.append({
                "path": str(md_file),
                "chapter_no": chapter_no,
                "heading_no": heading_no,
                "title": title,
                "content": content,
            })

    if limit > 0:
        chunks = chunks[:limit]
        log.info(f"📄 Limit: {limit} chunk (toplam {len(chunks)})")
    else:
        log.info(f"📄 Toplam chunk: {len(chunks)}")

    return chunks


# ──────────────────────────────────────────────────────────
# ENTITY & RELATIONSHIP EXTRACTION (LLM ile)
# ──────────────────────────────────────────────────────────
EXTRACTION_PROMPT = """Analyze the following text from an aerospace engineering textbook about airplane stability and control.

Extract key entities (concepts, terms, people, theories, components) and their relationships.

Return ONLY valid JSON in this exact format:
{{
  "entities": [
    {{"name": "...", "type": "concept|term|person|component|theory", "description": "..."}}
  ],
  "relationships": [
    {{"source": "entity1", "target": "entity2", "type": "is_a|has_property|influences|part_of|developed_by|related_to", "description": "..."}}
  ]
}}

Text:
{content}"""


def call_ollama(prompt: str, model: str) -> Optional[str]:
    """Ollama ile metin üret."""
    import urllib.request
    import urllib.error
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.3,
        "options": {"num_predict": 2048}
    }).encode()
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data.get("response", "")
    except Exception as e:
        log.warning(f"Ollama hatası: {e}")
        return None


def call_openrouter(prompt: str, model: str) -> Optional[str]:
    """OpenRouter ile metin üret."""
    import urllib.request
    api_key = None
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY"):
                    api_key = line.split("=", 1)[1].strip().strip("\"'")
                    break
    if not api_key:
        log.error("OPENROUTER_API_KEY .env'de bulunamadı")
        return None

    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 2048,
    }).encode()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload, headers=headers, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        log.warning(f"OpenRouter hatası: {e}")
        return None


def extract_entities(content: str, config: GraphConfig) -> dict:
    """
    Bir chunk metninden entity + relationship çıkarır.
    Dönen: {"entities": [...], "relationships": [...]}
    """
    prompt = EXTRACTION_PROMPT.format(content=content[:6000])  # max 6K karakter

    if config.llm_backend == "ollama":
        response = call_ollama(prompt, config.llm_model)
    else:
        response = call_openrouter(prompt, config.openrouter_model)

    if not response:
        return {"entities": [], "relationships": []}

    # JSON parse
    json_match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
    text = json_match.group(1) if json_match else response
    text = text.strip()
    # JSON olmayan kısımları temizle
    brace_start = text.find("{")
    brace_end = text.rfind("}")
    if brace_start >= 0 and brace_end > brace_start:
        text = text[brace_start:brace_end + 1]

    try:
        data = json.loads(text)
        entities = data.get("entities", [])
        relationships = data.get("relationships", [])
        return {
            "entities": entities[:20],       # chunk başına max 20 entity
            "relationships": relationships[:20],
        }
    except (json.JSONDecodeError, KeyError) as e:
        log.warning(f"⚠ JSON parse hatası: {e}")
        return {"entities": [], "relationships": []}


def extract_all_entities(chunks: list[dict], config: GraphConfig) -> tuple[list, list, dict]:
    """
    Tüm chunk'lardan entity + relationship çıkarır.
    """
    all_entities = []       # (chunk_idx, entity_dict)
    all_relationships = []  # (chunk_idx, rel_dict)
    chunk_entity_map = defaultdict(list)  # chunk_path -> [entity_name, ...]

    log.info(f"🤖 Entity extraction başlıyor (backend: {config.llm_backend})...")

    for i, chunk in enumerate(chunks):
        chunk_path = chunk["path"]
        content = chunk["content"]

        log.info(f"   [{i+1}/{len(chunks)}] {Path(chunk_path).name} "
                 f"({len(content)} karakter)...")

        result = extract_entities(content, config)

        for ent in result["entities"]:
            name = ent.get("name", "").strip()
            if name:
                all_entities.append((i, ent))
                chunk_entity_map[chunk_path].append(name)

        for rel in result["relationships"]:
            src = rel.get("source", "").strip()
            tgt = rel.get("target", "").strip()
            if src and tgt:
                all_relationships.append((i, rel))

        log.info(f"      → {len(result['entities'])} entity, {len(result['relationships'])} ilişki")

        # Rate limiting
        if i < len(chunks) - 1:
            time.sleep(1.5)

    log.info(f"\n📊 Extraction özeti:")
    log.info(f"   Toplam entity:        {len(all_entities)}")
    log.info(f"   Toplam relationship:  {len(all_relationships)}")
    log.info(f"   Chunk-entity bağlantı: {len(chunk_entity_map)} chunk")

    return all_entities, all_relationships, dict(chunk_entity_map)


# ──────────────────────────────────────────────────────────
# GRAF İNŞAASI (NetworkX)
# ──────────────────────────────────────────────────────────
def build_knowledge_graph(
    all_entities: list,
    all_relationships: list,
    chunks: list[dict],
    chunk_entity_map: dict,
    config: GraphConfig,
):
    """
    Entity'lerden ve ilişkilerden NetworkX grafi oluşturur.
    Community detection + embedding ekler.
    """
    import networkx as nx
    import numpy as np
    from sentence_transformers import SentenceTransformer

    G = nx.Graph()
    log.info("\n🔗 Graf inşa ediliyor...")

    # ── Entity'leri ekle ──
    entity_metadata = {}  # name -> description, type, freq
    entity_counter = defaultdict(int)

    for chunk_idx, ent in all_entities:
        name = ent["name"].strip()
        if not name:
            continue
        entity_counter[name] += 1
        if name not in entity_metadata:
            entity_metadata[name] = {
                "name": name,
                "type": ent.get("type", "concept"),
                "description": ent.get("description", ""),
            }

    # Sık geçen entity'leri filtrele
    for name, freq in entity_counter.items():
        if freq >= config.min_entity_freq:
            G.add_node(name, **entity_metadata.get(name, {}))
            G.nodes[name]["frequency"] = freq

    log.info(f"   Düğüm (node): {G.number_of_nodes()}")

    # ── İlişkileri ekle ──
    edge_count = 0
    for chunk_idx, rel in all_relationships:
        src = rel.get("source", "").strip()
        tgt = rel.get("target", "").strip()
        rtype = rel.get("type", "related_to")
        desc = rel.get("description", "")

        if src in G and tgt in G:
            if G.has_edge(src, tgt):
                G[src][tgt]["weight"] = G[src][tgt].get("weight", 1) + 1
                if desc and desc not in G[src][tgt].get("descriptions", []):
                    G[src][tgt]["descriptions"] = G[src][tgt].get("descriptions", []) + [desc]
            else:
                G.add_edge(src, tgt, weight=1, type=rtype, descriptions=[desc] if desc else [])
                edge_count += 1

    log.info(f"   Kenar (edge): {G.number_of_edges()}")

    # ── Community detection ──
    communities = detect_communities(G)
    log.info(f"   Community: {len(set(communities.values()))} adet")

    # ── Entity embedding ──
    device = auto_device(config.embedding_device)
    log.info(f"🧠 Entity embedding: {config.embedding_model} ({device})")
    model = SentenceTransformer(config.embedding_model, device=device)

    entity_names = list(G.nodes())
    entity_descriptions = [
        f"{n}: {G.nodes[n].get('description', '')}" for n in entity_names
    ]

    entity_embeddings = model.encode(
        entity_descriptions,
        batch_size=config.batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    log.info(f"   Embedding boyutu: {entity_embeddings.shape}")

    # ── Chunk-entity adjacency ──
    # chunk_entity_map zaten hazır

    return G, communities, entity_names, entity_embeddings, chunk_entity_map


def detect_communities(G) -> dict:
    """
    Grafikte community detection (Leiden algoritması).
    Döner: {node_name: community_id}
    """
    try:
        from networkx.algorithms.community import leiden_communities
        communities = leiden_communities(G)
        community_map = {}
        for cid, members in enumerate(communities):
            for node in members:
                community_map[node] = cid
        return community_map
    except ImportError:
        log.warning("⚠ leiden_communities yok, greedy_modularity kullanılıyor.")
        from networkx.algorithms.community import greedy_modularity_communities
        communities = greedy_modularity_communities(G)
        community_map = {}
        for cid, members in enumerate(communities):
            for node in members:
                community_map[node] = cid
        return community_map


# ──────────────────────────────────────────────────────────
# KAYDETME
# ──────────────────────────────────────────────────────────
def save_graph(
    G,
    communities: dict,
    entity_names: list,
    entity_embeddings,
    chunk_entity_map: dict,
    config: GraphConfig,
):
    """
    Grafik + embedding'leri dosyaya kaydeder.
    """
    import networkx as nx
    import numpy as np

    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. NetworkX grafi (JSON serileştirme)
    graph_path = output_dir / "graph.json"
    graph_data = nx.node_link_data(G)
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    log.info(f"💾 Graf: {graph_path} ({graph_path.stat().st_size / 1024:.0f} KB)")

    # 2. Community bilgisi
    comm_path = output_dir / "community.json"
    with open(comm_path, "w") as f:
        json.dump(communities, f, indent=2)
    log.info(f"💾 Community: {comm_path}")

    # 3. Entity embedding (numpy .npy)
    emb_path = output_dir / "entity_embeddings.npy"
    np.save(str(emb_path), entity_embeddings)
    log.info(f"💾 Embedding: {emb_path} ({entity_embeddings.shape})")

    # 4. Entity isim listesi (sıralı)
    meta_path = output_dir / "entity_metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(entity_names, f, ensure_ascii=False, indent=2)
    log.info(f"💾 Entity list: {meta_path}")

    # 5. Chunk-entity haritası
    cem_path = output_dir / "chunk_entity_map.json"
    with open(cem_path, "w", encoding="utf-8") as f:
        json.dump(chunk_entity_map, f, ensure_ascii=False, indent=2)
    log.info(f"💾 Chunk-entity map: {cem_path}")

    # 6. Config
    cfg_path = output_dir / "config.json"
    with open(cfg_path, "w") as f:
        json.dump({
            "embedding_model": config.embedding_model,
            "llm_backend": config.llm_backend,
            "num_nodes": G.number_of_nodes(),
            "num_edges": G.number_of_edges(),
            "num_communities": len(set(communities.values())),
            "embedding_dim": entity_embeddings.shape[1],
        }, f, indent=2)
    log.info(f"💾 Config: {cfg_path}")


# ──────────────────────────────────────────────────────────
# ÖZET
# ──────────────────────────────────────────────────────────
def print_summary(G, communities: dict, chunks: list):
    """Grafik hakkında özet."""
    import networkx as nx

    degrees = [d for _, d in G.degree()]
    avg_degree = sum(degrees) / len(degrees) if degrees else 0
    community_ids = set(communities.values())

    log.info("\n" + "=" * 60)
    log.info("📊 GRAFİK ÖZETİ")
    log.info(f"   Düğüm (entity):       {G.number_of_nodes()}")
    log.info(f"   Kenar (ilişki):       {G.number_of_edges()}")
    log.info(f"   Ortalama derece:      {avg_degree:.2f}")
    log.info(f"   Community sayısı:     {len(community_ids)}")
    log.info(f"   İşlenen chunk:        {len(chunks)}")

    # En bağlantılı 5 entity
    top_entities = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:5]
    log.info(f"   En bağlantılı entity'ler:")
    for name, deg in top_entities:
        log.info(f"      {name:40s} ({deg} bağlantı)")
    log.info("=" * 60)


# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="GraphRAG — Bilgi Grafi Oluşturma"
    )
    parser.add_argument("--limit", "-l", type=int, default=0,
                        help="İşlenecek maksimum chunk (0=tümü)")
    parser.add_argument("--force", "-f", action="store_true",
                        help="Varolan graph'ı sil yeniden yap")
    parser.add_argument("--llm", choices=["ollama", "openrouter"], default="ollama",
                        help="Entity extraction için LLM backend")
    parser.add_argument("--device", type=str, default="auto",
                        help="cuda / cpu / auto")
    parser.add_argument("--output_dir", type=str, default="graphrag/graph_store")
    args = parser.parse_args()

    config = GraphConfig(
        llm_backend=args.llm,
        embedding_device=args.device,
        limit_chunks=args.limit,
        force_rebuild=args.force,
        output_dir=args.output_dir,
    )

    if config.force_rebuild:
        import shutil
        out = Path(config.output_dir)
        if out.exists():
            shutil.rmtree(out)
            log.info(f"🗑️  Eski graph silindi: {out}")

    # 1. Chunk'ları tara
    log.info("=" * 60)
    log.info("🔍 CHUNK TARANIYOR")
    chunks = scan_chunks(config.chunks_dir, config.limit_chunks)

    # 2. Entity + Relationship extraction
    log.info("")
    all_entities, all_relationships, chunk_entity_map = extract_all_entities(chunks, config)

    if not all_entities:
        log.warning("⚠ Hiç entity çıkarılamadı. LLM bağlantısını kontrol edin.")
        sys.exit(1)

    # 3. Graf inşaası
    log.info("")
    G, communities, entity_names, entity_embeddings, chunk_entity_map = build_knowledge_graph(
        all_entities, all_relationships, chunks, chunk_entity_map, config,
    )

    # 4. Kaydet
    log.info("")
    save_graph(G, communities, entity_names, entity_embeddings, chunk_entity_map, config)

    # 5. Özet
    print_summary(G, communities, chunks)

    log.info("\n✅ GraphRAG — Graph oluşturma tamamlandı!")


if __name__ == "__main__":
    main()
