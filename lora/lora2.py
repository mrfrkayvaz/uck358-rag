#!/usr/bin/env python3
"""
lora2.py — Qwen3:1.7B modelini LoRA ile fine-tune eder.

Veri Formatı (JSONL — Unsloth uyumlu):
    lora/q_a/qa_dataset.jsonl
    Her satır: {"question", "answer", "chapter_title", "heading_title", "chunk_path"}
    - Tüm formüller $ veya $$ arasında (LaTeX)
    - Cevap uzunluğu 200-600 karakter arası
    - Dosya sonunda \n karakteri (Unsloth gereksinimi)

Kullanım:
    uv run python3 lora/lora2.py                                          # GPU varsa otomatik
    uv run python3 lora/lora2.py --use_unsloth                             # Unsloth ile eğitim
    uv run python3 lora/lora2.py --num_epochs 5 --lr 2e-4                 # hiperparametre
    uv run python3 lora/lora2.py --batch_size 8 --grad_accum 2            # GPU'ya göre batch
    uv run python3 lora/lora2.py --no_4bit --bf16                         # 4bit yoksa (yüksek VRAM)
    uv run python3 lora/lora2.py --resume_from_checkpoint                 # kaldığı yerden devam
    uv run python3 lora/lora2.py --eval_only --adapter_path lora-out/     # sadece değerlendirme
    uv run python3 lora/lora2.py --validate                               # dataset validation
    uv run python3 lora/lora2.py --merge --adapter_path lora-out/final/   # adapter merge

Çıktı:
    lora/lora-out/                      # LoRA adapter ağırlıkları (Unsloth veya PEFT)
    lora/lora-out/final/                # Merge edilmiş tam model
    lora/q_a/validation_report.json     # Dataset kalite raporu

Gereksinimler (uv add ile kurulur):
    uv add torch transformers accelerate peft bitsandbytes trl datasets

GPU Desteği:
    - CUDA varsa:  otomatik 4-bit QLoRA (NF4) + bf16 + gradient checkpointing
    - VRAM 6GB:    batch=2, grad_accum=8  (~5.5 GB kullanır)
    - VRAM 8GB:    batch=4, grad_accum=4  (~7.5 GB kullanır)
    - VRAM 12GB+:  batch=8, grad_accum=2  (~10 GB kullanır)
    - Unsloth:     ~%%40 daha hızlı, %%50 daha az bellek

⚠️ PÜF NOKTALAR:
  1. LaTeX: Tüm formüller $/$$ içinde olmalı (Unsloth bunu tanır)
  2. Tutarlılık: Cevap boyu 200-600 karakter, aynı ton/derinlik
  3. JSONL: Her satır JSON, dosya sonunda \n karakteri şart
"""

import argparse
import json
import logging
import math
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ──────────────────────────────────────────────────────────
# logging
# ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("lora2")


# ──────────────────────────────────────────────────────────
# GPU OTOMATİK TESPİT
# ──────────────────────────────────────────────────────────
def detect_gpu_info() -> dict:
    """GPU varsa bilgilerini toplar, yoksa boş dict döndürür."""
    info = {"available": False, "name": "", "vram_gb": 0, "count": 0}
    try:
        import torch
        if torch.cuda.is_available():
            info["available"] = True
            info["count"] = torch.cuda.device_count()
            info["name"] = torch.cuda.get_device_name(0)
            try:
                free_vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                info["vram_gb"] = round(free_vram, 1)
            except:
                info["vram_gb"] = 0
    except ImportError:
        pass
    return info


def suggest_batch_size(vram_gb: float, base_batch: int = 4) -> tuple[int, int]:
    """VRAM'e göre batch_size ve grad_accum önerir."""
    if vram_gb >= 12:
        return 8, 2
    elif vram_gb >= 8:
        return 4, 4
    elif vram_gb >= 6:
        return 2, 8
    else:
        return base_batch, 4


