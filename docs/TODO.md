# Developer TODO / 開發者待辦（技術細節）

> Action checklist for you / 個人待辦清單 → **[../TODO.md](../TODO.md)**

This file tracks dependencies, item IDs, and tasks assignable to AI or developers.  
本檔記錄依賴關係、編號與可指派開發任務。

---

## Blocked on User Input / 需使用者提供

| # | Item / 項目 | Blocks / 阻塞 |
|---|-------------|---------------|
| 1 | Gemini API Key | Real LLM translation / 真實 LLM 翻譯 |
| 4–5 | Videos + `labels.csv` | CNN+LSTM training / 模型訓練 |
| 6 | MOE common word list / 教育部詞表 | RAG coverage / 詞庫覆蓋率 |
| 7 | `homophone_pairs.json` | RAG experiment metrics / 實驗數據 |
| 9 | GPU | Local training speed / 本機訓練速度 |

---

## Continuable Development / 可接續開發（AI / developer）

| ID | Task / 任務 | Depends on / 依賴 |
|----|-------------|-------------------|
| A | Batch-import MOE lexicon / 批次匯入教育部詞表 | #6 |
| B | Implement `train_cnn_lstm.py` | #4, #5 |
| C | Backend PyTorch inference / 後端推論 | B |
| D | Frontend sends keypoints → `/api/recognize` | C |
| E | bge-m3 + ChromaDB | — |
| F | `eval_rag.py` report output / 評估報告 | #7 |
| G | Docker Compose | hosting account / 部署帳號 |

---

## File Layout / 檔案約定

See [../TODO.md](../TODO.md) and `data/zhuyin_corpus/README.md`.
