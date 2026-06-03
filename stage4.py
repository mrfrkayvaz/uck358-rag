#!/usr/bin/env python3
"""
stage4.py — book/chunks/ içindeki .md dosyalarındaki görsel referanslarını
evaluate_images.py ile oluşturulmuş Gemini yorumlarıyla değiştirir.

İşlem:
    1. book/chunks/ altındaki tüm .md'leri tara
    2. ![alt](path) referanslarını bul
    3. book/assets-evaluation/ altında aynı isimli .md'yi bul
    4. Görsel satırını, Gemini'nin yorum metniyle değiştir
    5. Dosyayı kaydet

Kullanım:
    uv run python3 stage4.py                    # tüm chunk'lar
    uv run python3 stage4.py --chapter 1        # sadece chapter 1
    uv run python3 stage4.py --dry-run          # değişiklik yapmadan göster
"""

import argparse
import re
import sys
from pathlib import Path

# ──────────────────────────────────────────────────────────
# YAPILANDIRMA
# ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
CHUNKS_DIR = BASE_DIR / "book" / "chunks"
EVAL_DIR = BASE_DIR / "book" / "assets-evaluation"

REPLACEMENT_TEMPLATE = """

---
<!-- GÖRSEL YORUMU (Gemini): {filename} -->
{interpretation}
---
"""


def find_evaluation_md(image_path: str) -> Path | None:
    """
    Görsel yolundan assets-evaluation'daki .md dosyasını bulur.

    Örnek:
        ../assets/chapter3/image_0.png
        → book/assets-evaluation/chapter3/image_0.md
    """
    # Yoldan dosya adını ve üst klasörü çıkar
    image_path = image_path.strip()

    # Göreceli yolu temizle
    parts = Path(image_path).parts
    # "assets/chapter3/image_0.png" kısmını bul
    try:
        assets_idx = [p.lower() for p in parts].index("assets")
    except ValueError:
        return None

    # assets'ten sonraki kısmı al: chapter3/image_0
    rel = Path(*parts[assets_idx + 1:])
    stem = rel.stem  # image_0

    # assets-evaluation içinde ara: chapter3/image_0.md
    eval_path = EVAL_DIR / rel.parent / f"{stem}.md"
    if eval_path.exists():
        return eval_path
    return None


def replace_images_in_md(md_content: str, md_file_path: Path, dry_run: bool = False) -> tuple[str, int, list[str]]:
    """
    Markdown içindeki tüm ![...](...) referanslarını bulur,
    her biri için evaluation .md'sini arar ve değiştirir.

    Returns:
        (yeni_içerik, değiştirilen_görsel_sayısı, eksik_evaluation_listesi)
    """
    img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

    replacements = 0
    missing = []

    def replacer(match):
        nonlocal replacements
        alt_text = match.group(1)
        img_path = match.group(2)

        eval_md = find_evaluation_md(img_path)

        if eval_md is None:
            missing.append(Path(img_path).name)
            return match.group(0)  # evaluation yok, dokunma

        interpretation = eval_md.read_text(encoding="utf-8").strip()
        if not interpretation:
            return match.group(0)

        replacements += 1
        filename = Path(img_path).name

        mark = "KURU ÇALIŞMA" if dry_run else "DEĞİŞTİRİLDİ"
        print(f"   [{mark}] {filename} → {eval_md.relative_to(BASE_DIR)}")

        return REPLACEMENT_TEMPLATE.format(
            filename=filename,
            interpretation=interpretation,
        ).strip()

    new_content = img_pattern.sub(replacer, md_content)
    return new_content, replacements, missing


def process_chapter(chapter_num: int, dry_run: bool = False) -> tuple[int, list[str]]:
    """Bir chapter'ın tüm chunk .md'lerini işler.
    Returns: (değiştirilen, eksik_evaluation_listesi)"""
    chapter_dir = CHUNKS_DIR / str(chapter_num)
    if not chapter_dir.exists():
        print(f"  ⚠ {chapter_dir} bulunamadı.")
        return 0, []

    md_files = sorted(chapter_dir.glob("*.md"))
    if not md_files:
        print(f"  ⚠ {chapter_dir} içinde .md yok.")
        return 0, []

    total_replaced = 0
    all_missing = []

    for md_file in md_files:
        original = md_file.read_text(encoding="utf-8")
        new_content, count, missing = replace_images_in_md(original, md_file, dry_run)

        if count > 0 and not dry_run:
            md_file.write_text(new_content, encoding="utf-8")
            print(f"  💾 {md_file.relative_to(BASE_DIR)} kaydedildi ({count} görsel)")
        elif count > 0 and dry_run:
            print(f"  👁️  {md_file.relative_to(BASE_DIR)} (kuru çalışma — {count} görsel)")
        else:
            print(f"  ─ {md_file.name} (görsel yok veya evaluation eksik)")

        total_replaced += count
        all_missing.extend(missing)

    return total_replaced, all_missing


def main():
    parser = argparse.ArgumentParser(
        description="Chunk .md'lerdeki görselleri Gemini yorumlarıyla değiştir."
    )
    parser.add_argument("--chapter", "-c", type=int, action="append",
                        help="Sadece belirtilen chapter (tekrarlanabilir)")
    parser.add_argument("--dry-run", "-n", action="store_true",
                        help="Değişiklik yapmadan ne olacağını göster")
    args = parser.parse_args()

    if not EVAL_DIR.exists():
        print(f"⚠ {EVAL_DIR} bulunamadı.")
        print(f"  Önce 'uv run python3 evaluate_images.py' çalıştırın.")
        sys.exit(1)

    # Hangi chapter'lar?
    if args.chapter:
        chapter_numbers = args.chapter
    else:
        chapter_numbers = sorted(
            int(d.name) for d in CHUNKS_DIR.iterdir()
            if d.is_dir() and d.name.isdigit()
        )

    if not chapter_numbers:
        print(f"HATA: {CHUNKS_DIR} içinde chapter klasörü yok.")
        sys.exit(1)

    mode = "KURU ÇALIŞMA" if args.dry_run else "İŞLEM"
    print(f"🔍 Stage4 — {mode} MODU")
    print(f"   Chunk: {CHUNKS_DIR}")
    print(f"   Eval:  {EVAL_DIR}")
    print(f"   Chapter: {chapter_numbers}")
    print()

    grand_total = 0
    all_missing = []
    for ch in chapter_numbers:
        print(f"── Chapter {ch} ──")
        count, missing = process_chapter(ch, args.dry_run)
        grand_total += count
        all_missing.extend(missing)
        print()

    print(f"{'='*50}")
    print(f"Toplam değiştirilen görsel: {grand_total}")

    if all_missing:
        unique_missing = sorted(set(all_missing))
        print(f"\n⚠ {len(unique_missing)} görselin Gemini yorumu henüz alınmamış:")
        print(f"   Önce şunu çalıştırın: uv run python3 evaluate_images.py")
        for name in unique_missing:
            print(f"     - {name}")

    if args.dry_run:
        print(f"\n⚠ Kuru çalışma — değişiklik yapılmadı. --dry-run olmadan tekrar çalıştırın.")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