# ──────────────────────────────────────────────────────────
# YAPILANDIRMA
# ──────────────────────────────────────────────────────────
@dataclass
class TrainingConfig:
    # Model
    model_name: str = "Qwen/Qwen3-1.7B"
    use_4bit: bool = True
    bnb_4bit_compute_dtype: str = "bfloat16"  # bf16 > fp16 > fp32
    bnb_4bit_quant_type: str = "nf4"          # nf4 > fp4
    use_double_quant: bool = True              # double quantization

    # LoRA
    lora_r: int = 16                           # rank
    lora_alpha: int = 32                       # scaling = alpha / r
    lora_dropout: float = 0.1
    lora_target_modules: list = field(
        default_factory=lambda: [
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ]
    )
    lora_bias: str = "none"                    # "none", "all", "lora_only"

    # Dataset
    data_file: str = "lora/q_a/qa_dataset.jsonl"  # JSONL format
    max_seq_length: int = 2048
    train_test_split: float = 0.9              # 90% train, 10% test
    num_workers: int = 4

    # Training
    output_dir: str = "lora/lora-out"
    num_epochs: int = 3
    per_device_train_batch_size: int = 4
    per_device_eval_batch_size: int = 4
    gradient_accumulation_steps: int = 4
    gradient_checkpointing: bool = True
    learning_rate: float = 2e-4
    lr_scheduler_type: str = "cosine"
    warmup_ratio: float = 0.03
    weight_decay: float = 0.01
    max_grad_norm: float = 0.3
    logging_steps: int = 5
    save_steps: int = 50
    eval_steps: int = 50
    save_total_limit: int = 3                  # sadece son 3 checkpoint
    load_best_model_at_end: bool = True
    metric_for_best_model: str = "eval_loss"
    greater_is_better: bool = False
    fp16: bool = False
    bf16: bool = True                          # Qwen3 bf16 ile eğitilmiş
    optim: str = "adamw_8bit"                  # 8-bit AdamW (bellek tasarrufu)
    seed: int = 42
    dataloader_pin_memory: bool = True         # GPU'ya veri aktarımını hızlandırır
    torch_compile: bool = True                 # torch.compile ile hız (GPU'da %15-25)
    ddp_find_unused_parameters: bool = False

    # Generation test
    do_test: bool = True
    test_prompts: list = field(
        default_factory=lambda: [
            "What is longitudinal stability in aircraft?",
            "Explain the concept of dihedral effect.",
        ]
    )

    # Unsloth
    use_unsloth: bool = False                  # True = UnslothTrainer kullan
    unsloth_max_seq_length: int = 2048

    # Resume
    resume_from_checkpoint: Optional[str] = None


