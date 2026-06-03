#!/usr/bin/env python3
"""
graphrag3.py — GraphRAG Pipeline ile questions/ klasöründeki soruları cevaplar.
Cevapları answers-graphrag/ klasörüne a1.md, a2.md şeklinde kaydeder.

GraphRAG: vektör araması + bilgi grafi traversal (hibrit retrieval)

Kullanım:
    uv run python3 graphrag/graphrag3.py                           # tüm sorular
    uv run python3 graphrag/graphrag3.py --limit 5                 # ilk 5 soru
    uv run python3 graphrag/graphrag3.py --depth 3                 # graf derinliği 3
    uv run python3 graphrag/graphrag3.py --llm openrouter          # OpenRouter ile
    uv run python3 graphrag/graphrag3.py --question "dihedral?"    # tek soru

Gereksinimler:
    - graphrag/graph_store/ altında bilgi grafi (graphrag1.py ile oluştur)
    - questions/ klasöründe .md dosyaları

Çıktı:
    answers-graphrag/
        a1.md       <!-- SORU: ... -->\n(cevap metni + grafik kaynakları)
        a2.md
        ...
"""

import argparse
import json
import logging
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("graphrag3")


# ──────────────────────────────────────────────────────────
# YAPILANDIRMA
# ──────────────────────────────────────────────────────────
@dataclass
class Config:
    graph_dir: Path = Path("graphrag/graph_store")
    questions_dir: Path = Path("questions")
    answers_dir: Path = Path("answers-graphrag")
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_device: str = "auto"
    llm_backend: str = "ollama"
    llm_model: str = "qwen3:1.7b"
    openrouter_model: str = "deepseek/deepseek-v4-flash"
    ollama_url: str = "http://localhost:11434"
    top_k_entities: int = 10
    graph_walk_depth: int = 2
    similarity_threshold: float = 0.2
    vector_weight: float = 0.4
    graph_weight: float = 0.6
    max_context_chars: int = 6000
    temperature: float = 0.7
    max_new_tokens: int = 1024
    show_sources: bool = True
    limit: int = 0
    single_question: Optional[str] = None


# ──────────────────────────────────────────────────────────
# GPU
# ──────────────────────────────────────────────────────────
def auto_device(prefer: str) -> str:
    if prefer != "auto":
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
def load_graph(cfg: Config):
    """Kaydedilmiş bilgi grafi + embedding + metadata yükler."""
    import networkx as nx
    import numpy as np
    from sentence_transformers import SentenceTransformer

    gdir = cfg.graph_dir
    if not gdir.exists():
        log.error(f"❌ {gdir} bulunamadı. Önce graphrag1.py çalıştırın.")
        sys.exit(1)

    # Graf
    with open(gdir / "graph.json", encoding="utf-8") as f:
        G = nx.node_link_graph(json.load(f))
    log.info(f"📂 Graf: {G.number_of_nodes()} düğüm, {G.number_of_edges()} kenar")

    # Entity embedding
    entity_embeddings = np.load(str(gdir / "entity_embeddings.npy"))
    log.info(f"📂 Embedding: {entity_embeddings.shape}")

    # Entity list
    with open(gdir / "entity_metadata.json", encoding="utf-8") as f:
        entity_names = json.load(f)
    log.info(f"📂 Entity: {len(entity_names)} adet")

    # Chunk map (opsiyonel)
    cem_path = gdir / "chunk_entity_map.json"
    chunk_entity_map = {}
    if cem_path.exists():
        with open(cem_path, encoding="utf-8") as f:
            chunk_entity_map = json.load(f)

    # Embedding model
    device = auto_device(cfg.embedding_device)
    log.info(f"🧠 Embedding: {cfg.embedding_model} ({device})")
    embed_model = SentenceTransformer(cfg.embedding_model, device=device)

    return G, entity_names, entity_embeddings, chunk_entity_map, embed_model


