#!/usr/bin/env python3
"""
Tüm değerlendirme klasörlerindeki JSON dosyalarından
question_score değerlerini toplar ve özetler.

Klasörler:
    results/           - base model değerlendirme
    results-lora/      - LoRA fine-tuned model değerlendirme
    results-rag/       - RAG pipeline değerlendirme
    results-graphrag/  - GraphRAG pipeline değerlendirme
"""

import json
import os
import sys
from pathlib import Path

# Değerlendirilecek klasörler
RESULT_DIRS = [
    ("results",          "Base Model"),
    ("results-lora",     "LoRA Fine-tuned"),
    ("results-rag",      "RAG Pipeline"),
    ("results-graphrag", "GraphRAG Pipeline"),
]

SEPARATOR = "─" * 70


def evaluate_dir(dir_name: str, label: str) -> dict | None:
    """Bir klasördeki tüm JSON'ları okur, question_score toplamı döndürür."""
    dir_path = Path(dir_name)

    if not dir_path.exists():
        return None  # klasör yok

    json_files = sorted(dir_path.glob("*.json"))
    if not json_files:
        return None  # klasör var ama içi boş

    scores = {}
    total = 0

    for fp in json_files:
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
        score = data.get("question_score", 0)
        scores[fp.name] = score
        total += score

    return {
        "label": label,
        "dir": str(dir_path),
        "files": scores,
        "total": total,
        "count": len(scores),
    }


def main():
    results = []

    for dir_name, label in RESULT_DIRS:
        result = evaluate_dir(dir_name, label)
        results.append((dir_name, label, result))

    total_overall = 0
    total_dirs = 0

    print()
    print(" Airplane Stability & Control — Değerlendirme Özeti ".center(70, "="))
    print()

    for dir_name, label, result in results:
        print(f" [{label}]")

        if result is None:
            print(f"   📭 {dir_name}/ bulunamadı — henüz değerlendirme yapılmamış.")
            print()
            continue

        files = result["files"]
        print(f"   {SEPARATOR}")
        print(f"   {'Dosya':<25} {'question_score':>15}")
        print(f"   {SEPARATOR}")
        for name, score in files.items():
            print(f"   {name:<25} {score:>15}")
        print(f"   {SEPARATOR}")
        print(f"   {'Toplam (' + str(result['count']) + ' soru)':<25} {result['total']:>15}")
        print()

        total_overall += result["total"]
        total_dirs += 1

    # Genel toplam
    if total_dirs > 0:
        print(f" {'GENEL TOPLAM':-^70}")
        print(f" {'Toplam':<25} {total_overall:>15}")
        print("=" * 72)
    else:
        print("-" * 72)
        print("  Hiçbir değerlendirme klasörü bulunamadı. Önce pipeline'ları çalıştırın.")
        print("-" * 72)

    print()


if __name__ == "__main__":
    main()
