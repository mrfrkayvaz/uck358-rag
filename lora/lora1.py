#!/usr/bin/env python3
"""
lora1.py — book/chunks/ içindeki .md dosyalarından OpenRouter API ile
750+ adet yüksek kalite Q&A üretir. JSONL formatında (Unsloth uyumlu).

⚠️ PÜF NOKTALAR:
  1. LaTeX Formatı: Tüm formüller $ veya $$ arasında (Unsloth bunu tanır)
  2. Tutarlılık: Cevap tonu, uzunluğu (200-600 karakter), teknik derinlik aynı
  3. JSONL: Her satır bir JSON obje, dosya sonunda mutlaka \n karakteri

Kullanım:
    uv run python3 lora/lora1.py                           # 750 soru hedef
    uv run python3 lora/lora1.py --total 1000              # 1000 soru
    uv run python3 lora/lora1.py --limit 5 --total 30      # ilk 5 chunk, 30 soru
    uv run python3 lora/lora1.py --resume                  # kaldığı yerden devam
    uv run python3 lora/lora1.py --validate                # dataset kalite kontrolü

Çıktı:
    lora/q_a/qa_dataset.jsonl      # her satır: {"question","answer","chapter_no","heading_no"}
    lora/q_a/validation_report.txt # kalite raporu (--validate ile)
""",

import json
import os
import re
import sys
import time
import argparse
import math
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError


# ============================================================
# YAPILANDIRMA
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent
CHUNKS_DIR = BASE_DIR / "book" / "chunks"
QA_DIR = BASE_DIR / "lora" / "q_a"

# OpenRouter
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-v4-flash"
TOTAL_QA_TARGET = 750  # ⚡ yönerge: en az 500, ideal 750+

# Her API çağrısında kaç Q&A üretilecek (2-3 optimal)
QA_PER_CALL = 3

# Rate limiting
REQUEST_DELAY = 3.0   # saniye
MAX_RETRIES = 5
RETRY_DELAY = 10

DEBUG = False


# ============================================================
# PROMPT
# ============================================================
PROMPT_TEMPLATE = """You are helping build a dataset of exactly {total_target} "analytical reasoning" questions about airplane stability and control. Your goal is to help us reach {total_target} high-quality Q&A pairs.

=== CURRENT PROGRESS ===
Questions generated so far: {current_count} / {total_target}
Remaining to reach target: {remaining}
Total chunks to process: {total_chunks}
Current chunk: #{chunk_index} / {total_chunks}
Chapter: {chapter_no}, Section: {heading_no}

=== HOW MANY QUESTIONS TO GENERATE? ===
YOU decide how many questions (0 to 3) to generate from THIS chunk:
- Generate MORE (2-3) if the content is rich in important stability & control concepts
- Generate FEWER (1) if the content has moderate relevant material  
- Generate NONE (0) if the content is introductory, historical, or lacks examinable theory
- If we are very close to the target ({remaining} remaining), be more selective
- If we are far from the target, be more generous but never exceed 3

=== RULES FOR QUESTIONS ===
1. TYPE: "analytical reasoning" — tests understanding of definitions and theoretical concepts in flight stability & control. NOT memorization. Must require actual thinking.
2. LATEX (mandatory): ALL math must be in $...$ (inline) or $$...$$ (display). Example: "As $V$ increases, how does $C_{m_\\alpha}$ change?"
3. CONSISTENCY: Answers 200-600 characters, academic English, undergraduate level, precise.
4. UNIQUENESS: Each question must test a DIFFERENT concept.

=== OUTPUT FORMAT ===
Return ONLY valid JSON. qa_pairs can be empty array [] if you decide not to generate any:
{{
  "reasoning": "Briefly: why {0,1,2,3} questions?",
  "qa_pairs": [
    {{
      "question": "...",
      "answer": "..."
    }}
  ]
}}

=== CHAPTER CONTENT ===
{content}"""


