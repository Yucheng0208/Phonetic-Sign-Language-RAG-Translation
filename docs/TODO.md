# 專題開發 TODO 清單

> 更新日期：2026-05-20  
> 圖例：🔴 需你提供／決策 · 🟡 進行中 · 🟢 已完成 · ⚪ 待排程

---

## 一、需要你提供或決策（🔴）

### 帳號與 API

| # | 項目 | 說明 | 狀態 |
|---|------|------|------|
| 1 | **Gemini API Key** | 至 [Google AI Studio](https://aistudio.google.com/apikey) 申請，填入專案根目錄 `.env` 的 `GEMINI_API_KEY` | 🔴 |
| 2 | **部署平台帳號** | 後端需 Render / Railway / VPS 其一（GitHub Pages **無法**跑 FastAPI） | 🔴 |
| 3 | **GitHub Pages** | 若要用 gh-pages 部署前端，確認 repo Settings → Pages 已啟用 | 🔴 |

### 資料（論文／模型核心）

| # | 項目 | 說明 | 建議格式 | 狀態 |
|---|------|------|----------|------|
| 4 | **注音手語影片** | 每人每字／每詞 20+ 次，光線、背景盡量一致 | `.mp4` 或影像幀資料夾 | 🔴 |
| 5 | **標註對照表** | 影片檔名 ↔ 注音序列 ↔ 中文 gloss | CSV：`filename,zhuyin,text` | 🔴 |
| 6 | **教育部常用詞表** | 下載後放到 `data/raw/`，或提供下載連結 | CSV / TXT | 🔴 |
| 7 | **同音消歧測試集** | 至少 30 組「同注音、不同義」句對，供 RAG 實驗 | `data/eval/homophone_pairs.json` | 🔴 |
| 8 | **注音標籤表** | 37 符 + 5 聲調完整列表（若學校有規範版請提供） | JSON 或 PDF | 🔴 |

### 硬體與環境

| # | 項目 | 說明 | 狀態 |
|---|------|------|------|
| 9 | **訓練用 GPU** | CNN+LSTM 建議 Colab、學校 GPU 或本機 NVIDIA | 🔴 |
| 10 | **瀏覽器測試** | Chrome / Safari 各一台（攝影機、WebSocket） | 🔴 |

### 論文／專題行政

| # | 項目 | 說明 | 狀態 |
|---|------|------|------|
| 11 | **指導教授確認題目** | 中英文題目、投稿／口試日期 | 🔴 |
| 12 | **倫理／受試者** | 若錄製他人手語需同意書範本 | 🔴 |

---

## 二、Repo 內已完成（🟢）

- [x] Monorepo 骨架（`backend/`、`frontend/`、`ml/`、`data/`）
- [x] FastAPI：`/api/health`、`/api/translate`、`/api/rag/search`、`/api/recognize`（stub）
- [x] WebSocket：`/ws/translate`
- [x] RAG 雙支幹（BM25 + 注音 n-gram）
- [x] Gemini 整合（無 key 時 mock）
- [x] React 前端：攝影機、語言 Swiper、示範注音、一鍵辨識演示
- [x] 詞庫多檔載入、`scripts/import_corpus.py` 匯入工具
- [x] MediaPipe 特徵擷取腳本 `ml/extract_features.py`

---

## 三、進行中／下一步（🟡 → 可指派給 AI 繼續）

| # | 任務 | 依賴 | 優先級 |
|---|------|------|--------|
| A | 匯入教育部詞表 → `data/zhuyin_corpus/` | 🔴 #6 | 高 |
| B | `ml/train_cnn_lstm.py` 訓練腳本骨架 | 🔴 #4 #5 | 高 |
| C | 後端載入 `.pt` 模型真實推論 | B | 高 |
| D | 前端送關鍵點序列至 `/api/recognize` | C | 中 |
| E | RAG 升級 bge-m3 + ChromaDB | 無 | 中 |
| F | 同音測試集自動評估腳本 | 🔴 #7 | 中 |
| G | Docker Compose 一鍵部署 | 🔴 #2 | 低 |
| H | Zerotier 私有 LLM（Bonus） | 自架模型 | 低 |

---

## 四、你可立即執行的指令

```bash
# 1. 環境
cp .env.example .env          # 填入 GEMINI_API_KEY

# 2. 啟動
./scripts/dev.sh

# 3. 新增詞庫條目
python scripts/import_corpus.py --zhuyin "ㄨㄛˇ ㄞˋ ㄋㄧˇ" --text "我愛你" --tags 情感

# 4. 從影片擷取 MediaPipe 關鍵點（需先 pip install -r ml/requirements.txt）
python ml/extract_features.py --input data/raw/your_video.mp4 --output ml/dataset/features/
```

---

## 五、檔案放置約定

```
data/
├── raw/                    # 你提供的原始影片、教育部詞表（勿提交大型檔至 git）
├── zhuyin_corpus/*.json    # RAG 詞庫（可提交）
└── eval/                   # 實驗用測試集

ml/
├── dataset/features/       # extract_features.py 輸出
└── checkpoints/            # 訓練好的 .pt（可 .gitignore）
```

---

## 六、完成定義（MVP Demo）

- [ ] 鏡頭前比劃 → 輸出注音（模型或演示模式）
- [ ] 同音詞 RAG Top-3 正確率可報告
- [ ] 中文句子 + 至少 2 種外語翻譯
- [ ] 論文用延遲數據（端到端 ms）截圖 1 張

---

有資料或 API key 後，在 issue 或對話中標註編號（例如「#6 詞表已放 data/raw」），即可接續開發對應項目。
