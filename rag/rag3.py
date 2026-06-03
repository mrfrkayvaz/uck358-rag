#!/usr/bin/env python3
"""
rag3.py — RAG Pipeline ile questions/ klasöründeki soruları cevaplar.
Cevapları answers-rag/ klasörüne a1.json, a2.json şeklinde kaydeder.

Her JSON:
    - answer: cevap metni
    - source_pdf: kaynak PDF adı
    - retrieved_chunks: [{content, chapter_no, heading_no, score, path}, ...]
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
log = logging.getLogger("rag3")


# ──────────────────────────────────────────────────────────
# YAPILANDIRMA
# ──────────────────────────────────────────────────────────
@dataclass
class Config:
    index_dir: Path = Path("rag/vector_store")
    questions_dir: Path = Path("questions")
    answers_dir: Path = Path("answers-rag")
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_device: str = "auto"
    llm_backend: str = "ollama"           # ollama / openrouter
    llm_model: str = "qwen3:1.7b"
    openrouter_model: str = "deepseek/deepseek-v4-flash"
    ollama_url: str = "http://localhost:11434"
    top_k: int = 5
    similarity_threshold: float = 0.2
    max_context_chars: int = 6000
    temperature: float = 0.7
    max_new_tokens: int = 1024
    show_sources: bool = True
    limit: int = 0
    single_question: Optional[str] = None


# ──────────────────────────────────────────────────────────
# GPU TESPİT
# ──────────────────────────────────────────────────────────
def auto_device(prefer: str = "auto") -> str:
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
# INDEX + METADATA YÜKLEME
# ──────────────────────────────────────────────────────────
def load_index(cfg: Config):
    """FAISS index + metadata + embedding model yükler."""
    if not cfg.index_dir.exists():
        log.error(f"❌ Index bulunamadı: {cfg.index_dir}")
        log.error(f"   Önce 'uv run python3 rag/rag1.py' çalıştırın.")
        sys.exit(1)

    # FAISS
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer

    faiss_path = cfg.index_dir / "index.faiss"
    t0 = time.time()
    index = faiss.read_index(str(faiss_path))
    log.info(f"📂 Index: {index.ntotal} vektör, {index.d}D ({time.time() - t0:.1f}s)")

    # Metadata
    with open(cfg.index_dir / "metadata.json", encoding="utf-8") as f:
        metadata = json.load(f)
    log.info(f"📂 Metadata: {len(metadata)} chunk")

    # Embedding model
    device = auto_device(cfg.embedding_device)
    log.info(f"🧠 Embedding: {cfg.embedding_model} ({device})")
    model = SentenceTransformer(cfg.embedding_model, device=device)

    return index, metadata, model


# ──────────────────────────────────────────────────────────
# SORU OKUMA
# ──────────────────────────────────────────────────────────
def load_questions(cfg: Config) -> list[dict]:
    """questions/ içindeki .md dosyalarını okur."""
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
        content = f.read_text(encoding="utf-8").strip()
        if content:
            qs.append({"index": len(qs) + 1, "filename": f.name, "content": content})

    if cfg.limit > 0:
        qs = qs[:cfg.limit]

    log.info(f"📄 {len(qs)} soru")
    for q in qs:
        log.info(f"   [{q['index']}] {q['filename']}: {q['content'][:70]}...")
    return qs


# ──────────────────────────────────────────────────────────
# RETRIEVAL
# ──────────────────────────────────────────────────────────
def retrieve(index, metadata, embed_model, question: str, cfg: Config) -> list[dict]:
    """Sorguyu embed et, top-k chunk bul, skora göre sırala."""
    import numpy as np

    q_emb = embed_model.encode(question, normalize_embeddings=True).astype(np.float32)
    scores, indices = index.search(q_emb.reshape(1, -1), cfg.top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(metadata) or score < cfg.similarity_threshold:
            continue
        c = metadata[idx]
        results.append({
            "chapter_no": c["chapter_no"], "heading_no": c["heading_no"],
            "title": c.get("title", ""), "content": c["content"],
            "score": float(score),
        })
    results.sort(key=lambda r: r["score"], reverse=True)
    return results


# ──────────────────────────────────────────────────────────
# CONTEXT
# ──────────────────────────────────────────────────────────
def build_context(results: list[dict], cfg: Config) -> str:
    """Retrieval sonuçlarından LLM context'i oluşturur."""
    parts = []
    total = 0
    for i, r in enumerate(results, 1):
        txt = f"\n\n### [Kaynak {i}] Ch.{r['chapter_no']}/{r['heading_no']} (skor: {r['score']:.2f})\n\n{r['content']}"
        if total + len(txt) > cfg.max_context_chars:
            break
        parts.append(txt)
        total += len(txt)
    return "".join(parts)