# ============================================================
# .env OKUMA
# ============================================================
def load_env() -> str:
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        print("HATA: .env dosyası bulunamadı!")
        sys.exit(1)

    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("OPENROUTER_API_KEY"):
                key = line.split("=", 1)[1].strip().strip("\"'")
                return key

    print("HATA: .env içinde OPENROUTER_API_KEY bulunamadı!")
    sys.exit(1)


# ============================================================
# OPENROUTER API
# ============================================================
def call_openrouter(api_key: str, content: str, progress: dict, retry: int = 0) -> list[dict] | None:
    """
    OpenRouter API'ye istek atar. Model 0-3 arası Q&A üretir.
    progress: {"current_count", "total_target", "remaining", "total_chunks", "chunk_index", "chapter_no", "heading_no"}
    """
    prompt = PROMPT_TEMPLATE.format(
        total_target=progress["total_target"],
        current_count=progress["current_count"],
        remaining=progress["remaining"],
        total_chunks=progress["total_chunks"],
        chunk_index=progress["chunk_index"],
        chapter_no=progress["chapter_no"],
        heading_no=progress["heading_no"],
        content=content,
    )

    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 4096,
    }).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/your-project",
        "X-Title": "LORA QA Generator",
    }

    req = Request(OPENROUTER_URL, data=payload, headers=headers, method="POST")

    try:
        with urlopen(req, timeout=180) as resp:
            response_data = json.loads(resp.read().decode("utf-8"))
            assistant_msg = response_data["choices"][0]["message"]["content"]

        qa_list = parse_llm_response(assistant_msg)
        if qa_list:
            return qa_list

        print(f"         ⚠ JSON parse başarısız, ham yanıt kaydediliyor...")
        return [{"question": assistant_msg, "answer": "", "_raw": True}]

    except Exception as e:
        print(f"         ⚠ Hata: {e}")

    if retry < MAX_RETRIES:
        wait = RETRY_DELAY * (retry + 1)
        print(f"         {retry+1}/{MAX_RETRIES} yeniden deneniyor ({wait}s)...")
        time.sleep(wait)
        return call_openrouter(api_key, content, progress, retry + 1)

    return None


def parse_llm_response(text: str) -> list[dict] | None:
    """LLM yanıtından Q&A listesi çıkarır."""
    text = text.strip()

    # ```json ... ``` bloğu
    m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        text = m.group(1).strip()

    # JSON parse
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Süslü parantezler arasındaki kısmı dene
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            try:
                data = json.loads(m.group())
            except json.JSONDecodeError:
                return None
        else:
            return None

    # qa_pairs dizisi mi?
    if isinstance(data, dict) and "qa_pairs" in data:
        pairs = data["qa_pairs"]
    elif isinstance(data, list):
        pairs = data
    elif isinstance(data, dict) and "question" in data:
        pairs = [data]
    else:
        return None

    # Doğrula ve temizle
    result = []
    for p in pairs:
        if isinstance(p, dict) and "question" in p and "answer" in p:
            result.append({
                "question": p["question"].strip(),
                "answer": p["answer"].strip(),
            })
    return result if result else None


# ============================================================
# CHUNK DOSYALARINI TARA
# ============================================================
def find_chunk_files() -> list[dict]:
    """
    book/chunks/ içindeki tüm .md dosyalarını bulur.
    """
    files = []
    chapter_dirs = sorted(
        [d for d in CHUNKS_DIR.iterdir() if d.is_dir() and d.name.isdigit()],
        key=lambda p: int(p.name)
    )

    for ch_dir in chapter_dirs:
        chapter_no = int(ch_dir.name)
        for md_file in sorted(ch_dir.glob("*.md")):
            stem = md_file.stem  # "1-1" veya "1-intro"
            if stem == f"{chapter_no}-intro":
                heading_no = f"{chapter_no}.0"
                sort_heading = 0.0
            else:
                m = re.match(rf"{chapter_no}-(\d+)", stem)
                if m:
                    heading_no = f"{chapter_no}.{m.group(1)}"
                    sort_heading = float(m.group(1))
                else:
                    continue

            files.append({
                "path": md_file,
                "chapter_no": chapter_no,
                "heading_no": heading_no,
                "sort_key": (chapter_no, sort_heading),
                "content_length": 0,  # sonra doldurulacak
            })

    files.sort(key=lambda f: f["sort_key"])

    # İçerik uzunluğunu hesapla (dağıtım için)
    for f in files:
        try:
            f["content_length"] = len(f["path"].read_text(encoding="utf-8"))
        except:
            f["content_length"] = 1

    return files


