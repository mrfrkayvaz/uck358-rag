#!/usr/bin/env python3
"""
stage3.py - Chapter markdown'larını bölüm başlıklarına göre chunk'lara ayırır.

Kullanım:
    uv run python3 stage3.py                           # tüm chapter'lar
    uv run python3 stage3.py --chapter 1               # sadece chapter 1

Çıktı Yapısı:
    book/chunks/
        1/                       # chapter 1 klasörü
            1-1.md               # bölüm 1.1 + içindeki tüm alt başlıklar
            1-2.md               # bölüm 1.2 + içindeki tüm alt başlıklar
            1-3.md               # bölüm 1.3 ...
            ...                  # (###, #### seviyeleri ayrılmaz, üst başlık içinde kalır)
        2/
            2-1.md
            2-2.md
            ...

Mantık:
    - ## (level 2) başlıkları chunk sınırıdır
    - Her ## başlığı -> ayrı bir .md dosyası
    - ###, #### vb. alt başlıklar -> üst ## dosyasının içinde kalır
    - Dosya adı: {chapter}-{bölüm_no}.md  (örn: 1-1.md, 1-2.md)
"""

import argparse
import re
import sys
from pathlib import Path


# ============================================================
# YAPILANDIRMA
# ============================================================
BOOK_DIR = Path("book")
MARKDOWNS_DIR = BOOK_DIR / "markdowns"
CHUNKS_DIR = BOOK_DIR / "chunks"

DEBUG = False


# ============================================================
# CHUNK'A AYIRMA MANTIĞI
# ============================================================
def parse_chapter_markdown(md_content: str) -> list[dict]:
    """
    Markdown içeriğini ## (level 2) başlıklarından böler.
    
    Her chunk şu yapıda:
    {
        "heading": "## 1.1 Inherent Stability",   # başlık satırı
        "section_num": "1",                         # bölüm numarası (örn: 1)
        "content": "başlık + içerik...",             # chunk'ın tüm içeriği
        "is_intro": False,                           # giriş kısmı mı?
    }
    
    Eğer başlık numarasızsa (örn: "## Introduction"), section_num=None olur
    ve sırayla numara verilir.
    """
    lines = md_content.split("\n")
    
    chunks = []
    current_lines = []
    current_heading = None
    current_section_num = None
    is_intro = True
    section_counter = 1  # numarasız başlıklar için sayaç
    
    # Chapter numarasını birden fazla pattern'le ara
    chapter_num = None
    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            text = line.lstrip("#").strip()
            # "# CHAPTER 1 Title"
            m = re.match(r"(?:CHAPTER|Chapter)\s+(\d+)", text, re.IGNORECASE)
            if m:
                chapter_num = m.group(1)
                break
            # "# 1. Title"
            m = re.match(r"(\d+)\.\s", text)
            if m:
                chapter_num = m.group(1)
                break
            # "# 1 Early Developments"
            m = re.match(r"(\d+)\s", text)
            if m:
                chapter_num = m.group(1)
                break
    
    for line in lines:
        # Level 2 başlık mı? (## ile başlayan, ### veya # ile karışmasın)
        if re.match(r"^##\s+(?!##)", line):  # ## ama ### değil
            # Önceki birikmiş içeriği kaydet
            if current_lines:
                content = "\n".join(current_lines).strip()
                if content:
                    chunks.append({
                        "heading": current_heading,
                        "section_num": current_section_num,
                        "content": content,
                        "is_intro": is_intro,
                    })
            
            # Yeni başlığa başla
            current_lines = [line]
            current_heading = line
            
            # Başlıktan bölüm numarasını çıkar (örn: "## 1.1 Başlık" -> "1")
            # Numarasız başlıklar için slug kullan (örn: "Conclusion" -> "conclusion")
            heading_text = line.lstrip("#").strip()
            num_match = re.match(r"(\d+)\.(\d+)", heading_text)
            if num_match:
                current_section_num = num_match.group(2)  # "1.1" -> "1"
            else:
                # Numarasız başlık -> ilk 2 kelimenin slug'ı
                slug = re.sub(r"[^a-zA-Z0-9]+", "_", heading_text.lower()).strip("_")[:30]
                current_section_num = slug if slug else str(section_counter)
                section_counter += 1

            is_intro = False
            continue
        
        # Level 1 başlık (#) — intro'ya ekle, sonraki chapter başlıklarını yok say
        if line.startswith("# ") and not line.startswith("## "):
            if is_intro:
                current_lines.append(line)
                continue
            continue
        
        current_lines.append(line)
    
    # Son birikmiş içeriği kaydet
    if current_lines:
        content = "\n".join(current_lines).strip()
        if content:
            chunks.append({
                "heading": current_heading,
                "section_num": current_section_num,
                "content": content,
                "is_intro": is_intro,
            })
    
    return chunks, chapter_num


def extract_chapter_number(filename: str) -> str:
    """chapter1.md -> 1, chapter2.md -> 2"""
    m = re.match(r"chapter(\d+)", filename)
    return m.group(1) if m else None


