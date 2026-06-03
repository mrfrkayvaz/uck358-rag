#!/usr/bin/env python3
"""
stage2.py - Chapter PDF'lerini Marker ile Markdown'a dönüştürür.

Kullanım:
    uv run python3 stage2.py                           # tüm chapter'lar
    uv run python3 stage2.py --chapter 1               # sadece chapter 1
    uv run python3 stage2.py --chapter 1 --chapter 3   # chapter 1 ve 3

İşlem Adımları:
    1. Chapter PDF'ini Marker ile Markdown'a çevir (LaTeX denklemler korunur)
    2. Görselleri book/assets/chapterN/ altına kaydet
    3. Header/footer (sayfa numarası, kitap adı, bölüm başlığı) temizliği
    4. Tablo görsellerini kırp, assets'e kaydet
    5. Temiz .md dosyasını book/markdowns/ altına yaz
"""

import argparse
import re
import os
import sys
from pathlib import Path


# ============================================================
# YAPILANDIRMA
# ============================================================
BOOK_DIR = Path("book")
CHAPTERS_DIR = BOOK_DIR / "chapters"
MARKDOWNS_DIR = BOOK_DIR / "markdowns"
ASSETS_DIR = BOOK_DIR / "assets"

# Header/Footer temizliğinde silinecek pattern'ler
# (PDF'den çıkarılan örüntülere göre doldurulacak)
HEADER_FOOTER_PATTERNS = [
    # Örnek: sayfa numaraları (tek başına satırdaki rakamlar)
    r"^\d+$",
    # Örnek: "Airplane Stability and Control, Second Edition"
    r"^Airplane Stability and Control, Second Edition$",
    # Örnek: "CHAPTER \d+.*"  (header'da tekrar eden chapter başlığı)
    r"^CHAPTER\s+\d+.*",
]

# Markdown'da resim placeholder template'i
IMAGE_TEMPLATE = "![{alt_text}]({rel_path})"

# Debug modu
DEBUG = False


# ============================================================
# 1. MARKER DÖNÜŞÜM
# ============================================================
def detect_device() -> tuple[str, object]:
    """GPU varsa 'cuda' + torch.bfloat16 döndürür, yoksa 'cpu' + torch.float32.
    🔴 KRİTİK: dtype torch objesi olmalı, string değil!"""
    try:
        import torch
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            print(f"      🎮 GPU tespit edildi: {device_name}")
            return "cuda", torch.bfloat16
    except ImportError:
        pass
    import torch
    print(f"      💻 GPU bulunamadı, CPU kullanılıyor.")
    return "cpu", torch.float32


def convert_pdf_to_markdown(pdf_path: Path) -> tuple[str, dict]:
    """
    Marker kullanarak PDF'i Markdown'a çevirir.
    
    Args:
        pdf_path: Chapter PDF'inin yolu
        
    Returns:
        (markdown_metni, resources_dict)
        - markdown_metni: Dönüştürülmüş Markdown içeriği
        - resources_dict: {dosya_adı: bytes} - görsel/table resimleri
    """
    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    
    print(f"  [1/4] Marker dönüşümü başlatılıyor...")
    
    device, dtype = detect_device()
    
    converter = PdfConverter(
        artifact_dict=create_model_dict(device=device, dtype=dtype),
    )
    rendered = converter(str(pdf_path))
    
    md_content = rendered.markdown
    resources = rendered.resources  # {filename: bytes}
    
    print(f"         Markdown: {len(md_content)} karakter")
    print(f"         Resources (görsel/table): {len(resources)} adet")
    
    return md_content, resources


# ============================================================
# 2. GÖRSEL ÇIKARMA VE KAYDETME
# ============================================================
def save_resources(resources: dict, chapter_num: int) -> dict[str, str]:
    """
    Marker'ın çıkardığı görsel/table resource'larını 
    book/assets/chapter{N}/ klasörüne kaydeder.
    
    Args:
        resources: {dosya_adı: bytes} sözlüğü
        chapter_num: Chapter numarası
        
    Returns:
        {orijinal_ad: yeni_göreceli_yol} mapping'i
    """
    asset_dir = ASSETS_DIR / f"chapter{chapter_num}"
    asset_dir.mkdir(parents=True, exist_ok=True)
    
    mapping = {}
    for filename, data in resources.items():
        # Marker resource'ları "image_0.png", "table_0.png" şeklinde isimlendirir
        ext = Path(filename).suffix if Path(filename).suffix else ".png"
        dest_name = f"{filename}"
        dest_path = asset_dir / dest_name
        dest_path.write_bytes(data)
        
        # Göreceli yol (markdown içinde kullanılacak)
        rel_path = f"../assets/chapter{chapter_num}/{dest_name}"
        mapping[filename] = rel_path
        
        if DEBUG:
            print(f"         Kaydedildi: {rel_path} ({len(data)} bytes)")
    
    print(f"  [2/4] {len(resources)} resource kaydedildi -> {asset_dir}")
    return mapping


