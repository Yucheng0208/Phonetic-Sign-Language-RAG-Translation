#!/usr/bin/env python3
"""
從影片擷取 MediaPipe Holistic 手部關鍵點，輸出 JSON 供 CNN+LSTM 訓練。

用法：
  python ml/extract_features.py --input data/raw/demo.mp4 --output ml/dataset/features/demo.json
  python ml/extract_features.py --input data/raw/frames/ --output ml/dataset/features/
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np

# 每幀：左手 21*3 + 右手 21*3 = 126 維（僅 xyz，未含 visibility）
HAND_LANDMARK_COUNT = 21
COORDS_PER_POINT = 3


def _landmarks_to_array(landmarks) -> list[float]:
    if landmarks is None:
        return [0.0] * (HAND_LANDMARK_COUNT * COORDS_PER_POINT)
    out: list[float] = []
    for lm in landmarks.landmark:
        out.extend([lm.x, lm.y, lm.z])
    return out


def extract_from_video(video_path: Path) -> dict:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"無法開啟影片：{video_path}")

    holistic = mp.solutions.holistic.Holistic(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    frames: list[list[float]] = []
    frame_idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = holistic.process(rgb)
        left = _landmarks_to_array(result.left_hand_landmarks)
        right = _landmarks_to_array(result.right_hand_landmarks)
        frames.append(left + right)
        frame_idx += 1

    cap.release()
    holistic.close()

    return {
        "source": str(video_path),
        "frame_count": frame_idx,
        "feature_dim": len(frames[0]) if frames else 0,
        "frames": frames,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="MediaPipe 手語關鍵點擷取")
    parser.add_argument("--input", type=Path, required=True, help="影片檔或影像目錄")
    parser.add_argument("--output", type=Path, required=True, help="輸出 JSON 檔或目錄")
    args = parser.parse_args()

    inputs: list[Path] = []
    if args.input.is_dir():
        inputs = sorted(
            p
            for p in args.input.iterdir()
            if p.suffix.lower() in {".mp4", ".mov", ".avi", ".mkv"}
        )
    else:
        inputs = [args.input]

    if not inputs:
        raise SystemExit(f"找不到可處理的影片：{args.input}")

    args.output.mkdir(parents=True, exist_ok=True)

    for video in inputs:
        data = extract_from_video(video)
        if args.output.is_dir():
            out_file = args.output / f"{video.stem}.json"
        else:
            out_file = args.output
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        print(f"✓ {video.name} → {out_file} ({data['frame_count']} frames)")


if __name__ == "__main__":
    main()
