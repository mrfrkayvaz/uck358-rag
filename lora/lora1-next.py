#!/usr/bin/env python3
"""
lora1-next.py — Tüm chapter JSON dosyalarını tek bir JSONL'de birleştirir.

İşlev:
    lora/q_a/{chapter_no}/*.json dosyalarını okur, chapter_title bilgisini
    chapter_headers.json'dan alır ve lora/q_a/qa_dataset.jsonl olarak yazar.

Kullanım:
    uv run python3 lora/lora1-next.py

Çıktı:
    lora/q_a/qa_dataset.jsonl   — Unsloth uyumlu JSONL (question, answer, chapter_title, heading_title, chunk_path)

Gereksinimler:
    - Ana dizinde chapter_headers.json (chapter_no → chapter_title mapping)
    - lora/q_a/ içinde chapter_no/qa*.json dosyaları
"""

import json
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("lora1-next")


def load_chapter_headers(headers_path: str) -> dict[str, str]:
    """chapter_headers.json dosyasını yükler: {chapter_no: chapter_title}"""
    fp = Path(headers_path)
    if not fp.exists():
        log.error(f"❌ {headers_path} bulunamadı!")
        sys.exit(1)
    with open(fp, encoding="utf-8") as f:
        data = json.load(f)
    log.info(f"📖 Chapter headers yüklendi: {len(data)} bölüm")
    return data


def collect_json_files(qa_dir: str) -> list[Path]:
    """lora/q_a/ altındaki tüm chapter_no/*.json dosyalarını toplar."""
    base = Path(qa_dir)
    if not base.exists():
        log.error(f"❌ {qa_dir} dizini bulunamadı!")
        sys.exit(1)

    json_files = sorted(base.rglob("*.json"))
    log.info(f"📂 Bulunan JSON dosyaları: {len(json_files)}")
    return json_files


def build_qa_dataset(
    json_files: list[Path],
    chapter_headers: dict[str, str],
    output_path: str,
) -> int:
    """
    Tüm JSON dosyalarını okur, chapter_no → chapter_title mapping yapar
    ve JSONL formatında yazar.
    """
    output_fp = Path(output_path)
    output_fp.parent.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0
    latex_ok = 0

    with open(output_fp, "w", encoding="utf-8") as out:
        for jf in json_files:
            try:
                with open(jf, encoding="utf-8") as f:
                    item = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                log.warning(f"⚠ Okunamadı: {jf} — {e}")
                skipped += 1
                continue

            # Zorunlu alan kontrolü
            if "question" not in item or "answer" not in item:
                log.warning(f"⚠ Atlanıyor (question/answer eksik): {jf}")
                skipped += 1
                continue

            question = item.get("question", "").strip()
            answer = item.get("answer", "").strip()
            if not question or not answer:
                log.warning(f"⚠ Atlanıyor (boş içerik): {jf}")
                skipped += 1
                continue

            # chapter_no → chapter_title
            chapter_no = str(item.get("chapter_no", ""))
            chapter_title = chapter_headers.get(chapter_no, "")
            if not chapter_title:
                log.warning(f"⚠ chapter_no '{chapter_no}' headers'ta bulunamadı: {jf}")
                chapter_title = f"Chapter {chapter_no}"

            heading_title = item.get("heading_title", "").strip()
            chunk_path = item.get("chunk_path", "").strip()

            # LaTeX kontrol
            if "$" in answer:
                latex_ok += 1

            # Yeni format
            new_item = {
                "question": question,
                "answer": answer,
                "chapter_title": chapter_title,
                "heading_title": heading_title,
                "chunk_path": chunk_path,
            }

            out.write(json.dumps(new_item, ensure_ascii=False) + "\n")
            written += 1

    # Dosya sonuna \n garantisi (Unsloth gereksinimi)
    with open(output_fp, "rb") as f:
        raw = f.read()
    if not raw.endswith(b"\n"):
        with open(output_fp, "ab") as f:
            f.write(b"\n")

    return written, skipped, latex_ok


def validate_output(output_path: str):
    """Oluşturulan JSONL'yi doğrular ve istatistik yazdırır."""
    fp = Path(output_path)
    if not fp.exists():
        log.error(f"❌ {output_path} oluşturulamadı!")
        return

    records = []
    with open(fp, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                log.warning(f"⚠ Satır {line_no}: JSON hatası — {e}")

    if not records:
        log.warning("⚠ Hiç kayıt yok!")
        return

    lengths = [len(r["answer"]) for r in records]
    latex_count = sum(1 for r in records if "$" in r["answer"])
    chapters = set(r.get("chapter_title", "") for r in records)

    log.info(f"\n📊 VALIDASYON RAPORU:")
    log.info(f"   Toplam kayıt:       {len(records)}")
    log.info(f"   Ort. cevap:         {sum(lengths) // len(lengths)} karakter")
    log.info(f"   Min/Max:            {min(lengths)} / {max(lengths)}")
    log.info(f"   LaTeX içeren:       {latex_count}/{len(records)} (%{100 * latex_count // len(records)})")
    log.info(f"   Chapter sayısı:     {len(chapters)}")
    log.info(f"   Chapter listesi:    {', '.join(sorted(chapters))}")
    log.info(f"   Dosya sonu \\n:     {'✅ var' if Path(output_path).read_bytes().endswith(b'\\n') else '❌ yok'}")


def main():
    # Yollar (ana dizin = proje kökü)
    project_root = Path(__file__).resolve().parent.parent  # lora/../ = ana dizin
    headers_path = project_root / "chapter_headers.json"
    qa_dir = project_root / "lora" / "q_a"
    output_path = qa_dir / "qa_dataset.jsonl"

    log.info("=" * 60)
    log.info("🔧 LORA1-NEXT: JSON → JSONL DÖNÜŞTÜRÜCÜ")
    log.info("=" * 60)

    # 1. Chapter headers yükle
    chapter_headers = load_chapter_headers(str(headers_path))

    # 2. JSON dosyalarını topla
    json_files = collect_json_files(str(qa_dir))
    if not json_files:
        log.warning("⚠ Hiç JSON dosyası bulunamadı!")
        return

    # 3. Dataset oluştur
    log.info("\n📝 Dataset oluşturuluyor...")
    written, skipped, latex_ok = build_qa_dataset(
        json_files, chapter_headers, str(output_path)
    )

    log.info(f"\n✅ İşlem tamamlandı!")
    log.info(f"   Yazılan:    {written}")
    log.info(f"   Atlanan:    {skipped}")
    log.info(f"   LaTeX'li:   {latex_ok}")
    log.info(f"   Çıktı:      {output_path}")

    # 4. Doğrulama
    log.info("\n🔍 Çıktı doğrulanıyor...")
    validate_output(str(output_path))

    log.info(f"\n{'=' * 60}")
    log.info(f"🚀 Şimdi lora2.py ile eğitime geçebilirsiniz:")
    log.info(f"   uv run python3 lora/lora2.py")
    log.info(f"{'=' * 60}")


if __name__ == "__main__":
    main()