# ============================================================
# 3. HEADER/FOOTER TEMİZLEME
# ============================================================
def clean_header_footer(md_content: str, chapter_num: int) -> str:
    """
    Header/footer gürültülerini temizler.
    - Sadece TEK BAŞINA satırdaki sayfa numaraları
    - Kitap adı tekrarı
    - Chapter başlığı tekrarı (sayfa üstünde)
    - Aşırı tekrar eden satırlar (header/footer kalıpları)
    """
    lines = md_content.split("\n")
    cleaned = []

    # Chapter başlığını al (ilk # satırı)
    chapter_title = ""
    for line in lines:
        if line.startswith("# ") and not line.startswith("## "):
            chapter_title = line.lstrip("#").strip()
            break

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 1. TEK BAŞINA sayfa numarası satırları (sadece rakam)
        if re.fullmatch(r"\d{1,4}", stripped):
            # Komşu satırlara bak: öncesi/sonrası boşsa gerçek sayfa no'dur
            prev_empty = (i == 0 or not lines[i-1].strip())
            next_empty = (i == len(lines)-1 or not lines[i+1].strip())
            if prev_empty or next_empty:
                if DEBUG:
                    print(f"         Sayfa no: '{stripped}'")
                continue

        # 2. Kitap adı / sürüm bilgisi
        if stripped.lower() in (
            "airplane stability and control, second edition",
            "airplane stability and control",
        ):
            if DEBUG:
                print(f"         Kitap adı: '{stripped[:50]}'")
            continue

        # 3. Header'da tekrar eden CHAPTER başlığı (sayfa üstünde)
        if re.fullmatch(r"CHAPTER\s+\d+.*", stripped):
            if chapter_title and stripped != chapter_title:
                if DEBUG:
                    print(f"         Header: '{stripped[:50]}'")
                continue

        cleaned.append(line)

    return "\n".join(cleaned)


# ============================================================
# 4. RESOURCE REFERANSLARINI DÜZELTME
# ============================================================
def fix_resource_references(md_content: str, resource_mapping: dict[str, str]) -> str:
    """
    Markdown ![...](...) referanslarını asset yollarına çevirir.
    🔴 Sadece ![...]() pattern'inde değiştirir — LaTeX $...$ içindekilere dokunmaz.
    
    Ayrıca alt metin yoksa dosya adından otomatik alt metin ekler.
    """
    for old_name, new_path in resource_mapping.items():
        escaped = re.escape(old_name)

        # 1. ![](old_name) → ![](new_path)
        md_content = re.sub(
            rf"!\[\]\(\{escaped}\)",
            f"![]({new_path})",
            md_content,
        )

        # 2. ![alt](old_name) → ![alt](new_path)  (alt varsa koru)
        md_content = re.sub(
            rf"!\[([^\]]*)\]\(\{escaped}\)",
            rf"![\1]({new_path})",
            md_content,
        )

    return md_content


# ============================================================
# 5. POST-PROCESSING (TABLOLAR, FORMAT)
# ============================================================
def post_process_markdown(md_content: str) -> str:
    """
    Markdown çıktısında son düzeltmeler:
    - Aşırı boş satırları temizle
    - LaTeX display/block netliğini kontrol et
    - İç içe geçmiş LaTeX bloklarını düzelt
    - Başlık hiyerarşisini kontrol et
    """
    # 1. 3'ten fazla ardışık boş satırı 2'ye indir
    md_content = re.sub(r"\n{4,}", "\n\n\n", md_content)

    # 2. Başlıklardan önce boş satır olduğundan emin ol
    md_content = re.sub(r"([^\n])\n(#{1,6}\s)", r"\1\n\n\2", md_content)

    # 3. İç içe geçmiş $$$$ bloklarını düzelt (nesne içinde nesne)
    md_content = re.sub(r"\$\$\s*\$\$", "$$\n$$", md_content)

    # 4. LaTeX kalitesini raporla
    display_eq = len(re.findall(r"\$\$", md_content)) // 2
    inline_eq = len(re.findall(r"(?<!\$)\$(?!\$)", md_content))
    if DEBUG:
        print(f"         LaTeX: {display_eq} display denklem, {inline_eq} inline")

    return md_content


