#!/usr/bin/env python3
"""
CNN+LSTM 訓練骨架（需標註資料後執行）。

預期資料：
  ml/dataset/features/*.json   # extract_features.py 輸出
  ml/dataset/labels.csv        # filename,zhuyin,text

完成訓練後將權重存至 ml/checkpoints/cnn_lstm.pt，後端會自動偵測。
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURES_DIR = ROOT / "ml" / "dataset" / "features"
LABELS_CSV = ROOT / "ml" / "dataset" / "labels.csv"
CHECKPOINT = ROOT / "ml" / "checkpoints" / "cnn_lstm.pt"


def main() -> None:
    parser = argparse.ArgumentParser(description="CNN+LSTM 訓練（骨架）")
    parser.add_argument("--epochs", type=int, default=50)
    args = parser.parse_args()

    if not LABELS_CSV.exists():
        print("❌ 缺少標註檔：ml/dataset/labels.csv")
        print("   格式：filename,zhuyin,text")
        print("   範例：demo.json,ㄋㄧˇ ㄏㄠˇ,你好")
        return 1

    labels = list(csv.DictReader(LABELS_CSV.open(encoding="utf-8")))
    feature_files = list(FEATURES_DIR.glob("*.json"))
    print(f"標註 {len(labels)} 筆 · 特徵檔 {len(feature_files)} 個")

    if not feature_files:
        print("❌ 尚無特徵檔，請先執行：")
        print("   python ml/extract_features.py --input data/raw/xxx.mp4 --output ml/dataset/features/")
        return 1

    print(f"⚠️  訓練程式尚未實作（epochs={args.epochs}）")
    print(f"   完成後請輸出：{CHECKPOINT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
