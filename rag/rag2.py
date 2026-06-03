#!/usr/bin/env python3
"""
rag2.py — Retrieval-Augmented Generation: SORGULAMA

Bu script FAISS index'ini yükler, kullanıcı sorusunu embed eder,
en alakalı chunk'ları bulur ve bir LLM ile cevap üretir.

Kullanım:
    uv run python3 rag/rag2.py "Uçağın boylamsal stabilitesi nedir?"
    uv run python3 rag/rag2.py --top_k 10 "aileron nedir?"
    uv run python3 rag/rag2.py --llm ollama "What is dihedral effect?"
    uv run python3 rag/rag2.py --llm openrouter "stability augmentation"
    uv run python3 rag/rag2.py --interactive           # interaktif mod
    uv run python3 rag/rag2.py --stats                  # index istatistikleri
    uv run python3 rag/rag2.py --device cpu "query"   # zorla CPU
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
log = logging.getLogger("rag2")


# ──────────────────────────────────────────────────────────
# YAPILANDIRMA
# ──────────────────────────────────────────────────────────
def auto_device(prefer: str = "") -> str:
    """CUDA varsa 'cuda', yoksa 'cpu' döndürür."""
    if prefer and prefer != "auto":
        return prefer
    try:
        import torch
        if torch.cuda.is_available():
            device_count = torch.cuda.device_count()
            device_name = torch.cuda.get_device_name(0)
            logging.getLogger("rag2").info(f"🎮 GPU tespit edildi: {device_name}")
            return "cuda"
    except ImportError:
        pass
    logging.getLogger("rag2").info("💻 GPU bulunamadı, CPU kullanılacak.")
    return "cpu"


@dataclass
class QueryConfig:
    index_dir: str = "rag/vector_store"
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_device: str = "auto"
    top_k: int = 5                       # kaç chunk dönsün
    similarity_threshold: float = 0.3    # minimum benzerlik skoru
    llm_backend: str = "ollama"          # "ollama" veya "openrouter"
    llm_model: str = ""                  # boş = auto
    ollama_url: str = "http://localhost:11434"
    openrouter_model: str = "deepseek/deepseek-v4-flash"
    max_context_chars: int = 8000        # maksimum context uzunluğu
    show_sources: bool = True            # kaynak göster
    temperature: float = 0.7


# ──────────────────────────────────────────────────────────
# INDEX YÜKLEME
# ──────────────────────────────────────────────────────────
def load_index(config: QueryConfig):
    """
    FAISS index + metadata + config'i yükler.
    """
    index_dir = Path(config.index_dir)
    if not index_dir.exists():
        log.error(f"❌ Index dizini bulunamadı: {index_dir}")
        log.error(f"   Önce rag1.py çalıştırın.")
        sys.exit(1)

    # FAISS index
    faiss_path = index_dir / "index.faiss"
    if not faiss_path.exists():
        log.error(f"❌ {faiss_path} bulunamadı.")
        sys.exit(1)

    import faiss
    t0 = time.time()
    index = faiss.read_index(str(faiss_path))
    log.info(f"📂 Index yüklendi: {faiss_path.name} ({index.ntotal} vektör, {index.d} dim)")
    log.info(f"   Yükleme süresi: {time.time() - t0:.2f}s")

    # Metadata
    meta_path = index_dir / "metadata.json"
    if not meta_path.exists():
        log.error(f"❌ {meta_path} bulunamadı.")
        sys.exit(1)

    with open(meta_path, encoding="utf-8") as f:
        metadata = json.load(f)
    log.info(f"📂 Metadata yüklendi: {len(metadata)} chunk")

    # Index config
    config_path = index_dir / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            index_config = json.load(f)
        log.info(f"📂 Index config: {index_config.get('embedding_model', '?')}")
        # Embedding model adını index'ten al
        if config.embedding_model == "all-MiniLM-L6-v2":
            config.embedding_model = index_config.get("embedding_model", config.embedding_model)
    else:
        log.warning("⚠ config.json bulunamadı, varsayılan embedding model kullanılacak.")

    return index, metadata


# ──────────────────────────────────────────────────────────
# EMBEDDING
# ──────────────────────────────────────────────────────────
_embedding_model_cache = None

def get_embedding_model(model_name: str, device: str):
    """sentence-transformers modelini singleton olarak yükler."""
    global _embedding_model_cache
    if _embedding_model_cache is not None:
        return _embedding_model_cache

    log.info(f"🧠 Embedding model yükleniyor: {model_name}")
    from sentence_transformers import SentenceTransformer
    _embedding_model_cache = SentenceTransformer(model_name, device=device)
    return _embedding_model_cache


def embed_query(query: str, config: QueryConfig):
    """Sorguyu embed eder ve normalleştirir."""
    import numpy as np
    model = get_embedding_model(config.embedding_model, config.embedding_device)
    emb = model.encode(query, normalize_embeddings=True)
    return emb.astype(np.float32).reshape(1, -1)


# ──────────────────────────────────────────────────────────
# RETRIEVAL
# ──────────────────────────────────────────────────────────
def retrieve(index, metadata: list[dict], query_emb, config: QueryConfig) -> list[dict]:
    """
    FAISS index'te arama yapar ve en alakalı chunk'ları döndürür.
    """
    import numpy as np

    # FAISS araması
    scores, indices = index.search(query_emb, config.top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0 or idx >= len(metadata):
            continue
        if score < config.similarity_threshold:
            continue

        chunk = metadata[idx]
        results.append({
            "chapter_no": chunk["chapter_no"],
            "heading_no": chunk["heading_no"],
            "title": chunk.get("title", ""),
            "content": chunk["content"],
            "score": float(score),
            "path": chunk.get("path", ""),
        })

    # Skora göre sırala (yüksekten düşüğe)
    results.sort(key=lambda r: r["score"], reverse=True)

    return results


# ──────────────────────────────────────────────────────────
# CONTEXT OLUŞTURMA
# ──────────────────────────────────────────────────────────
def build_context(results: list[dict], config: QueryConfig) -> str:
    """
    Retrieval sonuçlarından context metni oluşturur.
    """
    parts = []
    total_chars = 0

    for i, r in enumerate(results, 1):
        header = f"[Kaynak {i}] — Chapter {r['chapter_no']}, Bölüm {r['heading_no']}"
        if r["title"]:
            header += f" — {r['title']}"

        # İçerikten başlık satırlarını temizle (context'i temiz tut)
        content = r["content"]

        # Context sınırını kontrol et
        entry = f"\n\n### {header}\n\n{content}"
        if total_chars + len(entry) > config.max_context_chars:
            # Sığdığı kadar al
            remaining = config.max_context_chars - total_chars
            if remaining > 200:
                entry = f"\n\n### {header}\n\n{content[:remaining]}..."
                parts.append(entry)
            break

        parts.append(entry)
        total_chars += len(entry)

    context = "".join(parts)
    return context


# ──────────────────────────────────────────────────────────
# LLM CEVAPLAMA
# ──────────────────────────────────────────────────────────
def call_ollama(prompt: str, model: str, config: QueryConfig) -> str:
    """Ollama ile cevap üret."""
    import urllib.request
    import urllib.error

    url = f"{config.ollama_url}/api/generate"
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": config.temperature,
        "options": {
            "num_predict": 1024,
        }
    }).encode()

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data.get("response", "").strip()
    except urllib.error.HTTPError as e:
        return f"[Ollama Hatası {e.code}: {e.reason}]"
    except urllib.error.URLError as e:
        return f"[Ollama bağlantı hatası: {e.reason}]"


def call_openrouter(prompt: str, config: QueryConfig) -> str:
    """OpenRouter ile cevap üret."""
    import urllib.request
    import urllib.error

    # .env'den API key
    api_key = None
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY"):
                    api_key = line.split("=", 1)[1].strip().strip("\"'")
                    break

    if not api_key:
        return "[HATA: OPENROUTER_API_KEY .env'de bulunamadı]"

    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = json.dumps({
        "model": config.openrouter_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": config.temperature,
        "max_tokens": 1024,
    }).encode()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[OpenRouter Hatası: {e}]"


def get_llm_answer(context: str, question: str, config: QueryConfig) -> str:
    """
    Context + soru ile LLM'den cevap üretir.
    """
    # LLM model adını belirle
    if config.llm_backend == "ollama":
        model = config.llm_model or "qwen3:1.7b"
    else:
        model = config.openrouter_model

    log.info(f"🤖 LLM: {config.llm_backend}/{model}")

    # Prompt
    system_prompt = (
        "You are an expert aerospace engineering tutor. "
        "Answer the question based ONLY on the provided context. "
        "If the context doesn't contain enough information, say so. "
        "Use precise technical language. Include specific details from the context."
    )

    full_prompt = f"""{system_prompt}

