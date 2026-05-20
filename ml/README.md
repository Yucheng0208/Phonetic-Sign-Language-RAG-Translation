# Machine Learning Pipeline / 機器學習管線

## 1. Install / 安裝

```bash
pip install -r ml/requirements.txt
```

## 2. Extract keypoints / 擷取關鍵點

Place videos in `data/raw/`, then run:  
將影片放於 `data/raw/` 後執行：

```bash
python ml/extract_features.py \
  --input data/raw/your_clip.mp4 \
  --output ml/dataset/features/your_clip.json
```

## 3. Labels / 標註

Copy `ml/dataset/labels.csv.example` → `labels.csv` with columns `filename,zhuyin,text`.

## 4. Train (pending implementation) / 訓練（待實作）

```bash
python ml/train_cnn_lstm.py --epochs 50
```

Weights output / 權重輸出：`ml/checkpoints/cnn_lstm.pt`  
Backend `/api/health` will report `model_loaded: true` when present.

## Layout / 目錄

```
ml/
├── extract_features.py
├── train_cnn_lstm.py
├── dataset/
│   ├── features/     # keypoint JSON / 關鍵點 JSON
│   └── labels.csv
└── checkpoints/
```
