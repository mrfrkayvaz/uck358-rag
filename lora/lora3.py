#!/usr/bin/env python3
"""
lora3.py — Eğitilmiş LoRA modeline questions klasöründeki soruları
tek tek gönderir ve cevapları answers-lora/ klasörüne a1.md, a2.md şeklinde kaydeder.

Kullanım:
    uv run python3 lora/lora3.py                                # tüm sorular
    uv run python3 lora/lora3.py --limit 5                      # ilk 5 soru
    uv run python3 lora/lora3.py --question "What is dihedral?" # tek soru
    uv run python3 lora/lora3.py --adapter lora/lora-out/final  # farklı adapter

Gereksinimler:
    - Eğitilmiş LoRA adapter'ı (varsayılan: lora/lora-out/final/)
    - questions/ klasöründe .md dosyaları (q1.md, q2.md, ...)

Çıktı:
    answers-lora/
        a1.md
        a2.md
        ...
"""

import argparse
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
log = logging.getLogger("lora3")


# ──────────────────────────────────────────────────────────
# YAPILANDIRMA
# ──────────────────────────────────────────────────────────
@dataclass
class Config:
    model_name: str = "Qwen/Qwen3-1.7B"
    adapter_dir: Optional[Path] = Path("lora/lora-out/final")
    questions_dir: Path = Path("questions")
    answers_dir: Path = Path("answers-lora")
    max_new_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    device: str = "auto"
    limit: int = 0
    single_question: Optional[str] = None


# ──────────────────────────────────────────────────────────
# GPU TESPİT
# ──────────────────────────────────────────────────────────
def detect_device(cfg: Config) -> str:
    if cfg.device != "auto":
        return cfg.device
    try:
        import torch
        if torch.cuda.is_available():
            log.info(f"🎮 GPU: {torch.cuda.get_device_name(0)}")
            return "cuda"
    except ImportError:
        pass
    log.info("💻 GPU yok, CPU (yavaş olabilir)")
    return "cpu"


# ──────────────────────────────────────────────────────────
# MODEL YÜKLEME
# ──────────────────────────────────────────────────────────
def load_model_and_tokenizer(cfg: Config):
    """Base model + LoRA adapter yükler."""
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    device = detect_device(cfg)
    dtype = torch.bfloat16 if device == "cuda" else torch.float32

    log.info(f"📦 Base model: {cfg.model_name}")
    tokenizer = AutoTokenizer.from_pretrained(
        cfg.model_name, trust_remote_code=True, use_fast=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        cfg.model_name,
        device_map="auto" if device == "cuda" else None,
        torch_dtype=dtype,
        trust_remote_code=True,
    )
    if device == "cpu":
        model = model.to("cpu")

    # LoRA adapter
    if cfg.adapter_dir and cfg.adapter_dir.exists() and (cfg.adapter_dir / "adapter_config.json").exists():
        log.info(f"🔧 LoRA adapter: {cfg.adapter_dir}")
        model = PeftModel.from_pretrained(model, str(cfg.adapter_dir))
        log.info("✅ Adapter yüklendi")
    else:
        log.warning(f"⚠ Adapter bulunamadı: {cfg.adapter_dir}")
        log.warning("   Base model (FINE-TUNE EDİLMEMİŞ) kullanılacak.")

    model.eval()
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    log.info(f"   Param: {total:,} toplam, {trainable:,} trainable")

    return model, tokenizer, device


# ──────────────────────────────────────────────────────────
# SORU OKUMA
# ──────────────────────────────────────────────────────────
def load_questions(cfg: Config) -> list[dict]:
    """questions/ klasöründeki .md dosyalarını sıralı okur."""
    if not cfg.questions_dir.exists():
        log.error(f"❌ {cfg.questions_dir}/ bulunamadı.")
        sys.exit(1)

    md_files = sorted(
        cfg.questions_dir.glob("*.md"),
        key=lambda f: int(re.search(r"(\d+)", f.stem).group(1))
        if re.search(r"(\d+)", f.stem) else 9999,
    )
    if not md_files:
        log.error(f"❌ {cfg.questions_dir}/ içinde .md dosyası yok.")
        sys.exit(1)

    questions = []
    for f in md_files:
        content = f.read_text(encoding="utf-8").strip()
        if content:
            questions.append({"index": len(questions) + 1, "filename": f.name, "content": content})

    if cfg.limit > 0:
        questions = questions[:cfg.limit]

    log.info(f"📄 {len(questions)} soru yüklendi")
    for q in questions:
        log.info(f"   [{q['index']}] {q['filename']}: {q['content'][:70]}...")

    return questions


