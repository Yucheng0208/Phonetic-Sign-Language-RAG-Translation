#!/usr/bin/env python3
"""RAG Top-k 評估（需 data/eval/homophone_pairs.json）。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.services.pipeline import run_rag_search  # noqa: E402

EVAL_FILE = ROOT / "data" / "eval" / "homophone_pairs.json"


def main() -> int:
    if not EVAL_FILE.exists():
        print(f"❌ 請建立 {EVAL_FILE}")
        print("   可複製 homophone_pairs.template.json 開始填寫")
        return 1

    pairs = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
    top1 = top3 = 0
    for item in pairs:
        zhuyin = item["zhuyin"]
        correct = item["correct"]
        result = run_rag_search(zhuyin, top_k=5)
        texts = [c.text for c in result.candidates]
        if texts and texts[0] == correct:
            top1 += 1
        if correct in texts[:3]:
            top3 += 1

    n = len(pairs)
    print(f"樣本數: {n}")
    print(f"Top-1: {top1}/{n} ({100 * top1 / n:.1f}%)")
    print(f"Top-3: {top3}/{n} ({100 * top3 / n:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