# ──────────────────────────────────────────────────────────
# SORU OKUMA
# ──────────────────────────────────────────────────────────
def load_questions(cfg: Config) -> list[dict]:
    if not cfg.questions_dir.exists():
        log.error(f"❌ {cfg.questions_dir}/ bulunamadı.")
        sys.exit(1)

    md_files = sorted(
        cfg.questions_dir.glob("*.md"),
        key=lambda f: int(re.search(r"(\d+)", f.stem).group(1))
        if re.search(r"(\d+)", f.stem) else 9999,
    )
    if not md_files:
        log.error(f"❌ {cfg.questions_dir}/ içinde .md yok.")
        sys.exit(1)

    qs = []
    for f in md_files:
        c = f.read_text(encoding="utf-8").strip()
        if c:
            qs.append({"index": len(qs) + 1, "filename": f.name, "content": c})

    if cfg.limit > 0:
        qs = qs[:cfg.limit]

    log.info(f"📄 {len(qs)} soru")
    for q in qs:
        log.info(f"   [{q['index']}] {q['filename']}: {q['content'][:70]}...")
    return qs


# ──────────────────────────────────────────────────────────
# GRAPH TRAVERSAL + VEKTÖR ARAMA (hibrit)
# ──────────────────────────────────────────────────────────
def graph_traversal(embed_model, query: str, entity_names, entity_embeddings, G, cfg: Config):
    """
    Sorguyu embed et → en yakın entity'ler → grafikte BFS dolaş → komşuları topla.
    
    Returns: (seed_entities, graph_entities)
    """
    import numpy as np
    import networkx as nx

    q_emb = embed_model.encode(query, normalize_embeddings=True).astype(np.float32)
    similarities = entity_embeddings @ q_emb.T

    top_idx = np.argsort(similarities.flatten())[::-1][:cfg.top_k_entities]

    # Seed entity'ler
    seed = []
    for idx in top_idx:
        s = float(similarities[idx])
        if s < cfg.similarity_threshold:
            continue
        name = entity_names[idx]
        if name in G:
            seed.append((name, s))

    if not seed:
        return [], []

    log.info(f"   🌱 Seed: {len(seed)} entity")

    # BFS traversal
    visited = set()
    graph_ents = []
    for name, score in seed:
        visited.add(name)
        graph_ents.append({"name": name, "score": score, "source": "vector"})

        for neighbor, _ in nx.bfs_edges(G, name, depth_limit=cfg.graph_walk_depth):
            if neighbor not in visited:
                visited.add(neighbor)
                dist = nx.shortest_path_length(G, name, neighbor)
                decay = 0.5 ** (dist - 1)
                graph_ents.append({"name": neighbor, "score": score * decay, "source": f"graph({name})"})

    graph_ents.sort(key=lambda x: x["score"], reverse=True)
    log.info(f"   🔗 Graph traversal: {len(graph_ents)} entity (depth={cfg.graph_walk_depth})")

    return seed, graph_ents[:cfg.top_k_entities * 2]


# ──────────────────────────────────────────────────────────
# CONTEXT
# ──────────────────────────────────────────────────────────
def build_graph_context(seed, graph_ents, G, chunk_entity_map: dict, cfg: Config) -> str:
    """Graph traversal sonucundan LLM context'i oluşturur."""
    import networkx as nx

    parts = []
    total = 0

    # Entity descriptions
    section = "### İlgili Kavramlar\n\n"
    for e in graph_ents[:10]:
        name = e["name"]
        desc = G.nodes[name].get("description", "")
        freq = G.nodes[name].get("frequency", 1)
        line = f"- **{name}** (frekans: {freq})"
        if desc:
            line += f": {desc[:150]}"
        line += f" [skor: {e['score']:.2f}]\n"
        if total + len(line) > cfg.max_context_chars // 2:
            break
        section += line
        total += len(line)
    parts.append(section)

    # Relationships
    rel_section = "\n### İlişkiler\n\n"
    count = 0
    for e in graph_ents[:cfg.top_k_entities]:
        if e["name"] not in G:
            continue
        for nb in G.neighbors(e["name"]):
            edge = G[e["name"]][nb]
            rtype = edge.get("type", "related_to")
            descs = edge.get("descriptions", [])
            line = f"- **{e['name']}** --[{rtype}]--> **{nb}**"
            if descs:
                line += f": {descs[0][:120]}"
            line += "\n"
            if total + len(line) > cfg.max_context_chars:
                break
            rel_section += line
            total += len(line)
            count += 1
            if count >= 8:
                break
        if total >= cfg.max_context_chars or count >= 8:
            break
    if count:
        parts.append(rel_section)

    # Chunk referansları
    if chunk_entity_map:
        refs = set()
        for name, _ in seed:
            for cp, ents in chunk_entity_map.items():
                if name in ents:
                    refs.add(f"- {Path(cp).parent.name}/{Path(cp).name}")
        if refs:
            parts.append("\n### İlgili Bölümler\n\n" + "\n".join(sorted(refs)[:5]))

    return "".join(parts)


