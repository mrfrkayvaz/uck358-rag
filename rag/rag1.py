#!/usr/bin/env python3
"""
rag1.py — Retrieval-Augmented Generation: INDEX OLUŞTURMA

Bu script book/chunks/ içindeki tüm .md dosyalarını tarar, 
embedding vektörlerine çevirir ve bir FAISS index'ine kaydeder.

Kullanım:
    uv run python3 rag/rag1.py                                   # GPU varsa otomatik kullanır
    uv run python3 rag/rag1.py --embedding_model all-MiniLM-L6-v2
    uv run python3 rag/rag1.py --force                           # varsa sil yeniden yap
    uv run python3 rag/rag1.py --device cpu                      # zorla CPU

Çıktı:
    rag/vector_store/
        index.faiss          # FAISS binary index
        metadata.json        # chunk metinleri + chapter/heading bilgisi
        config.json          # embedding model adı vb.
"""

import argparse
import json
import logging
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("rag1")


# ──────────────────────────────────────────────────────────
# YAPILANDIRMA
# ──────────────────────────────────────────────────────────
@dataclass
class IndexConfig:
    chunks_dir: str = "book/chunks"
    output_dir: str = "rag/vector_store"
    embedding_model: str = "all-MiniLM-L6-v2"  # sentence-transformers modeli
    embedding_device: str = "auto"             # auto / cuda / cpu
    batch_size: int = 32                       # embedding batch boyutu
    force_rebuild: bool = False                # varsa sil yeniden yap
    normalize_embeddings: bool = True          # cosine similarity için normalize


# ──────────────────────────────────────────────────────────
# CHUNK TARAMA
# ──────────────────────────────────────────────────────────
def scan_chunks(chunks_dir: str) -> list[dict]:
    """
    book/chunks/ içindeki tüm .md dosyalarını tarar.
    
    Her chunk için:
        - path: dosya yolu
        - chapter_no: chapter numarası (1, 2, ...)
        - heading_no: başlık numarası ("1.1", "1.2", ...)
        - content: .md içeriği
        - title: ilk başlık satırı (# veya ##)
    """
    base = Path(chunks_dir)
    if not base.exists():
        log.error(f"❌ {chunks_dir} bulunamadı. Önce stage3.py çalıştırın.")
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
            stem = md_file.stem  # "1-1" veya "1-intro"

            # heading_no çıkar
            if stem == f"{chapter_no}-intro":
                heading_no = f"{chapter_no}.0"
                sort_key = (chapter_no, 0.0)
            else:
                m = re.match(rf"{chapter_no}-(\d+)", stem)
                if m:
                    heading_no = f"{chapter_no}.{m.group(1)}"
                    sort_key = (chapter_no, float(m.group(1)))
                else:
                    log.warning(f"⚠ {md_file.name} tanınmadı, atlanıyor.")
                    continue

            content = md_file.read_text(encoding="utf-8").strip()
            if not content:
                continue

            # İlk başlık satırını bul (# veya ##)
            title = ""
            for line in content.split("\n"):
                stripped = line.strip()
                if stripped.startswith("#"):
                    title = stripped.lstrip("#").strip()
                    break

            chunks.append({
                "path": str(md_file),
                "chapter_no": chapter_no,
                "heading_no": heading_no,
                "title": title,
                "content": content,
                "sort_key": sort_key,
                "char_count": len(content),
            })

    log.info(f"📄 Toplam chunk: {len(chunks)}")
    log.info(f"   Chapter sayısı: {len(chapter_dirs)}")
    if chunks:
        log.info(f"   Toplam karakter: {sum(c['char_count'] for c in chunks):,}")
        log.info(f"   Ortalama chunk:  {sum(c['char_count'] for c in chunks) // len(chunks):,} karakter")

    return chunks


# ──────────────────────────────────────────────────────────
# EMBEDDING MODELİ YÜKLE
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
            log.info(f"🎮 GPU tespit edildi: {device_name} ({device_count} adet)")
            return "cuda"
    except ImportError:
        pass
    log.info("💻 GPU bulunamadı, CPU kullanılacak.")
    return "cpu"


def load_embedding_model(model_name: str, device: str):
    """sentence-transformers modelini yükler."""
    log.info(f"🧠 Embedding model yükleniyor: {model_name} (device: {device})")
    t0 = time.time()

    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name, device=device)
    model.eval()

    elapsed = time.time() - t0
    log.info(f"   Model boyutu: {model.get_sentence_embedding_dimension()} dim")
    log.info(f"   Yükleme süresi: {elapsed:.1f}s")

    return model


# ──────────────────────────────────────────────────────────
# EMBEDDING + FAISS INDEX
# ──────────────────────────────────────────────────────────
def build_index(chunks: list[dict], config: IndexConfig):
    """
    Chunk'ları embed eder ve FAISS index oluşturur.
    """
    import numpy as np
    import faiss

    # 1. Modeli yükle
    model = load_embedding_model(config.embedding_model, config.embedding_device)

    # 2. Metinleri hazırla (başlık + içerik)
    texts = []
    for c in chunks:
        # Başlık varsa önce başlık, sonra içerik — daha iyi embedding
        if c["title"]:
            texts.append(f"{c['title']}\n\n{c['content']}")
        else:
            texts.append(c["content"])

    # 3. Embedding
    log.info(f"📐 Embedding hesaplanıyor ({len(texts)} chunk, batch={config.batch_size})...")
    t0 = time.time()

    embeddings = model.encode(
        texts,
        batch_size=config.batch_size,
        show_progress_bar=True,
        normalize_embeddings=config.normalize_embeddings,
    )

    elapsed = time.time() - t0
    dim = embeddings.shape[1]
    log.info(f"   Boyut: {embeddings.shape}")
    log.info(f"   Süre:  {elapsed:.1f}s ({len(texts) / elapsed:.1f} chunk/s)")

    # 4. FAISS index
    log.info("🗂️  FAISS index oluşturuluyor...")
    index = faiss.IndexFlatIP(dim)  # Inner Product = Cosine (normalized)
    index.add(embeddings.astype(np.float32))

    log.info(f"   Index boyutu: {index.ntotal} vektör")
    log.info(f"   Index boyutu: {dim} dim")

    return index, embeddings


