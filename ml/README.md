# 機器學習管線

## 1. 安裝

```bash
pip install -r ml/requirements.txt
```

## 2. 擷取關鍵點

將影片放於 `data/raw/`，執行：

```bash
python ml/extract_features.py \
  --input data/raw/your_clip.mp4 \
  --output ml/dataset/features/your_clip.json
```

## 3. 標註

複製 `ml/dataset/labels.csv.example` → `labels.csv`，填寫 `filename,zhuyin,text`。

## 4. 訓練（待實作）

```bash
python ml/train_cnn_lstm.py --epochs 50
```

權重輸出：`ml/checkpoints/cnn_lstm.pt`（後端 `/api/health` 的 `model_loaded` 會變 true）

## 目錄

```
ml/
├── extract_features.py
├── train_cnn_lstm.py
├── dataset/
│   ├── features/     # JSON 關鍵點
│   └── labels.csv
└── checkpoints/
```
