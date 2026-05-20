# Work Plan / 工作計畫表

## Milestones / 里程碑

| Phase | Goal / 目標 | Status / 狀態 |
|-------|---------------|---------------|
| M0 | Repo scaffold, README, corpus format / 骨架與詞庫格式 | Done / 完成 |
| M1 | MediaPipe feature pipeline / 特徵管線 | Pending / 待辦 |
| M2 | CNN+LSTM Zhuyin recognition / 注音辨識 | Pending / 待辦 |
| M3 | Hybrid RAG (BM25 + n-gram) / 雙支幹 RAG | Prototype done / 原型完成 |
| M4 | Gemini sentence + multilingual / 組句與多語 | Prototype (mock OK) / 原型完成 |
| M5 | Frontend streaming + RWD / 即時串流與響應式 | Prototype done / 原型完成 |

## Tasks This Week / 本週可執行

- [ ] Collect and label Zhuyin sign videos or keypoint sequences / 收集與標註影片或關鍵點
- [ ] Expand `data/zhuyin_corpus/` / 擴充詞庫
- [ ] Complete MediaPipe → features → training scripts in `ml/` / 完善 ML 管線
- [ ] Send keypoints or frames from frontend to recognition API / 前端串接辨識 API

## Evaluation Metrics (thesis) / 實驗指標（論文用）

- Recognition / 辨識：syllable accuracy, CER / 音節準確率、CER
- RAG / 檢索：homophone Top-1 / Top-3, MRR
- System / 系統：end-to-end latency (ms) / 端到端延遲
