#!/usr/bin/env python3
"""results klasöründeki tüm JSON dosyalarından question_score değerlerini toplar."""

import json
import os
import glob

RESULTS_DIR = "results"


def main():
    json_files = sorted(glob.glob(os.path.join(RESULTS_DIR, "*.json")))

    if not json_files:
        print(f"'{RESULTS_DIR}' klasöründe JSON dosyası bulunamadı.")
        return

    total = 0
    scores = {}

    for filepath in json_files:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        score = data.get("question_score", 0)
        basename = os.path.basename(filepath)
        scores[basename] = score
        total += score

    print(f"{'Dosya':<20} {'question_score':>15}")
    print("-" * 37)
    for name, score in scores.items():
        print(f"{name:<20} {score:>15}")
    print("-" * 37)
    print(f"{'TOPLAM':<20} {total:>15}")


if __name__ == "__main__":
    main()