# ============================================================
# QA DAĞITIM HESAPLAMA
# ============================================================
def distribute_qa(files: list[dict], total_target: int, qa_per_call: int) -> list[tuple[dict, int]]:
    """
    Toplam total_target Q&A'yı chunk'lara içerik uzunluğuna göre dağıtır.
    
    Returns:
        [(file_info, o_chunktan_istenecek_soru_sayisi), ...]
    """
    total_length = sum(f["content_length"] for f in files)
    if total_length == 0:
        total_length = len(files)

    distribution = []
    remaining = total_target

    for i, f in enumerate(files):
        # Oransal dağıtım
        share = max(1, round(total_target * f["content_length"] / total_length))
        # QA_PER_CALL'in katına yuvarla (API her çağrıda birden çok üretsin)
        share = math.ceil(share / qa_per_call) * qa_per_call

        if i == len(files) - 1:
            # Son chunk'a kalanı ver
            share = remaining

        distribution.append((f, min(share, remaining)))
        remaining -= share

        if remaining <= 0:
            break

    # Kalan varsa sona ekle
    if remaining > 0 and distribution:
        last_idx = len(distribution) - 1
        dist = list(distribution[last_idx])
        distribution[last_idx] = (dist[0], dist[1] + remaining)

    return distribution


# ============================================================
# JSONL KAYDETME (Unsloth uyumlu)
# ============================================================
# JSONL formatı: her satır bir JSON obje, dosya sonunda \n karakteri.
# Bu format Unsloth tarafından doğrudan okunabilir.

JSONL_PATH = QA_DIR / "qa_dataset.jsonl"


def append_to_jsonl(qa_data: dict):
    """
    Q&A verisini JSONL dosyasına ekler.
    Her satır: {"question": "...", "answer": "...", "chapter_no": N, "heading_no": "..."}
    Dosya sonunda mutlaka \n olması sağlanır.
    """
    QA_DIR.mkdir(parents=True, exist_ok=True)
    with open(JSONL_PATH, "a", encoding="utf-8") as f:
        line = json.dumps(qa_data, ensure_ascii=False)
        f.write(line + "\n")  # 🔴 her satır sonunda \n garantisi


def count_jsonl_lines() -> int:
    """JSONL dosyasındaki mevcut satır sayısı (resume için)."""
    if not JSONL_PATH.exists():
        return 0
    with open(JSONL_PATH, encoding="utf-8") as f:
        return sum(1 for _ in f)