# ──────────────────────────────────────────────────────────
# JSONL VERİ YÜKLEME (Unsloth uyumlu)
# ──────────────────────────────────────────────────────────
def load_qa_dataset_jsonl(filepath: str) -> list[dict]:
    """
    JSONL dosyasından Q&A verisini yükler.
    Format: her satır bir JSON obje, son satırda \n karakteri.
    
    Her örnek: { "question": ..., "answer": ..., "chapter_title": ..., "heading_title": ..., "chunk_path": ... }
    """
    fp = Path(filepath)
    if not fp.exists():
        log.error(f"❌ {filepath} bulunamadı. Önce lora1.py çalıştırın.")
        log.error(f"   Beklenen: {fp} (JSONL formatında)")
        sys.exit(1)

    # Dosya sonu \n kontrolü
    with open(fp, "rb") as f:
        raw = f.read()
    if not raw.endswith(b"\n"):
        log.warning(f"⚠ {fp.name}: dosya sonunda \\n yok! Unsloth hata verebilir.")
        log.warning(f"   Otomatik düzeltme yapılıyor...")
        # Otomatik düzelt
        with open(fp, "ab") as f:
            f.write(b"\n")
        log.warning(f"   ✅ \\n eklendi")

    dataset = []
    with open(fp, encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue  # boş satırları atla
            try:
                item = json.loads(line)
                # Doğrulama
                if "question" not in item or "answer" not in item:
                    log.warning(f"⚠ Satır {line_no}: eksik alan (question/answer), atlanıyor.")
                    continue
                if not item["question"].strip() or not item["answer"].strip():
                    log.warning(f"⚠ Satır {line_no}: boş içerik, atlanıyor.")
                    continue

                # LaTeX kontrolü
                if "$" not in item["answer"]:
                    log.warning(f"   ⚠ Satır {line_no}: cevapta LaTeX ($) yok!")

                dataset.append(item)
            except json.JSONDecodeError as e:
                log.warning(f"⚠ Satır {line_no}: JSON hatası -> {e}")
                continue

    log.info(f"📚 Yüklenen: {len(dataset)} QA çifti")

    # Cevap uzunluğu istatistiği
    if dataset:
        lengths = [len(d["answer"]) for d in dataset]
        log.info(f"   Cevap uzunluğu: avg={sum(lengths)//len(lengths)}, "
                 f"min={min(lengths)}, max={max(lengths)} karakter")
        latex_count = sum(1 for d in dataset if "$" in d["answer"])
        log.info(f"   LaTeX içeren: {latex_count}/{len(dataset)} ({100*latex_count//len(dataset)}%%)")

    return dataset


# ──────────────────────────────────────────────────────────
# VERİ FORMATLAMA (Qwen3 Chat Template)
# ──────────────────────────────────────────────────────────
def format_chat_template(example: dict, tokenizer) -> str:
    """
    Qwen3 chat template'ine göre formatlar:
    
    <|im_start|>system
    You are an expert aerospace engineering tutor. Answer questions about
    airplane stability and control with precise, technical explanations.
    <|im_end|>
    <|im_start|>user
    {question}
    <|im_end|>
    <|im_start|>assistant
    {answer}
    <|im_end|>
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert aerospace engineering tutor specializing in "
                "airplane stability and control. Answer questions with precise, "
                "technical explanations suitable for an undergraduate course."
            )
        },
        {"role": "user", "content": example["question"]},
        {"role": "assistant", "content": example["answer"]},
    ]
    return tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=False
    )


def preprocess_dataset(dataset: list[dict], tokenizer, max_length: int, split_ratio: float):
    """
    Dataset'i tokenize eder ve train/test olarak ayırır.
    """
    from datasets import Dataset

    # Chat template ile formatla
    texts = []
    for ex in dataset:
        try:
            text = format_chat_template(ex, tokenizer)
            texts.append(text)
        except Exception as e:
            log.warning(f"⚠ Formatlama hatası: {e}")
            continue

    log.info(f"✅ Formatlanan örnek: {len(texts)}")

    # Tokenize
    def tokenize_fn(examples):
        return tokenizer(
            examples["text"],
            truncation=True,
            max_length=max_length,
            padding=False,
            return_tensors=None,
        )

    raw_ds = Dataset.from_dict({"text": texts})
    tokenized_ds = raw_ds.map(
        tokenize_fn,
        batched=True,
        remove_columns=["text"],
        num_proc=4,
        desc="Tokenizing",
    )

    # Train/test split
    split_ds = tokenized_ds.train_test_split(
        test_size=1 - split_ratio, seed=42
    )
    log.info(f"📊 Train: {len(split_ds['train'])}  |  Test: {len(split_ds['test'])}")

    return split_ds


# ──────────────────────────────────────────────────────────
# MODEL YÜKLEME
# ──────────────────────────────────────────────────────────
def load_model_and_tokenizer(config: TrainingConfig):
    """
    Qwen3 modelini 4-bit QLoRA için yükler.
    """
    import torch
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
    )

    log.info(f"📦 Model yükleniyor: {config.model_name}")

    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        config.model_name,
        trust_remote_code=True,
        use_fast=True,
    )

    # Padding token ayarla (Qwen3'te genelde eos_token_id kullanılır)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.pad_token_id = tokenizer.eos_token_id

    # Quantization config (4-bit QLoRA)
    compute_dtype_map = {
        "float32": torch.float32,
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
    }
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=config.use_4bit,
        bnb_4bit_compute_dtype=compute_dtype_map.get(
            config.bnb_4bit_compute_dtype, torch.bfloat16
        ),
        bnb_4bit_quant_type=config.bnb_4bit_quant_type,
        bnb_4bit_use_double_quant=config.use_double_quant,
    )

    # Model
    model = AutoModelForCausalLM.from_pretrained(
        config.model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=compute_dtype_map.get(
            config.bnb_4bit_compute_dtype, torch.bfloat16
        ),
    )

    # Gradient checkpointing
    if config.gradient_checkpointing:
        model.gradient_checkpointing_enable()
        model.config.use_cache = False

    # GPU info
    gpu = detect_gpu_info()
    # GPU bilgisi
    if gpu["available"]:
        log.info(f"🎮 GPU: {gpu['name']} ({gpu['vram_gb']}GB VRAM, {gpu['count']} adet)")
    else:
        log.info(f"💻 GPU bulunamadı, CPU'da çalışıyor (çok yavaş olacak, GPU önerilir)")

    # ── Unsloth kullan (isteğe bağlı, deneysel) ──
    if config.use_unsloth:
        try:
            from unsloth import FastLanguageModel
            log.info("⚡ Unsloth kullanılıyor...")
            model, tokenizer = FastLanguageModel.from_pretrained(
                model_name=config.model_name,
                max_seq_length=config.unsloth_max_seq_length,
                dtype=compute_dtype_map.get(config.bnb_4bit_compute_dtype, torch.bfloat16),
                load_in_4bit=config.use_4bit,
                device_map="auto",
            )
            log.info(f"✅ Unsloth model yüklendi: {model}")
            return model, tokenizer
        except ImportError:
            log.warning("⚠ Unsloth kurulu değil, standart transformers kullanılıyor.")
            log.warning("   Kurmak için: uv add unsloth")
        except Exception as e:
            log.warning(f"⚠ Unsloth yükleme hatası: {e}, standart yol kullanılıyor.")

    log.info(f"✅ Model yüklendi: {model.num_parameters():,} parametre")

    return model, tokenizer


# ──────────────────────────────────────────────────────────
# LORA KONFİGÜRASYONU
# ──────────────────────────────────────────────────────────
def setup_lora(model, config: TrainingConfig):
    """
    Qwen3'e LoRA adapter'ı ekler.
    """
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

    log.info("🔧 LoRA adapter hazırlanıyor...")

    # k-bit training için modeli hazırla
    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        target_modules=config.lora_target_modules,
        lora_dropout=config.lora_dropout,
        bias=config.lora_bias,
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, lora_config)

    # Trainable parametreleri yazdır
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())

    log.info(f"📐 LoRA yapılandırması:")
    log.info(f"   - Rank (r):            {config.lora_r}")
    log.info(f"   - Alpha:               {config.lora_alpha}")
    log.info(f"   - Dropout:             {config.lora_dropout}")
    log.info(f"   - Target modules:      {len(config.lora_target_modules)} adet")
    log.info(f"   - Trainable params:    {trainable_params:,} ({100 * trainable_params / total_params:.2f}%)")
    log.info(f"   - Total params:        {total_params:,}")

    return model


# ──────────────────────────────────────────────────────────
# DATA COLLATOR (daha hızlı eğitim için)
# ──────────────────────────────────────────────────────────
def create_data_collator(tokenizer):
    """
    Padding yapmayan data collator - dinamik padding ile daha hızlı.
    """
    from transformers import DataCollatorForLanguageModeling

    return DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # Causal LM, masked LM değil
    )


# ──────────────────────────────────────────────────────────
# EĞİTİM
# ──────────────────────────────────────────────────────────
def train(config: TrainingConfig):
    """
    Ana eğitim döngüsü.
    """
    import torch
    from transformers import (
        TrainingArguments,
        Trainer,
        EarlyStoppingCallback,
    )

    # 1. Veriyi yükle
    log.info("=" * 60)
    log.info("📂 VERİ YÜKLENİYOR (JSONL)")
    dataset_raw = load_qa_dataset_jsonl(config.data_file)
    log.info(f"   Toplam: {len(dataset_raw)} QA çifti")
    if len(dataset_raw) < 500:
        log.warning(f"   ⚠ En az 500 örnek önerilir. Mevcut: {len(dataset_raw)} — lora1.py ile artırın")

    # 2. Model + tokenizer
    model, tokenizer = load_model_and_tokenizer(config)

    # 3. Dataset'i formatla ve tokenize et
    log.info("\n📝 VERİ FORMATLANIYOR")
    split_ds = preprocess_dataset(
        dataset_raw, tokenizer, config.max_seq_length, config.train_test_split
    )

    # 4. LoRA adapter
    log.info("")
    # Unsloth zaten kendi LoRA setup'ını yapar; tekrar uygulama
    if config.use_unsloth:
        log.info("🔧 Unsloth: LoRA zaten model içinde, PEFT setup atlanıyor.")
    else:
        model = setup_lora(model, config)

    # ⚡ torch.compile — LoRA sonrası uygulanmalı! (önce olursa derlenmiş graf bozulur)
    if config.torch_compile and gpu["available"]:
        try:
            log.info("⚡ torch.compile uygulanıyor...")
            import torch
            model = torch.compile(model)
            log.info("✅ torch.compile aktif")
        except Exception as e:
            log.warning(f"⚠ torch.compile başarısız: {e}")

    # 5. Training arguments
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # VRAM'e göre batch size öner
    gpu = detect_gpu_info()
    if gpu["available"] and gpu["vram_gb"] > 0:
        suggested_batch, suggested_grad = suggest_batch_size(gpu["vram_gb"])
        if config.per_device_train_batch_size > suggested_batch:
            log.warning(f"⚠ Düşük VRAM ({gpu['vram_gb']}GB): batch_size={suggested_batch} önerilir")
            log.warning(f"  (şu an: {config.per_device_train_batch_size}, grad_accum={config.gradient_accumulation_steps})")

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=config.num_epochs,
        per_device_train_batch_size=config.per_device_train_batch_size,
        per_device_eval_batch_size=config.per_device_eval_batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        gradient_checkpointing=config.gradient_checkpointing,
        learning_rate=config.learning_rate,
        lr_scheduler_type=config.lr_scheduler_type,
        warmup_ratio=config.warmup_ratio,
        weight_decay=config.weight_decay,
        max_grad_norm=config.max_grad_norm,
        logging_steps=config.logging_steps,
        save_steps=config.save_steps,
        eval_steps=config.eval_steps,
        save_total_limit=config.save_total_limit,
        load_best_model_at_end=config.load_best_model_at_end,
        metric_for_best_model=config.metric_for_best_model,
        greater_is_better=config.greater_is_better,
        fp16=config.fp16,
        bf16=config.bf16,
        optim=config.optim,
        seed=config.seed,
        evaluation_strategy="steps",
        logging_strategy="steps",
        save_strategy="steps",
        report_to="none",
        ddp_find_unused_parameters=config.ddp_find_unused_parameters,
        remove_unused_columns=True,
        dataloader_num_workers=config.num_workers,
        dataloader_pin_memory=config.dataloader_pin_memory and gpu["available"],
    )

    # 6. Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=split_ds["train"],
        eval_dataset=split_ds["test"],
        tokenizer=tokenizer,
        data_collator=create_data_collator(tokenizer),
        callbacks=[
            EarlyStoppingCallback(early_stopping_patience=5),
        ],
    )

    # 7. Eğitim
    log.info("\n" + "=" * 60)
    log.info("🚀 EĞİTİM BAŞLIYOR")
    log.info(f"   Epochs:      {config.num_epochs}")
    log.info(f"   Batch size:  {config.per_device_train_batch_size} × {config.gradient_accumulation_steps} (grad acc)")
    log.info(f"   LR:          {config.learning_rate}")
    log.info(f"   Scheduler:   {config.lr_scheduler_type}")
    log.info(f"   Warmup:      {config.warmup_ratio:.0%}")
    log.info(f"   Optimizer:   {config.optim}")
    log.info(f"   LoRA rank:   {config.lora_r}")
    log.info(f"   Precision:   {'bf16' if config.bf16 else 'fp16' if config.fp16 else 'fp32'}")
    log.info(f"   GPU:         {'✅ ' + gpu['name'] if gpu['available'] else '❌ CPU (çok yavaş)'}")
    if gpu["available"]:
        log.info(f"   VRAM:        {gpu['vram_gb']}GB ({gpu['count']} adet)")
    log.info(f"   torch.compile: {'✅' if config.torch_compile and gpu['available'] else '—'}")
    log.info("=" * 60)

    train_result = trainer.train(resume_from_checkpoint=config.resume_from_checkpoint)

    # 8. Metrikleri kaydet
    metrics = train_result.metrics
    log.info(f"\n📊 EĞİTİM METRİKLERİ:")
    log.info(f"   Train Loss:        {metrics.get('train_loss', 'N/A'):.4f}")
    log.info(f"   Train Runtime:     {metrics.get('train_runtime', 'N/A'):.1f}s")
    log.info(f"   Train Samples/sec: {metrics.get('train_samples_per_second', 'N/A'):.2f}")
    log.info(f"   Eval Loss:         {metrics.get('eval_loss', 'N/A'):.4f}")

    # 9. Modeli kaydet
    final_path = output_dir / "final"
    trainer.save_model(str(final_path))
    tokenizer.save_pretrained(str(final_path))
    log.info(f"\n💾 LoRA adapter kaydedildi: {final_path}")

    # 10. Test generation
    if config.do_test:
        log.info("\n🧪 TEST GENERATION")
        test_generation(model, tokenizer, config)

    log.info("\n✅ Eğitim tamamlandı!")
    return model, tokenizer


# ──────────────────────────────────────────────────────────
# GENERATION TEST
# ──────────────────────────────────────────────────────────
def test_generation(model, tokenizer, config: TrainingConfig):
    """Eğitilmiş model ile birkaç örnek soru cevapla."""
    import torch

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Model'i eval moduna al
    model.eval()

    for prompt in config.test_prompts:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert aerospace engineering tutor specializing in "
                    "airplane stability and control."
                )
            },
            {"role": "user", "content": prompt},
        ]
        formatted = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        inputs = tokenizer(formatted, return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
            )

        response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
        log.info(f"\n   Q: {prompt}")
        log.info(f"   A: {response[:300]}")


# ──────────────────────────────────────────────────────────
# SADECE DEĞERLENDİRME
# ──────────────────────────────────────────────────────────
def evaluate_only(config: TrainingConfig, adapter_path: str):
    """
    Önceden eğitilmiş LoRA adapter'ını yükler ve değerlendirir.
    """
    import torch
    from peft import PeftModel

    log.info("📂 Değerlendirme modu")

    # Base model + tokenizer
    model, tokenizer = load_model_and_tokenizer(config)

    # LoRA adapter'ını yükle
    log.info(f"🔧 Adapter yükleniyor: {adapter_path}")
    model = PeftModel.from_pretrained(model, adapter_path)
    model.eval()

    # Test generation
    test_generation(model, tokenizer, config)

    log.info("✅ Değerlendirme tamamlandı.")


# ──────────────────────────────────────────────────────────
# MERGE ADAPTER (opsiyonel)
# ──────────────────────────────────────────────────────────
def merge_and_save(config: TrainingConfig, adapter_path: str, output_path: str):
    """
    LoRA adapter'ını base model ile birleştirip kaydeder.
    """
    import torch
    from peft import PeftModel

    log.info("🔗 Adapter merge ediliyor...")

    model, tokenizer = load_model_and_tokenizer(config)
    model = PeftModel.from_pretrained(model, adapter_path)
    merged = model.merge_and_unload()

    Path(output_path).mkdir(parents=True, exist_ok=True)
    merged.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)

    log.info(f"✅ Merge edilen model kaydedildi: {output_path}")
    return merged, tokenizer


# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Qwen3:1.7B'yi LoRA ile fine-tune et."
    )

    # Training
    parser.add_argument("--num_epochs", type=int, default=3)
    parser.add_argument("--lr", "--learning_rate", type=float, default=2e-4, dest="learning_rate")
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--grad_accum", type=int, default=4)
    parser.add_argument("--lora_r", type=int, default=16)
    parser.add_argument("--lora_alpha", type=int, default=32)
    parser.add_argument("--max_seq_length", type=int, default=2048)

    # Model
    parser.add_argument("--model_name", type=str, default="Qwen/Qwen3-1.7B")
    parser.add_argument("--use_4bit", action="store_true", default=True)
    parser.add_argument("--no_4bit", dest="use_4bit", action="store_false")

    # Checkpoint
    parser.add_argument("--resume_from_checkpoint", type=str, default=None)
    parser.add_argument("--output_dir", type=str, default="lora/lora-out")

    # Unsloth
    parser.add_argument("--use_unsloth", action="store_true",
                        help="Unsloth ile eğitim (daha hızlı, az bellek)")

    # Validate
    parser.add_argument("--validate", action="store_true",
                        help="Dataset kalite kontrolü yap (eğitim yapmaz)")

    # Eval only
    parser.add_argument("--eval_only", action="store_true")
    parser.add_argument("--adapter_path", type=str, default=None)

    # Merge
    parser.add_argument("--merge", action="store_true")
    parser.add_argument("--merge_output", type=str, default="lora/lora-merged")

    args = parser.parse_args()

    # Config
    config = TrainingConfig(
        num_epochs=args.num_epochs,
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        lora_r=args.lora_r,
        lora_alpha=args.lora_alpha,
        max_seq_length=args.max_seq_length,
        model_name=args.model_name,
        use_4bit=args.use_4bit,
        output_dir=args.output_dir,
        resume_from_checkpoint=args.resume_from_checkpoint,
        use_unsloth=args.use_unsloth,
    )

    # ── Validate modu ──
    if args.validate:
        log.info("=" * 60)
        log.info("🔍 DATASET VALIDASYONU")
        log.info("=" * 60)
        dataset = load_qa_dataset_jsonl(config.data_file)
        log.info(f"\n📊 RAPOR:")
        log.info(f"   Toplam örnek:      {len(dataset)}")
        if dataset:
            lengths = [len(d["answer"]) for d in dataset]
            latex_count = sum(1 for d in dataset if "$" in d["answer"])
            log.info(f"   Ort. cevap:        {sum(lengths)//len(lengths)} karakter")
            log.info(f"   Min/Max:           {min(lengths)} / {max(lengths)}")
            log.info(f"   LaTeX içeren:      {latex_count}/{len(dataset)} ({100*latex_count//len(dataset)}%%)")
            log.info(f"   Eksik $ olan:      {len(dataset) - latex_count}")
        log.info(f"\n{'='*60}")
        return

    # ── Merge modu ──
    if args.merge:
        adapter_path = args.adapter_path or (Path(config.output_dir) / "final")
        merge_and_save(config, str(adapter_path), args.merge_output)
        return

    # ── Eval modu ──
    if args.eval_only:
        adapter_path = args.adapter_path or (Path(config.output_dir) / "final")
        evaluate_only(config, str(adapter_path))
        return

    # ── Eğitim ──
    train(config)


if __name__ == "__main__":
    main()
