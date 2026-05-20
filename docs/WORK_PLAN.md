# 工作計畫表

## 里程碑

| 階段 | 目標 | 狀態 |
|------|------|------|
| M0 | Repo 骨架、README、詞庫格式 | 完成 |
| M1 | MediaPipe 特徵管線 | 待辦 |
| M2 | CNN+LSTM 注音辨識 | 待辦 |
| M3 | RAG 雙支幹（BM25 + n-gram embedding） | 原型完成 |
| M4 | Gemini 組句與多語翻譯 | 原型完成（可 mock） |
| M5 | 前端即時串流與 RWD | 原型完成 |

## 本週可執行任務

- [ ] 收集 / 標註注音手語影片或關鍵點序列
- [ ] 擴充 `data/zhuyin_corpus/` 詞庫
- [ ] 在 `ml/` 建立 MediaPipe → 特徵 → 訓練腳本
- [ ] 將前端改為送關鍵點或影像幀至後端辨識 API

## 實驗指標（論文用）

- 辨識：音節準確率、CER
- RAG：同音句 Top-1 / Top-3、MRR
- 系統：端到端延遲（ms）