def validate_jsonl(filepath: Path = None) -> dict:
    """
    JSONL dosyasını validation eder:
    - Her satır geçerli JSON mu?
    - Son satır \n ile bitiyor mu?
    - LaTeX formatı ($...$) var mı?
    - Cevap uzunlukları tutarlı mı?
    - chapter_no ve heading_no eksiksiz mi?
    """
    fp = filepath or JSONL_PATH
    if not fp.exists():
        return {"error": f"{fp} bulunamadı"}

    report = {
        "total_lines": 0,
        "valid_json": 0,
        "invalid_json": 0,
        "has_latex": 0,
        "no_latex": 0,
        "answer_lengths": [],
        "ends_with_newline": False,
        "missing_fields": 0,
        "issues": [],
    }

    with open(fp, "rb") as f:
        raw = f.read()

    # Son karakter \n mi?
    report["ends_with_newline"] = raw.endswith(b"\n")
    if not report["ends_with_newline"]:
        report["issues"].append("❌ Dosya sonunda \n karakteri yok! Unsloth hata verebilir.")

    lines = raw.decode("utf-8").split("\n")
    for i, line in enumerate(lines):
        if not line.strip():
            continue  # boş satır (genelde son satır)
        report["total_lines"] += 1

        try:
            data = json.loads(line)
            report["valid_json"] += 1

            # Alan kontrolü
            if not all(k in data for k in ("question", "answer", "chapter_no", "heading_no")):
                report["missing_fields"] += 1
                report["issues"].append(f"  ⚠ Satır {i+1}: eksik alan")

            # LaTeX kontrolü
            answer = data.get("answer", "")
            if "$" in answer:
                report["has_latex"] += 1
            else:
                report["no_latex"] += 1

            # Cevap uzunluğu
            report["answer_lengths"].append(len(answer))

        except json.JSONDecodeError:
            report["invalid_json"] += 1
            report["issues"].append(f"  ❌ Satır {i+1}: geçersiz JSON")

    # İstatistik
    lens = report["answer_lengths"]
    if lens:
        report["avg_answer_len"] = sum(lens) / len(lens)
        report["min_answer_len"] = min(lens)
        report["max_answer_len"] = max(lens)
        report["latex_ratio"] = f"{report['has_latex'] / report['valid_json'] * 100:.1f}%" if report["valid_json"] else "N/A"

    return report


