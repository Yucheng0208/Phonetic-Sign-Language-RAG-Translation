# Project TODO / 專題待辦清單

> **Phonetic Sign Translator / 注手快譯通** · Last updated / 最後更新：2026-05-20  
> Check `[x]` when done / 完成請勾選。Technical tasks / 技術任務見 [docs/TODO.md](./docs/TODO.md)。

---

## Top Priority This Week / 本週最優先（5 items）

- [ ] **1. Apply for Gemini API Key / 申請 Gemini API Key**  
  → [Google AI Studio](https://aistudio.google.com/apikey)  
  → Add to `.env`: `GEMINI_API_KEY=your_key`

- [ ] **2. Run locally and verify / 本機啟動驗證**  
  ```bash
  cp .env.example .env
  ./scripts/dev.sh
  ```  
  → Open http://localhost:5173 → click **Center (homophone demo) / 中心（同音演示）** to test RAG + translation

- [ ] **3. Record Zhuyin sign videos / 錄製注音手語影片**  
  → Save under `data/raw/` (20+ repetitions per sign/word, stable lighting and simple background / 每詞至少 20 次，光線與背景固定)

- [ ] **4. Create label file / 建立標註表**  
  → Copy `ml/dataset/labels.csv.example` → `ml/dataset/labels.csv`  
  → Columns / 欄位：`filename,zhuyin,text`

- [ ] **5. Download MOE common word list / 下載教育部常用詞表**  
  → Place in `data/raw/`  
  → Notify when ready (e.g. “lexicon in data/raw”) for batch RAG import / 完成後可協助批次匯入詞庫

---

## Environment and Accounts / 環境與帳號

- [ ] Install **Python 3.11+** and **Node.js 18+** / 安裝執行環境
- [ ] Backend deps / 後端依賴：`cd backend && pip install -r requirements.txt`
- [ ] ML deps / ML 依賴：`pip install -r ml/requirements.txt` (for keypoint extraction / 擷取關鍵點時)
- [ ] Choose a **hosting platform / 部署平台** (one of): Render · Railway · campus VPS  
  > GitHub Pages serves static frontend only; **cannot** run FastAPI / 僅能放前端，無法跑後端
- [ ] (Optional) Enable **GitHub Pages** for frontend / 啟用前端靜態部署

---

## Data Collection / 資料蒐集（required for model training / 訓練必備）

- [ ] **Zhuyin sign videos** `.mp4` → `data/raw/`
- [ ] **Label CSV** → `ml/dataset/labels.csv`
- [ ] Run keypoint extraction / 執行關鍵點擷取：
  ```bash
  python ml/extract_features.py \
    --input data/raw/your_video.mp4 \
    --output ml/dataset/features/
  ```
- [ ] **Homophone evaluation set / 同音消歧測試集** (30+ pairs / 至少 30 組)  
  → Copy `data/eval/homophone_pairs.template.json` → `data/eval/homophone_pairs.json`
- [ ] **37 Zhuyin symbols + 5 tones / 37 注音 + 5 聲調** label table → `data/raw/` (if provided by school / 若學校有標準版)
- [ ] Expand RAG corpus / 擴充詞庫：
  ```bash
  python scripts/import_corpus.py --zhuyin "ㄋㄧˇ ㄏㄠˇ" --text "你好" --tags greeting
  ```

---

## Model Training / 模型訓練（after videos + labels / 有影片與標註後）

- [ ] Verify JSON features in `ml/dataset/features/` / 確認特徵檔存在
- [ ] Align `labels.csv` filenames with feature files / 標註與檔名一致
- [ ] Train CNN+LSTM (GPU or Colab) / 訓練模型  
  → `python ml/train_cnn_lstm.py` (training logic pending / 訓練程式待實作)
- [ ] Save weights to `ml/checkpoints/cnn_lstm.pt`
- [ ] Restart backend; check `/api/health` → `model_loaded: true`

---

## Thesis and Administration / 論文與專題行政

- [ ] Confirm thesis title (EN/ZH) and deadlines with advisor / 與指導教授確認題目與口試日期
- [ ] Prepare **consent forms** if filming other signers / 拍攝他人手語需受試者同意書
- [ ] Write up: architecture, RAG homophone experiments, accuracy, latency / 撰寫架構圖、RAG 實驗、準確率、延遲
- [ ] Run RAG evaluation / 執行 RAG 評估：
  ```bash
  python scripts/eval_rag.py
  ```

---

## Deployment and Demo / 部署與展示（later phase）

- [ ] Deploy backend to Render or Railway (`GEMINI_API_KEY`, CORS) / 後端上雲
- [ ] Build frontend: `cd frontend && npm run build`
- [ ] Deploy frontend (GitHub Pages or same domain as API) / 前端部署
- [ ] Prepare oral demo: homophone `ㄓㄨㄥ ㄒㄧㄣ`, multilingual output, WebSocket / 口試演示腳本

---

## Optional Enhancements / 加值項目（時間允許時）

- [ ] Upgrade RAG to **bge-m3 + ChromaDB**
- [ ] **Docker Compose** one-command stack
- [ ] **ZeroTier** private LLM endpoint (security bonus / 資安展示)

---

## Already Done / 已完成（無需重複）

- [x] Monorepo scaffold, MIT license, README badges / 專案骨架與文件
- [x] FastAPI + RAG + Gemini (mock) + WebSocket
- [x] React UI (camera, language picker, demo buttons) / 前端介面
- [x] Sample corpus 40+ entries, import script, MediaPipe extractor / 詞庫與擷取腳本
- [x] CI workflow and `VERSION` file

---

## MVP Completion Criteria / 完成標準（demo / 口試）

| Criterion / 項目 | Done? |
|------------------|-------|
| Camera or demo → Zhuyin sequence / 鏡頭或演示 → 注音輸出 | [ ] |
| Homophone RAG Top-3 demonstrable / 同音 RAG Top-3 可展示 | [ ] |
| Chinese sentence + ≥2 target languages / 中文 + 至少兩種外語 | [ ] |
| End-to-end latency (ms) for thesis / 端到端延遲可寫入論文 | [ ] |

---

**Progress updates / 有進度時**：Reference item numbers in chat (e.g. “#5 lexicon in data/raw”) to continue import or training work / 標註編號即可接續開發。
