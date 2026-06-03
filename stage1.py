#!/usr/bin/env python3
"""
stage1.py - PDF'deki chapter'ları ayrı PDF'lere split eder.

Kullanım:
    python3 stage1.py

PDF: book/<filename>.pdf (book klasöründeki ilk PDF)
Çıktı: book/chapters/chapter1.pdf, chapter2.pdf, ... şeklinde kaydedilir.
"""

import os
import re
import fitz  # PyMuPDF


def find_pdf_in_book() -> str:
    """book/ klasöründeki ilk .pdf dosyasının yolunu döndürür."""
    book_dir = "book"
    if not os.path.isdir(book_dir):
        raise FileNotFoundError(f"'{book_dir}' klasörü bulunamadı.")

    pdfs = [f for f in os.listdir(book_dir) if f.lower().endswith(".pdf")]
    if not pdfs:
        raise FileNotFoundError(f"'{book_dir}' içinde .pdf dosyası bulunamadı.")

    return os.path.join(book_dir, pdfs[0])


def find_chapters(doc: fitz.Document) -> list[int]:
    """
    PDF içinde 'CHAPTER N' pattern'ini arayarak chapter başlangıç sayfalarını
    bulur. Sayfa numaraları 1-indexed olarak döndürülür.
    """
    chapter_pages = []
    pattern = re.compile(r"^CHAPTER\s+(\d+)$")

    for i in range(doc.page_count):
        page = doc[i]
        text = page.get_text()
        for line in text.split("\n"):
            if pattern.match(line.strip()):
                chapter_pages.append(i + 1)  # 1-indexed
                break

    return chapter_pages


def validate_chapters(chapter_pages: list[int], doc: fitz.Document):
    """Bulunan chapter'ların tutarlılığını kontrol eder."""
    if len(chapter_pages) < 2:
        print(f"Uyarı: Sadece {len(chapter_pages)} chapter bulundu.")
    print(f"Toplam chapter: {len(chapter_pages)}")
    print(f"PDF toplam sayfa: {doc.page_count}")
    print(f"Chapter başlangıç sayfaları: {chapter_pages}")


def split_chapters(doc: fitz.Document, chapter_pages: list[int], output_dir: str):
    """
    Chapter'ları ayrı PDF'lere böler ve output_dir altına kaydeder.
    """
    os.makedirs(output_dir, exist_ok=True)

    for idx, start in enumerate(chapter_pages):
        start_idx = start - 1  # 0-indexed'e çevir

        # Bitiş sayfasını belirle: son chapter ise PDF sonuna kadar,
        # değilse bir sonraki chapter'ın bir önceki sayfasına kadar
        if idx < len(chapter_pages) - 1:
            end_idx = chapter_pages[idx + 1] - 2  # bir sonraki chapter - 1 sayfa
        else:
            end_idx = doc.page_count - 1

        chapter_num = idx + 1
        output_path = os.path.join(output_dir, f"chapter{chapter_num}.pdf")

        # Yeni PDF oluştur ve sayfaları ekle
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=start_idx, to_page=end_idx)
        new_doc.save(output_path)
        new_doc.close()

        page_count = end_idx - start_idx + 1
        print(f"  ✓ chapter{chapter_num}.pdf  ->  {page_count} sayfa  (PDF sayfa {start}-{end_idx + 1})")


def main():
    # PDF dosyasını bul
    pdf_path = find_pdf_in_book()
    print(f"PDF: {pdf_path}")

    # PDF'i aç
    doc = fitz.open(pdf_path)
    print(f"Toplam sayfa: {doc.page_count}")

    # Chapter'ları bul
    chapter_pages = find_chapters(doc)
    validate_chapters(chapter_pages, doc)

    if not chapter_pages:
        print("Hata: Hiç chapter bulunamadı.")
        doc.close()
        return

    # Chapter'ları split et
    output_dir = os.path.join("book", "chapters")
    print(f"\nChapter'lar split ediliyor -> {output_dir}/")
    split_chapters(doc, chapter_pages, output_dir)

    doc.close()
    print("\n✅ Tüm chapter'lar başarıyla kaydedildi.")


if __name__ == "__main__":
    main()