# ============================================================
# 6. ANA DÖNÜŞTÜRME FONKSİYONU
# ============================================================
def convert_chapter(chapter_num: int):
    """Tek bir chapter'ı PDF'ten Markdown'a dönüştürür."""
    
    pdf_path = CHAPTERS_DIR / f"chapter{chapter_num}.pdf"
    if not pdf_path.exists():
        print(f"Hata: {pdf_path} bulunamadı.")
        return False
    
    output_dir = MARKDOWNS_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"chapter{chapter_num}.md"
    
    print(f"\n{'='*60}")
    print(f"Chapter {chapter_num} dönüştürülüyor...")
    print(f"  Kaynak: {pdf_path}")
    print(f"  Hedef:  {output_path}")
    print(f"{'='*60}")
    
    try:
        # Adım 1: Marker ile PDF -> Markdown
        md_content, resources = convert_pdf_to_markdown(pdf_path)
        
        # Adım 2: Resource'ları (görsel/table) assets'e kaydet
        resource_mapping = save_resources(resources, chapter_num)
        
        # Adım 3: Header/footer temizliği
        md_content = clean_header_footer(md_content, chapter_num)
        print(f"  [3/4] Header/footer temizliği tamam")
        
        # Adım 4: Resource referanslarını düzelt + alt metin ekle
        md_content = fix_resource_references(md_content, resource_mapping)
        md_content = add_image_alt_text(md_content, chapter_num)
        
        # Adım 5: Post-processing + kalite kontrolü
        md_content = post_process_markdown(md_content)
        quality = validate_markdown_quality(md_content, chapter_num)
        if quality["warnings"]:
            for w in quality["warnings"]:
                print(f"  ⚠  {w}")
        
        # Çıktıyı yaz
        output_path.write_text(md_content, encoding="utf-8")
        print(f"  [4/4] {output_path} kaydedildi ({len(md_content)} karakter)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ HATA: {e}")
        import traceback
        traceback.print_exc()
        return False


# ============================================================
# 6. GÖRSEL ALT METİN + KALİTE KONTROLÜ
# ============================================================
def add_image_alt_text(md_content: str, chapter_num: int) -> str:
    """
    ![](path) referanslarına bağlamdan alt metin ekler.
    Figure/Table başlığı bulamazsa chapter numaralı alt metin koyar.
    """
    alt_counter = {}

    def _replacer(match):
        path = match.group(1)
        pos = match.start()
        snippet = md_content[max(0, pos-250):pos]
        caption = re.search(
            r"(?:Figure|Fig|Table)\s*[\d.]+[:.]\s*([^\n]{3,80})",
            snippet,
        )
        if caption:
            alt = caption.group(1).strip()
        else:
            key = path.split("/")[-1]
            alt_counter[key] = alt_counter.get(key, 0) + 1
            alt = f"Chapter {chapter_num} - Figure {alt_counter[key]}"
        return f"![{alt}]({path})"

    return re.sub(r"!\[\]\(([^)]+)\)", _replacer, md_content)


def validate_markdown_quality(md_content: str, chapter_num: int) -> dict:
    """
    Markdown kalitesini kontrol eder.
    - LaTeX varligi
    - Image referans sayisi
    - Baslik hiyerarsisi
    """
    warnings = []

    if len(md_content.strip()) < 100:
        warnings.append(f"Chapter {chapter_num}: icerik cok kisa ({len(md_content)} kar)")

    latex = len(re.findall(r"\$\$|\$(?!\$)", md_content))
    if latex == 0:
        warnings.append(f"Chapter {chapter_num}: hic LaTeX ($) yok — denklemler kaybolmus olabilir")

    images = len(re.findall(r"!\[([^\]]*)\]\([^)]+\)", md_content))
    h1 = len(re.findall(r"^#\s", md_content, re.MULTILINE))
    h2 = len(re.findall(r"^##\s", md_content, re.MULTILINE))
    if h1 == 0 or h2 == 0:
        warnings.append(f"Chapter {chapter_num}: baslik hiyerarsisi zayif (H1={h1}, H2={h2})")

    print(f"         LaTeX: {latex}+ | Images: {images} | H1={h1} H2={h2}")
    return {"warnings": warnings}


# ============================================================
# ANA
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="Chapter PDF'lerini Marker ile Markdown'a dönüştür."
    )
    parser.add_argument(
        "--chapter", "-c",
        type=int,
        action="append",
        help="Dönüştürülecek chapter numarası (birden fazla verilebilir). "
             "Belirtilmezse tüm chapter'lar dönüştürülür."
    )
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Debug modu (detaylı log gösterir)"
    )
    
    args = parser.parse_args()
    
    global DEBUG
    DEBUG = args.debug
    
    # Hangi chapter'ların dönüştürüleceğini belirle
    if args.chapter:
        chapter_numbers = args.chapter
    else:
        # Tüm chapter'ları bul
        if not CHAPTERS_DIR.exists():
            print(f"Hata: {CHAPTERS_DIR} klasörü bulunamadı. Önce stage1.py çalıştırın.")
            sys.exit(1)
        
        chapter_files = sorted(CHAPTERS_DIR.glob("chapter*.pdf"))
        chapter_numbers = []
        for f in chapter_files:
            m = re.match(r"chapter(\d+)\.pdf", f.name)
            if m:
                chapter_numbers.append(int(m.group(1)))
        
        if not chapter_numbers:
            print(f"Hata: {CHAPTERS_DIR} içinde chapter PDF'i bulunamadı.")
            sys.exit(1)
    
    print(f"Dönüştürülecek chapter'lar: {chapter_numbers}")
    
    success = True
    for ch in chapter_numbers:
        if not convert_chapter(ch):
            success = False
    
    print(f"\n{'='*60}")
    if success:
        print("✅ Tüm chapter'lar başarıyla dönüştürüldü.")
    else:
        print("⚠️  Bazı chapter'larda hata oluştu.")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