# ──────────────────────────────────────────────────────────
# CEVAP ÜRETME
# ──────────────────────────────────────────────────────────
def generate_answer(model, tokenizer, question: str, device: str, cfg: Config) -> str:
    """LoRA modelinden cevap üretir."""
    import torch

    messages = [
        {"role": "system",
         "content": "You are an expert aerospace engineering tutor. Answer with precise "
                    "technical explanations. Use LaTeX ($...$ or $$...$$) for equations."},
        {"role": "user", "content": question},
    ]

    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)

    if device == "cuda":
        inputs = {k: v.to("cuda") for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs, max_new_tokens=cfg.max_new_tokens,
            temperature=cfg.temperature, top_p=cfg.top_p,
            do_sample=True, pad_token_id=tokenizer.eos_token_id,
        )

    response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()
    return response


# ──────────────────────────────────────────────────────────
# CEVAP KAYDETME
# ──────────────────────────────────────────────────────────
def save_answer(answer: str, index: int, question: str, cfg: Config) -> Path:
    """answers-lora/a{index}.md olarak kaydeder."""
    cfg.answers_dir.mkdir(parents=True, exist_ok=True)
    fp = cfg.answers_dir / f"a{index}.md"
    content = f"<!-- SORU: {question.strip()} -->\n\n{answer}"
    fp.write_text(content, encoding="utf-8")
    return fp


# ──────────────────────────────────────────────────────────
# ANA
# ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="LoRA model ile soru-cevap.")
    parser.add_argument("--limit", "-l", type=int, default=0)
    parser.add_argument("--question", "-q", type=str, default=None, help="Tek soru")
    parser.add_argument("--adapter", "-a", type=str, default=None)
    parser.add_argument("--questions_dir", type=str, default="questions")
    parser.add_argument("--answers_dir", type=str, default="answers-lora")
    parser.add_argument("--model", type=str, default="Qwen/Qwen3-1.7B")
    parser.add_argument("--max_tokens", type=int, default=512)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--no_lora", action="store_true")
    args = parser.parse_args()

    cfg = Config(
        model_name=args.model,
        max_new_tokens=args.max_tokens,
        temperature=args.temperature,
        questions_dir=Path(args.questions_dir),
        answers_dir=Path(args.answers_dir),
        limit=args.limit,
        single_question=args.question,
    )

    # adapter: --adapter ile verilmişse onu kullan, --no_lora varsa None
    if args.no_lora:
        cfg.adapter_dir = None
    elif args.adapter:
        cfg.adapter_dir = Path(args.adapter)

    # Model yükle
    log.info("=" * 60)
    log.info("🤖 LoRA MODEL YÜKLENİYOR")
    log.info("=" * 60)
    model, tokenizer, device = load_model_and_tokenizer(cfg)

    # ── Tek soru ──
    if cfg.single_question:
        log.info(f"❓ {cfg.single_question[:80]}...")
        t0 = time.time()
        answer = generate_answer(model, tokenizer, cfg.single_question, device, cfg)
        elapsed = time.time() - t0
        log.info(f"   Süre: {elapsed:.1f}s | {len(answer)} karakter")
        print(f"\n{'='*60}\n{answer}\n{'='*60}")
        return

    # ── Dosyalardan soru oku ──
    questions = load_questions(cfg)
    log.info(f"\n{'='*60}")
    log.info(f"📝 CEVAPLAMA BAŞLIYOR ({len(questions)} soru)")
    log.info(f"   Çıktı: {cfg.answers_dir}/")
    log.info(f"{'='*60}\n")

    success = 0
    for q in questions:
        idx = q["index"]
        log.info(f"[{idx}/{len(questions)}] {q['filename']}")

        t0 = time.time()
        try:
            answer = generate_answer(model, tokenizer, q["content"], device, cfg)
            elapsed = time.time() - t0
            fp = save_answer(answer, idx, q["content"], cfg)
            log.info(f"   ✅ {len(answer)} karakter ({elapsed:.1f}s) -> {fp.name}")
            success += 1
        except Exception as e:
            log.error(f"   ❌ Hata: {e}")
            save_answer(f"[HATA] {e}", idx, q["content"], cfg)

        if device == "cpu":
            time.sleep(0.3)

    log.info(f"\n{'='*60}")
    log.info(f"📊 RAPOR: {success}/{len(questions)} başarılı")
    log.info(f"   Çıktı: {cfg.answers_dir}/")
    log.info(f"{'='*60}")


if __name__ == "__main__":
    main()