def get_filename(chapter_num: str, chunk: dict) -> str:
    """
    Chunk için dosya adını belirler.
    - Normal bölüm: {chapter_num}-{section_num}.md  (örn: 1-1.md)
    - Giriş kısmı:   {chapter_num}-intro.md         (örn: 1-intro.md)
    """
    if chunk["is_intro"]:
        return f"{chapter_num}-intro.md"
    elif chunk["section_num"]:
        return f"{chapter_num}-{chunk['section_num']}.md"
    else:
        # Numarasız başlık - sıra numarası kullan
        return f"{chapter_num}-{chunk.get('_fallback_num', 1)}.md"


# ============================================================
# CHUNK'LARI KAYDETME
# ============================================================
def save_chunks(chunks: list[dict], chapter_num: str, output_dir: Path):
    """Chunk'lari ilgili chapter klasorune kaydeder.
    Ayni isimde dosya varsa sessizce uzerine yazmaz, suffix ekler."""

    chapter_dir = output_dir / chapter_num
    chapter_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []
    used_names = set()

    for i, chunk in enumerate(chunks):
        filename = get_filename(chapter_num, chunk)

        # Duplicate korumasi: ayni isim varsa _2, _3 ekle
        base, ext = filename.rsplit(".", 1) if "." in filename else (filename, "")
        counter = 2
        original = filename
        while filename in used_names or (chapter_dir / filename).exists():
            filename = f"{base}_{counter}.{ext}"
            counter += 1
        if filename != original:
            print(f"         ⚠ Duplicate: '{original}' -> '{filename}'")

        used_names.add(filename)
        filepath = chapter_dir / filename
        filepath.write_text(chunk["content"], encoding="utf-8")
        saved_files.append(filename)

        if DEBUG:
            section_preview = chunk["heading"] if chunk["heading"] else "(giris)"
            print(f"         {filename:18s} | {section_preview[:60]}")

    return saved_files


# ============================================================
# ANA DÖNÜŞTÜRME FONKSİYONU
# ============================================================
def process_chapter(chapter_num: int):
    """Tek bir chapter'ı chunk'lara ayırır."""
    
    md_path = MARKDOWNS_DIR / f"chapter{chapter_num}.md"
    if not md_path.exists():
        print(f"Hata: {md_path} bulunamadı.")
        return False
    
    print(f"\n{'='*60}")
    print(f"Chapter {chapter_num} chunk'lanıyor...")
    print(f"  Kaynak: {md_path}")
    print(f"{'='*60}")
    
    try:
        # Markdown'ı oku
        md_content = md_path.read_text(encoding="utf-8")
        print(f"  Okunan: {len(md_content)} karakter")
        
        # Chunk'lara ayır
        chunks, chapter_num_str = parse_chapter_markdown(md_content)
        chapter_num_str = chapter_num_str or str(chapter_num)
        
        print(f"  Bulunan chunk: {len(chunks)} adet")
        
        # Chunk'ları kaydet
        saved = save_chunks(chunks, chapter_num_str, CHUNKS_DIR)
        print(f"  Kaydedilen: {len(saved)} dosya -> {CHUNKS_DIR / chapter_num_str}/")
        if DEBUG:
            for f in saved:
                print(f"    - {f}")
        
        return True
        
    except Exception as e:
        print(f"  HATA: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================
# ANA
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="Chapter markdown'larını bölüm başlıklarına göre chunk'lara ayır."
    )
    parser.add_argument(
        "--chapter", "-c",
        type=int,
        action="append",
        help="İşlenecek chapter numarası (birden fazla verilebilir). "
             "Belirtilmezse tüm chapter'lar işlenir."
    )
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Debug modu"
    )
    
    args = parser.parse_args()
    global DEBUG
    DEBUG = args.debug
    
    # Hangi chapter'lar?
    if args.chapter:
        chapter_numbers = args.chapter
    else:
        if not MARKDOWNS_DIR.exists():
            print(f"Hata: {MARKDOWNS_DIR} klasörü bulunamadı. Önce stage2.py çalıştırın.")
            sys.exit(1)
        
        md_files = sorted(MARKDOWNS_DIR.glob("chapter*.md"))
        chapter_numbers = []
        for f in md_files:
            m = re.match(r"chapter(\d+)\.md", f.name)
            if m:
                chapter_numbers.append(int(m.group(1)))
        
        if not chapter_numbers:
            print(f"Hata: {MARKDOWNS_DIR} içinde chapter .md dosyası bulunamadı.")
            sys.exit(1)
    
    print(f"İşlenecek chapter'lar: {chapter_numbers}")
    
    success = True
    for ch in chapter_numbers:
        if not process_chapter(ch):
            success = False
    
    print(f"\n{'='*60}")
    if success:
        print("✅ Tüm chapter'lar başarıyla chunk'lara ayrıldı.")
    else:
        print("⚠️  Bazı chapter'larda hata oluştu.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