# ──────────────────────────────────────────────────────────
# KAYDETME
# ──────────────────────────────────────────────────────────
def save_index(index, chunks: list[dict], config: IndexConfig):
    """
    FAISS index + metadata + config'i kaydeder.
    """
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # FAISS
    faiss_path = output_dir / "index.faiss"
    import faiss
    faiss.write_index(index, str(faiss_path))
    log.info(f"💾 Index kaydedildi: {faiss_path} ({faiss_path.stat().st_size / 1024:.0f} KB)")

    # Metadata (sadece gerekli alanlar)
    metadata = []
    for c in chunks:
        metadata.append({
            "path": c["path"],
            "chapter_no": c["chapter_no"],
            "heading_no": c["heading_no"],
            "title": c["title"],
            "content": c["content"],
            "char_count": c["char_count"],
        })

    meta_path = output_dir / "metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    log.info(f"💾 Metadata kaydedildi: {meta_path} ({meta_path.stat().st_size / 1024:.0f} KB)")

    # Config
    config_path = output_dir / "config.json"
    with open(config_path, "w") as f:
        json.dump({
            "embedding_model": config.embedding_model,
            "normalize_embeddings": config.normalize_embeddings,
            "num_chunks": len(chunks),
            "embedding_dim": index.d,
        }, f, indent=2)
    log.info(f"💾 Config kaydedildi: {config_path}")


# ──────────────────────────────────────────────────────────
# INDEX ÖZETİ
# ──────────────────────────────────────────────────────────
def print_summary(chunks: list[dict], index):
    """Index hakkında özet bilgi yazdırır."""
    chapter_counts = {}
    for c in chunks:
        ch = c["chapter_no"]
        chapter_counts[ch] = chapter_counts.get(ch, 0) + 1

    log.info("\n" + "=" * 60)
    log.info("📊 INDEX ÖZETİ")
    log.info(f"   Toplam chunk:  {len(chunks)}")
    log.info(f"   Embedding dim: {index.d}")
    log.info("   Chapter dağılımı:")
    for ch in sorted(chapter_counts.keys()):
        cnt = chapter_counts[ch]
        bar = "█" * max(1, int(cnt / max(chapter_counts.values()) * 30))
        log.info(f"     Chapter {ch:2d}: {cnt:3d} chunk  {bar}")
    log.info("=" * 60)


# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="RAG Index Oluşturucu — chunk .md'leri embed edip FAISS'e kaydeder."
    )
    parser.add_argument("--embedding_model", type=str, default="all-MiniLM-L6-v2",
                        help="sentence-transformers model adı (varsayılan: all-MiniLM-L6-v2)")
    parser.add_argument("--device", type=str, default="auto",
                        help="cuda / cpu / auto (varsayılan: auto — GPU varsa cuda)")
    parser.add_argument("--batch_size", type=int, default=32,
                        help="embedding batch boyutu (varsayılan: 32)")
    parser.add_argument("--force", "-f", action="store_true",
                        help="Varsa index'i silip yeniden oluştur")
    parser.add_argument("--output_dir", type=str, default="rag/vector_store",
                        help="Çıktı dizini (varsayılan: rag/vector_store)")
    args = parser.parse_args()

    # GPU otomatik tespit
    device = auto_device(args.device)
    log.info(f"🔧 Kullanılan cihaz: {device}")
    if device == "cuda":
        log.info(f"    Batch size embedding için optimize: {min(args.batch_size * 2, 256)}")

    config = IndexConfig(
        embedding_model=args.embedding_model,
        embedding_device=device,
        batch_size=args.batch_size,
        force_rebuild=args.force,
        output_dir=args.output_dir,
    )

    # Force: eski index'i sil
    if config.force_rebuild:
        out_path = Path(config.output_dir)
        if out_path.exists():
            import shutil
            shutil.rmtree(out_path)
            log.info(f"🗑️  Eski index silindi: {out_path}")

    # Varolan index varsa uyar
    index_path = Path(config.output_dir) / "index.faiss"
    if index_path.exists():
        log.warning(f"⚠ Index zaten var: {index_path}")
        log.warning(f"   Yeniden oluşturmak için --force kullanın.")
        log.warning(f"   Devam etmek için 3sn bekleniyor...")
        import time as ttime
        ttime.sleep(3)

    # 1. Chunk'ları tara
    log.info("=" * 60)
    log.info("🔍 CHUNK TARANIYOR")
    chunks = scan_chunks(config.chunks_dir)

    # 2. Embed + Index
    log.info("")
    index, _ = build_index(chunks, config)

    # 3. Kaydet
    log.info("")
    save_index(index, chunks, config)

    # 4. Özet
    print_summary(chunks, index)

    log.info("\n✅ Index oluşturma tamamlandı!")


if __name__ == "__main__":
    main()
