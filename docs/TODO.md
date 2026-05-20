# 開發者 TODO（技術細節）

> **給你的行動清單**請看專案根目錄 → **[../TODO.md](../TODO.md)**

本檔記錄依賴關係、API 編號與可指派給 AI 的開發任務。

---

## 需使用者提供（🔴）

| # | 項目 | 阻塞 |
|---|------|------|
| 1 | Gemini API Key | LLM 真實翻譯 |
| 4–5 | 影片 + labels.csv | CNN+LSTM 訓練 |
| 6 | 教育部詞表 | RAG 覆蓋率 |
| 7 | homophone_pairs.json | RAG 實驗數據 |
| 9 | GPU | 本機訓練速度 |

---

## 可接續開發（AI / 開發者）

| ID | 任務 | 依賴 |
|----|------|------|
| A | 批次匯入教育部詞表 | #6 |
| B | 實作 `train_cnn_lstm.py` | #4 #5 |
| C | 後端 PyTorch 推論 | B |
| D | 前端送 keypoints → `/api/recognize` | C |
| E | bge-m3 + ChromaDB | — |
| F | `eval_rag.py` 報告產出 | #7 |
| G | Docker Compose | 部署帳號 |

---

## 檔案約定

見 [../TODO.md](../TODO.md) 與 `data/zhuyin_corpus/README.md`。