=== CONTEXT ===
{context}

=== QUESTION ===
{question}

=== ANSWER ===
"""

    log.info(f"⏳ Cevap üretiliyor...")

    t0 = time.time()
    if config.llm_backend == "ollama":
        answer = call_ollama(full_prompt, model, config)
    elif config.llm_backend == "openrouter":
        answer = call_openrouter(full_prompt, config)
    else:
        answer = f"[Bilinmeyen LLM backend: {config.llm_backend}]"

    elapsed = time.time() - t0
    log.info(f"   Süre: {elapsed:.1f}s | Uzunluk: {len(answer)} karakter")

    return answer


# ──────────────────────────────────────────────────────────
# SORGUYU CEVAPLA (tüm akış)
# ──────────────────────────────────────────────────────────
def answer_question(question: str, index, metadata: list[dict], config: QueryConfig):
    """
    Soruyu cevaplamak için tüm RAG akışını çalıştırır.
    """
    log.info("=" * 60)
    log.info(f"❓ SORU: {question}")
    log.info("=" * 60)

    # 1. Sorguyu embed et
    log.info("\n🔎 Embedding hesaplanıyor...")
    query_emb = embed_query(question, config)

    # 2. Retrieval
    log.info(f"📡 Retrieval (top-{config.top_k})...")
    results = retrieve(index, metadata, query_emb, config)

    if not results:
        log.warning("⚠ Hiçbir chunk yeterli benzerlikte bulunamadı.")
        return "Üzgünüm, bu soruyla ilgili bir bilgi bulamadım."

    log.info(f"   En yüksek skor: {results[0]['score']:.4f}")
    log.info(f"   En düşük skor:  {results[-1]['score']:.4f}")
    log.info(f"   Kaynaklar:")
    for r in results:
        title_part = f" — {r['title']}" if r['title'] else ""
        log.info(f"     Ch.{r['chapter_no']} {r['heading_no']}{title_part} (skor: {r['score']:.3f})")

    # 3. Context oluştur
    log.info("\n📦 Context oluşturuluyor...")
    context = build_context(results, config)
    log.info(f"   Context: {len(context):,} karakter, {len(results)} kaynak")

    # 4. LLM cevabı
    log.info("")
    answer = get_llm_answer(context, question, config)

    # 5. Kaynakları ekle
    if config.show_sources and results:
        sources = []
        for r in results:
            sources.append(f"📖 Ch.{r['chapter_no']} / {r['heading_no']} (skor: {r['score']:.2f})")
        answer += f"\n\n---\n**Kaynaklar:**\n" + "\n".join(sources)

    return answer


# ──────────────────────────────────────────────────────────
# INDEX İSTATİSTİKLERİ
# ──────────────────────────────────────────────────────────
def show_stats(metadata: list[dict], index):
    """Index hakkında detaylı istatistik gösterir."""
    chapter_counts = {}
    total_chars = 0

    for c in metadata:
        ch = c["chapter_no"]
        chapter_counts[ch] = chapter_counts.get(ch, 0) + 1
        total_chars += c.get("char_count", len(c["content"]))

    print("\n" + "=" * 60)
    print("📊 INDEX İSTATİSTİKLERİ")
    print(f"   Toplam chunk:        {len(metadata)}")
    print(f"   Embedding boyutu:    {index.d}")
    print(f"   Toplam karakter:     {total_chars:,}")
    print(f"   Ortalama chunk:      {total_chars // max(len(metadata), 1):,} karakter")
    print(f"   Chapter sayısı:      {len(chapter_counts)}")
    print()
    print("   Chapter dağılımı:")
    max_count = max(chapter_counts.values()) if chapter_counts else 1
    for ch in sorted(chapter_counts.keys()):
        cnt = chapter_counts[ch]
        bar = "█" * max(1, int(cnt / max_count * 30))
        print(f"     Chapter {ch:2d}: {cnt:3d} chunk  {bar}")
    print("=" * 60)


# ──────────────────────────────────────────────────────────
# INTERAKTİF MOD
# ──────────────────────────────────────────────────────────
def interactive_mode(index, metadata: list[dict], config: QueryConfig):
    """Kullanıcıyla etkileşimli Q&A oturumu."""
    print("\n" + "=" * 60)
    print("💬 RAG Sorgulama — Interaktif Mod")
    print("   'exit' veya 'quit' yazarak çıkabilirsiniz.")
    print("   'stats' yazarak index istatistiklerini görebilirsiniz.")
    print("=" * 60)

    while True:
        try:
            question = input("\n🔍 Soru: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGörüşmek üzere!")
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit", "q"):
            print("Görüşmek üzere!")
            break
        if question.lower() == "stats":
            show_stats(metadata, index)
            continue

        answer = answer_question(question, index, metadata, config)
        print(f"\n💡 CEVAP:\n{answer}\n")


# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="RAG Sorgulama — FAISS index'inde arama yapıp LLM ile cevaplar."
    )
    parser.add_argument("query", nargs="?", type=str, default=None,
                        help="Sorgu metni")
    parser.add_argument("--device", type=str, default="auto",
                        help="cuda / cpu / auto (varsayılan: auto — GPU varsa cuda)")
    parser.add_argument("--top_k", "-k", type=int, default=5,
                        help="Getirilecek chunk sayısı (varsayılan: 5)")
    parser.add_argument("--threshold", "-t", type=float, default=0.3,
                        help="Minimum benzerlik eşiği (varsayılan: 0.3)")
    parser.add_argument("--llm", choices=["ollama", "openrouter"], default="ollama",
                        help="LLM backend (varsayılan: ollama)")
    parser.add_argument("--llm_model", type=str, default="",
                        help="LLM model adı (örn: qwen3:1.7b, deepseek/deepseek-v4-flash)")
    parser.add_argument("--no_sources", action="store_true",
                        help="Kaynak referanslarını gizle")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Interaktif mod")
    parser.add_argument("--stats", action="store_true",
                        help="Index istatistiklerini göster")
    parser.add_argument("--index_dir", type=str, default="rag/vector_store",
                        help="Index dizini (varsayılan: rag/vector_store)")
    args = parser.parse_args()

    # GPU otomatik tespit
    device = auto_device(args.device)
    log.info(f"🔧 Embedding cihazı: {device}")

    config = QueryConfig(
        top_k=args.top_k,
        similarity_threshold=args.threshold,
        llm_backend=args.llm,
        llm_model=args.llm_model,
        show_sources=not args.no_sources,
        index_dir=args.index_dir,
        embedding_device=device,
    )

    # OpenRouter model adını güncelle
    if args.llm_model:
        if args.llm == "openrouter":
            config.openrouter_model = args.llm_model

    # Index yükle
    index, metadata = load_index(config)

    # Stats modu
    if args.stats:
        show_stats(metadata, index)
        return

    # Interaktif mod
    if args.interactive:
        interactive_mode(index, metadata, config)
        return

    # Tek sorgu modu
    if not args.query:
        parser.print_help()
        print("\nHATA: Sorgu metni girin veya --interactive kullanın.")
        sys.exit(1)

    answer = answer_question(args.query, index, metadata, config)
    print(f"\n💡 CEVAP:\n{answer}\n")


if __name__ == "__main__":
    main()