# ──────────────────────────────────────────────────────────
# LLM CEVAPLAMA
# ──────────────────────────────────────────────────────────
def call_ollama(prompt: str, cfg: Config) -> str:
    import urllib.request
    payload = json.dumps({"model": cfg.llm_model, "prompt": prompt, "stream": False,
                           "temperature": cfg.temperature,
                           "options": {"num_predict": cfg.max_new_tokens}}).encode()
    req = urllib.request.Request(f"{cfg.ollama_url}/api/generate", data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read()).get("response", "").strip()
    except Exception as e:
        return f"[Ollama hatası: {e}]"


def call_openrouter(prompt: str, cfg: Config) -> str:
    import urllib.request
    api_key = None
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in open(env_path):
            if line.startswith("OPENROUTER_API_KEY"):
                api_key = line.split("=", 1)[1].strip().strip("\"'")
    if not api_key:
        return "[HATA: OPENROUTER_API_KEY yok]"

    payload = json.dumps({"model": cfg.openrouter_model,
                           "messages": [{"role": "user", "content": prompt}],
                           "temperature": cfg.temperature,
                           "max_tokens": cfg.max_new_tokens}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
                                 data=payload, method="POST",
                                 headers={"Authorization": f"Bearer {api_key}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read())["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[OpenRouter hatası: {e}]"


def get_llm_answer(context: str, question: str, cfg: Config) -> str:
    """RAG context + soru → LLM cevabı."""
    system = ("You are an expert aerospace engineering tutor. "
              "Answer based ONLY on the provided context. "
              "Use LaTeX ($...$ or $$...$$) for equations when relevant. "
              "If the context doesn't contain enough information, say so.")

    prompt = f"{system}\n\n=== CONTEXT ===\n{context}\n\n=== QUESTION ===\n{question}\n\n=== ANSWER ==="

    log.info(f"   🤖 LLM: {cfg.llm_backend}")
    t0 = time.time()

    if cfg.llm_backend == "ollama":
        answer = call_ollama(prompt, cfg)
    else:
        answer = call_openrouter(prompt, cfg)

    log.info(f"      {len(answer)} kar ({time.time() - t0:.1f}s)")
    return answer


# ──────────────────────────────────────────────────────────
# RAG CEVAPLAMA (tek soru)
# ──────────────────────────────────────────────────────────
def answer_one(model_or_index, metadata, embed_model, question: str, cfg: Config) -> tuple[str, dict]:
    """RAG pipeline: embed → retrieve → context → llm.
    Returns: (answer_text, result_dict_with_chunks)"""
    results = retrieve(model_or_index, metadata, embed_model, question, cfg)

    if not results:
        return "*(İlgili bir bağlam bulunamadı.)*", {"retrieved_chunks": []}

    log.info(f"   📡 {len(results)} chunk (top score: {results[0]['score']:.3f})")

    context = build_context(results, cfg)
    answer = get_llm_answer(context, question, cfg)

    # Kaynak ekle
    if cfg.show_sources and results:
        srcs = "\n".join(f"- Ch.{r['chapter_no']}/{r['heading_no']} (skor: {r['score']:.2f})" for r in results[:3])
        answer += f"\n\n---\n**Kaynaklar:**\n{srcs}"

    # Chunk verilerini derle
    meta_by_key = {(m["chapter_no"], m["heading_no"]): m for m in metadata}
    retrieved_chunks = []
    for r in results:
        key = (r["chapter_no"], r["heading_no"])
        m = meta_by_key.get(key, {})
        retrieved_chunks.append({
            "content": r["content"],
            "chapter_no": r["chapter_no"],
            "heading_no": r["heading_no"],
            "score": r["score"],
            "path": m.get("path", ""),
            "source_pdf": m.get("source_pdf", "AirplaneStabilityControl.pdf"),
        })

    result_data = {
        "answer": answer,
        "source_pdf": "AirplaneStabilityControl.pdf",
        "retrieved_chunks": retrieved_chunks,
    }

    return answer, result_data


# ──────────────────────────────────────────────────────────
# KAYDETME
# ──────────────────────────────────────────────────────────
def save_answer(result_data: dict, index: int, cfg: Config) -> Path:
    """RAG cevabını + chunk verisini .json olarak kaydeder."""
    cfg.answers_dir.mkdir(parents=True, exist_ok=True)
    fp = cfg.answers_dir / f"a{index}.json"
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    return fp


# ──────────────────────────────────────────────────────────
# ANA
# ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="RAG batch soru cevaplama")
    parser.add_argument("--limit", "-l", type=int, default=0)
    parser.add_argument("--question", "-q", type=str, default=None)
    parser.add_argument("--top_k", "-k", type=int, default=5)
    parser.add_argument("--llm", choices=["ollama", "openrouter"], default="ollama")
    parser.add_argument("--index_dir", type=str, default="rag/vector_store")
    parser.add_argument("--questions_dir", type=str, default="questions")
    parser.add_argument("--answers_dir", type=str, default="answers-rag")
    parser.add_argument("--device", type=str, default="auto")
    parser.add_argument("--no_sources", action="store_true", help="Kaynak gösterme")
    args = parser.parse_args()

    cfg = Config(
        index_dir=Path(args.index_dir),
        questions_dir=Path(args.questions_dir),
        answers_dir=Path(args.answers_dir),
        llm_backend=args.llm,
        embedding_device=args.device,
        top_k=args.top_k,
        show_sources=not args.no_sources,
        limit=args.limit,
        single_question=args.question,
    )

    # RAG pipeline'ı yükle
    log.info("=" * 60)
    log.info("🔍 RAG PIPELINE YÜKLENİYOR")
    log.info("=" * 60)
    index, metadata, embed_model = load_index(cfg)

    # ── Tek soru ──
    if cfg.single_question:
        log.info(f"❓ {cfg.single_question[:80]}...")
        ans, _ = answer_one(index, metadata, embed_model, cfg.single_question, cfg)
        print(f"\n{'='*60}\n{ans}\n{'='*60}")
        return

    # ── Batch ──
    questions = load_questions(cfg)
    if not questions:
        log.error("Hiç soru bulunamadı.")
        sys.exit(1)

    log.info(f"\n{'='*60}")
    log.info(f"📝 RAG CEVAPLAMA ({len(questions)} soru)")
    log.info(f"   LLM: {cfg.llm_backend}")
    log.info(f"   top-k: {cfg.top_k}")
    log.info(f"   Çıktı: {cfg.answers_dir}/")
    log.info(f"{'='*60}\n")

    success = 0
    for q in questions:
        idx = q["index"]
        log.info(f"[{idx}/{len(questions)}] {q['filename']}")

        try:
            t0 = time.time()
            ans, result_data = answer_one(index, metadata, embed_model, q["content"], cfg)
            elapsed = time.time() - t0
            result_data["question"] = q["content"]
            fp = save_answer(result_data, idx, cfg)
            log.info(f"   ✅ {len(ans)} karakter ({elapsed:.1f}s) → {fp.name}")
            success += 1
        except Exception as e:
            log.error(f"   ❌ {e}")
            save_answer({"question": q["content"], "answer": f"[HATA] {e}", "source_pdf": "", "retrieved_chunks": []}, idx, cfg)

    log.info(f"\n{'='*60}")
    log.info(f"📊 {success}/{len(questions)} başarılı → {cfg.answers_dir}/")
    log.info(f"{'='*60}")


if __name__ == "__main__":
    main()