# ──────────────────────────────────────────────────────────
# LLM
# ──────────────────────────────────────────────────────────
def call_ollama(prompt: str, cfg: Config) -> str:
    import urllib.request
    p = json.dumps({"model": cfg.llm_model, "prompt": prompt, "stream": False,
                     "temperature": cfg.temperature,
                     "options": {"num_predict": cfg.max_new_tokens}}).encode()
    req = urllib.request.Request(f"{cfg.ollama_url}/api/generate", data=p,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read()).get("response", "").strip()
    except Exception as e:
        return f"[Ollama hatası: {e}]"


def call_openrouter(prompt: str, cfg: Config) -> str:
    import urllib.request
    key = None
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in open(env_path):
            if line.startswith("OPENROUTER_API_KEY"):
                key = line.split("=", 1)[1].strip().strip("\"'")
    if not key:
        return "[HATA: API key yok]"
    p = json.dumps({"model": cfg.openrouter_model,
                     "messages": [{"role": "user", "content": prompt}],
                     "temperature": cfg.temperature,
                     "max_tokens": cfg.max_new_tokens}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
                                 data=p, method="POST",
                                 headers={"Authorization": f"Bearer {key}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[OpenRouter hatası: {e}]"


def get_llm_answer(graph_ctx: str, question: str, cfg: Config) -> str:
    system = ("You are an expert aerospace engineering tutor. "
              "Answer using the provided knowledge graph context. "
              "Explain relationships between concepts. "
              "Use LaTeX ($...$ or $$...$$) for equations when relevant.")

    prompt = f"{system}\n\n=== KNOWLEDGE GRAPH ===\n{graph_ctx}\n\n=== QUESTION ===\n{question}\n\n=== ANSWER ==="

    log.info(f"   🤖 LLM: {cfg.llm_backend}")
    t0 = time.time()
    answer = call_ollama(prompt, cfg) if cfg.llm_backend == "ollama" else call_openrouter(prompt, cfg)
    log.info(f"      {len(answer)} kar ({time.time() - t0:.1f}s)")
    return answer


# ──────────────────────────────────────────────────────────
# GraphRAG CEVAPLAMA (tek soru)
# ──────────────────────────────────────────────────────────
def answer_one(G, entity_names, entity_embeddings, chunk_entity_map, embed_model,
               question: str, cfg: Config) -> str:
    """GraphRAG pipeline: embed → graph traversal → context → LLM."""
    seed, graph_ents = graph_traversal(embed_model, question, entity_names, entity_embeddings, G, cfg)

    if not graph_ents:
        return "*(Bilgi grafiğinde ilgili kavram bulunamadı.)*"

    log.info(f"   📊 {len(graph_ents)} entity (seed: {len(seed)})")

    # Top 5 entity göster
    for e in graph_ents[:5]:
        log.info(f"      {e['name']:30s} skor={e['score']:.3f}")

    ctx = build_graph_context(seed, graph_ents, G, chunk_entity_map, cfg)
    answer = get_llm_answer(ctx, question, cfg)

    if cfg.show_sources and graph_ents:
        srcs = "\n".join(f"- 🧠 {e['name']} (skor: {e['score']:.2f})" for e in graph_ents[:5])
        answer += f"\n\n---\n**GraphRAG Kaynaklar:**\n{srcs}"

    return answer


# ──────────────────────────────────────────────────────────
# KAYDET
# ──────────────────────────────────────────────────────────
def save_answer(answer: str, index: int, question: str, cfg: Config) -> Path:
    cfg.answers_dir.mkdir(parents=True, exist_ok=True)
    fp = cfg.answers_dir / f"a{index}.md"
    fp.write_text(f"<!-- SORU: {question.strip()} -->\n\n{answer}\n", encoding="utf-8")
    return fp


# ──────────────────────────────────────────────────────────
# ANA
# ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="GraphRAG batch soru cevaplama")
    parser.add_argument("--limit", "-l", type=int, default=0)
    parser.add_argument("--question", "-q", type=str, default=None)
    parser.add_argument("--top_k", "-k", type=int, default=10)
    parser.add_argument("--depth", type=int, default=2, help="Graf walk depth")
    parser.add_argument("--llm", choices=["ollama", "openrouter"], default="ollama")
    parser.add_argument("--graph_dir", type=str, default="graphrag/graph_store")
    parser.add_argument("--questions_dir", type=str, default="questions")
    parser.add_argument("--answers_dir", type=str, default="answers-graphrag")
    parser.add_argument("--device", type=str, default="auto")
    parser.add_argument("--no_sources", action="store_true")
    args = parser.parse_args()

    cfg = Config(
        graph_dir=Path(args.graph_dir),
        questions_dir=Path(args.questions_dir),
        answers_dir=Path(args.answers_dir),
        llm_backend=args.llm,
        embedding_device=args.device,
        top_k_entities=args.top_k,
        graph_walk_depth=args.depth,
        show_sources=not args.no_sources,
        limit=args.limit,
        single_question=args.question,
    )

    # GraphRAG pipeline'ı yükle
    log.info("=" * 60)
    log.info("🔗 GraphRAG PIPELINE YÜKLENİYOR")
    log.info("=" * 60)
    G, entity_names, entity_embeddings, chunk_entity_map, embed_model = load_graph(cfg)

    # ── Tek soru ──
    if cfg.single_question:
        log.info(f"❓ {cfg.single_question[:80]}...")
        ans = answer_one(G, entity_names, entity_embeddings, chunk_entity_map,
                         embed_model, cfg.single_question, cfg)
        print(f"\n{'='*60}\n{ans}\n{'='*60}")
        return

    # ── Batch ──
    questions = load_questions(cfg)
    if not questions:
        sys.exit(1)

    log.info(f"\n{'='*60}")
    log.info(f"📝 GraphRAG CEVAPLAMA ({len(questions)} soru)")
    log.info(f"   LLM: {cfg.llm_backend}  |  depth: {cfg.graph_walk_depth}")
    log.info(f"   Çıktı: {cfg.answers_dir}/")
    log.info(f"{'='*60}\n")

    success = 0
    for q in questions:
        idx = q["index"]
        log.info(f"[{idx}/{len(questions)}] {q['filename']}")

        try:
            t0 = time.time()
            ans = answer_one(G, entity_names, entity_embeddings, chunk_entity_map,
                             embed_model, q["content"], cfg)
            elapsed = time.time() - t0
            fp = save_answer(ans, idx, q["content"], cfg)
            log.info(f"   ✅ {len(ans)} kar ({elapsed:.1f}s) → {fp.name}")
            success += 1
        except Exception as e:
            log.error(f"   ❌ {e}")
            save_answer(f"[HATA] {e}", idx, q["content"], cfg)

    log.info(f"\n{'='*60}")
    log.info(f"📊 {success}/{len(questions)} başarılı → {cfg.answers_dir}/")
    log.info(f"{'='*60}")


if __name__ == "__main__":
    main()
