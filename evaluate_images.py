#!/usr/bin/env python3
"""
evaluate_images.py — book/assets/ içindeki tüm görselleri OpenRouter'daki
görüntü destekli bir modele gönderip yorumlatır. Çıktıları book/assets-evaluation/
altına görselle aynı isimli .md dosyası olarak kaydeder.

Kullanım:
    uv run python3 evaluate_images.py                  # sadece yeni görseller
    uv run python3 evaluate_images.py --force          # tüm görselleri yeniden
    uv run python3 evaluate_images.py --limit 5        # ilk 5 görsel

Model:
    google/gemini-2.0-flash-001 (görüntü destekler, OpenRouter'da ücretsiz)
    DeepSeek modelleri görüntü desteklemediği için Gemini kullanılır.
"""

import argparse
import base64
import json
import re
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

# ──────────────────────────────────────────────────────────
# YAPILANDIRMA
# ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "book" / "assets"
OUTPUT_DIR = BASE_DIR / "book" / "assets-evaluation"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
# Gemini Flash — görüntü destekler, OpenRouter'da hızlı
MODEL = "openai/gpt-4o-mini"

MAX_RETRIES = 3
RETRY_DELAY = 5
REQUEST_DELAY = 1.5  # rate limit

# Context prompt (görsel yorumlaması için)
SYSTEM_PROMPT = (
    "You are an expert aerospace engineer analyzing figures from the textbook "
    "\"Airplane Stability and Control, Second Edition\" by Malcolm J. Abzug and "
    "E. Eugene Larrabee. Interpret the figure precisely: explain what variables "
    "are shown, what physical phenomenon or concept it illustrates, the axes and "
    "their units if visible, and the key engineering insight a student should "
    "take away. Use LaTeX ($...$ or $$...$$) for equations when relevant. "
    "Be concise but thorough (100-300 words)."
)


# ──────────────────────────────────────────────────────────
# .env OKUMA (dotenv veya manuel)
# ──────────────────────────────────────────────────────────
def load_api_key() -> str:
    env_path = BASE_DIR / ".env"

    # Önce python-dotenv dene
    try:
        from dotenv import load_dotenv
        load_dotenv(env_path)
        import os
        key = os.getenv("OPENROUTER_API_KEY", "")
        if key:
            return key.strip().strip("\"'")
    except ImportError:
        pass

    # Manuel fallback
    if not env_path.exists():
        print("HATA: .env bulunamadı.")
        sys.exit(1)
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("OPENROUTER_API_KEY"):
                key = line.split("=", 1)[1].strip().strip("\"'")
                return key
    print("HATA: OPENROUTER_API_KEY .env'de yok.")
    sys.exit(1)


# ──────────────────────────────────────────────────────────
# GÖRSEL TARAMA
# ──────────────────────────────────────────────────────────
def find_images() -> list[Path]:
    """book/assets/ altındaki tüm görsel dosyalarını bulur."""
    if not ASSETS_DIR.exists():
        print(f"HATA: {ASSETS_DIR} bulunamadı.")
        sys.exit(1)

    images = []
    for img in sorted(ASSETS_DIR.rglob("*")):
        if img.is_file() and img.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"):
            images.append(img)

    if not images:
        print(f"Görsel bulunamadı: {ASSETS_DIR}")
        sys.exit(1)

    return images


# ──────────────────────────────────────────────────────────
# OPENROUTER GÖRÜNTÜ İSTEĞİ
# ──────────────────────────────────────────────────────────
def encode_image_base64(path: Path) -> str:
    """Görseli base64'e çevirir."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def call_vision_model(api_key: str, image_path: Path, retry: int = 0) -> str | None:
    """Görüntüyü base64 olarak OpenRouter'a gönderir, yanıtı döndürür."""
    # MIME türü belirle
    ext = image_path.suffix.lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp"}
    mime = mime_map.get(ext, "image/png")

    b64 = encode_image_base64(image_path)
    data_uri = f"data:{mime};base64,{b64}"

    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Interpret this figure from the textbook. "
                                              f"Filename: {image_path.name}. "
                                              f"Location: {image_path.parent.name}."},
                    {"type": "image_url", "image_url": {"url": data_uri}},
                ]
            }
        ],
        "temperature": 0.4,
        "max_tokens": 1024,
    }).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/uck358-rag",
        "X-Title": "UCK358 Final Project",
    }

    req = Request(OPENROUTER_URL, data=payload, headers=headers, method="POST")

    try:
        with urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"  ⚠ API hatası: {e}")

    if retry < MAX_RETRIES:
        wait = RETRY_DELAY * (retry + 1)
        print(f"  {retry+1}/{MAX_RETRIES} yeniden deneniyor ({wait}s)...")
        time.sleep(wait)
        return call_vision_model(api_key, image_path, retry + 1)

    return None


# ──────────────────────────────────────────────────────────
# ÇIKTI DOSYA ADI
# ──────────────────────────────────────────────────────────
def output_path_for(image_path: Path, force: bool = False) -> Path | None:
    """
    Görselin değerlendirme çıktısının kaydedileceği yolu döndürür.
    Eğer .md dosyası zaten varsa ve --force değilse None döner.
    """
    # book/assets/chapter1/image_0.png → book/assets-evaluation/chapter1/image_0.md
    rel = image_path.relative_to(ASSETS_DIR)
    out = OUTPUT_DIR / rel.parent / f"{image_path.stem}.md"

    if out.exists() and not force:
        return None  # zaten var, atla

    out.parent.mkdir(parents=True, exist_ok=True)
    return out


# ──────────────────────────────────────────────────────────
# ANA
# ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Görselleri OpenRouter vision model ile yorumlat.")
    parser.add_argument("--force", "-f", action="store_true", help="Tüm görselleri yeniden işle")
    parser.add_argument("--limit", "-l", type=int, default=0, help="İlk N görsel")
    args = parser.parse_args()

    api_key = load_api_key()
    print(f"✅ API key okundu | Model: {MODEL}")

    images = find_images()
    total = len(images)
    print(f"🖼️  {total} görsel bulundu")

    if args.limit > 0:
        images = images[:args.limit]
        print(f"   Limit: {len(images)}")

    skipped = 0
    success = 0
    fail = 0

    for i, img in enumerate(images, 1):
        out = output_path_for(img, force=args.force)

        if out is None:
            skipped += 1
            continue

        short = str(img.relative_to(BASE_DIR))
        print(f"\n[{i}/{len(images)}] {short}")

        # API isteği
        print(f"   📤 Gönderiliyor...", end=" ", flush=True)
        t0 = time.time()
        answer = call_vision_model(api_key, img)

        if answer:
            elapsed = time.time() - t0
            out.write_text(answer, encoding="utf-8")
            print(f"✅ {len(answer)} karakter ({elapsed:.1f}s) → {out.relative_to(BASE_DIR)}")
            success += 1
        else:
            print(f"❌ başarısız")
            fail += 1

        time.sleep(REQUEST_DELAY)

    print(f"\n{'='*60}")
    print(f"📊 RAPOR")
    print(f"   Toplam:    {total}")
    print(f"   İşlenen:   {success}")
    print(f"   Atlanan:   {skipped} (zaten var)")
    print(f"   Başarısız: {fail}")
    print(f"   Çıktı:     {OUTPUT_DIR}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