# ============================================================
# ANA
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="Chunk .md'lerden OpenRouter ile JSONL dataset üret (Unsloth uyumlu)."
    )
    parser.add_argument("--total", "-t", type=int, default=TOTAL_QA_TARGET,
                        help=f"Toplam üretilecek soru sayısı (varsayılan: {TOTAL_QA_TARGET})")
    parser.add_argument("--limit", "-l", type=int,
                        help="İşlenecek maksimum chunk sayısı")
    parser.add_argument("--resume", "-r", action="store_true",
                        help="Kaldığı yerden devam et")
    parser.add_argument("--validate", "-v", action="store_true",
                        help="Dataset kalite kontrolü yap (üretim yapmaz)")
    parser.add_argument("--debug", "-d", action="store_true")
    args = parser.parse_args()

    global DEBUG
    DEBUG = args.debug

    # ── VALIDATE MODU ──
    if args.validate:
        print("\n" + "=" * 60)
        print("🔍 DATASET VALIDASYONU")
        print("=" * 60)
        report = validate_jsonl()
        for key, val in report.items():
            if key == "issues":
                if val:
                    print(f"\n  Sorunlar ({len(val)} adet):")
                    for issue in val:
                        print(f"    {issue}")
                else:
                    print(f"  Sorun: ✅ hiç yok")
            elif key == "answer_lengths":
                continue
            else:
                print(f"  {key}: {val}")
        print("\n" + "=" * 60)
        return

    # ── API key ──
    api_key = load_env()
    print(f"✅ OPENROUTER_API_KEY okundu")

    # ── Chunk dosyalarını bul ──
    files = find_chunk_files()
    if not files:
        print("HATA: book/chunks/ içinde .md dosyası bulunamadı.")
        sys.exit(1)

    print(f"Toplam chunk dosyası: {len(files)}")

    # ── Resume: JSONL'deki mevcut satır sayısını bul ──
    existing_count = count_jsonl_lines()
    if args.resume and existing_count > 0:
        print(f"📄 Kaldığı yerden devam: {existing_count} satır var")
    elif existing_count > 0:
        print(f"📄 Mevcut JSONL: {existing_count} satır — devam edilecek")
    else:
        print("📄 Yeni dataset oluşturuluyor")

    # ── Limit ──
    if args.limit and args.limit < len(files):
        files = files[:args.limit]

    total_target = args.total
    total_chunks = len(files)

    print(f"\n🎯 Hedef: {total_target} soru")
    print(f"📦 Toplam chunk: {total_chunks}")
    print(f"📊 Mevcut: {existing_count} | Kalan: {total_target - existing_count}")
    print(f"📋 Format: JSONL (Unsloth uyumlu) — model 0-3 soru/chunk karar verecek")
    print(f"💾 Çıktı: {JSONL_PATH}")
    print()

    current_count = existing_count
    success_count = 0
    fail_count = 0
    start_idx = max(0, existing_count // 3)  # chunk atlama (kabaca)

    for i, file_info in enumerate(files):
        chunk_idx = i + 1

        # Hedefe ulaştık mı?
        if current_count >= total_target:
            print(f"\n🎉 Hedefe ulaşıldı! {current_count}/{total_target} soru")
            break

        remaining = total_target - current_count
        md_path = file_info["path"]
        chapter_no = file_info["chapter_no"]
        heading_no = file_info["heading_no"]

        content = md_path.read_text(encoding="utf-8").strip()
        if not content:
            continue

        # Progress bilgisi
        progress = {
            "total_target": total_target,
            "current_count": current_count,
            "remaining": remaining,
            "total_chunks": total_chunks,
            "chunk_index": chunk_idx,
            "chapter_no": chapter_no,
            "heading_no": heading_no,
        }

        print(f"[{chunk_idx}/{total_chunks}] {md_path.name}  (ch.{chapter_no}, {heading_no})")
        print(f"         📊 {current_count}/{total_target} | kalan: {remaining} | ", end="")
        sys.stdout.flush()

        qa_list = call_openrouter(api_key, content, progress)

        if qa_list:
            gen_count = 0
            for qa in qa_list:
                if "_raw" in qa:
                    print(f"⚠ RAW")
                    continue
                qa["chapter_no"] = chapter_no
                qa["heading_no"] = heading_no
                append_to_jsonl(qa)
                gen_count += 1
                current_count += 1
                success_count += 1
            print(f"✅ +{gen_count} soru (toplam: {current_count}/{total_target})")
        else:
            print(f"❌ API hatası")
            fail_count += 1

        # İlerleme check
        if success_count + fail_count >= total_chunks:
            print(f"\n⚠ Tüm chunk'lar işlendi. {current_count}/{total_target} soru üretilebildi.")
            break

        time.sleep(REQUEST_DELAY)

    # ── Final rapor ──
    final_count = count_jsonl_lines()
    print(f"\n{'='*60}")
    print(f"📊 İŞLEM RAPORU")
    print(f"   Hedef:           {total_target}")
    print(f"   Üretilen:        {final_count}")
    print(f"   Bu sefer:        +{success_count}")
    print(f"   Başarısız istek: {fail_count}")
    print(f"   Tamamlanma:      {final_count / total_target * 100:.0f}%")
    print(f"   Çıktı:           {JSONL_PATH}")
    print()

    # Kalite kontrolü yap
    if success_count > 0:
        print("🔍 Kalite kontrolü yapılıyor...")
        report = validate_jsonl()
        print(f"   Toplam satır:    {report.get('total_lines', '?')}")
        print(f"   LaTeX oranı:     {report.get('latex_ratio', '?')}")
        print(f"   Ort. cevap:      {report.get('avg_answer_len', '?'):.0f} karakter")
        print(f"   Min/Max:         {report.get('min_answer_len', '?')}/{report.get('max_answer_len', '?')}")
        if report.get("issues"):
            print(f"   ⚠ Sorunlar:       {len(report['issues'])} adet")
            for iss in report["issues"][:3]:
                print(f"      {iss}")
        else:
            print(f"   ✅ Hiç sorun yok")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
