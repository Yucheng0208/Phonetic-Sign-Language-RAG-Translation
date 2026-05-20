# 你還要做的事 — 專題 TODO

> **注手快譯通** · 最後更新：2026-05-20  
> 勾選 `[x]` 代表完成。細節與開發任務見 [docs/TODO.md](./docs/TODO.md)。

---

## 本週最優先（先做這 5 件）

- [ ] **1. 申請 Gemini API Key**  
  → [Google AI Studio](https://aistudio.google.com/apikey)  
  → 複製到 `.env`：`GEMINI_API_KEY=你的金鑰`

- [ ] **2. 本機跑起來確認**  
  ```bash
  cp .env.example .env
  ./scripts/dev.sh
  ```  
  → 開 http://localhost:5173 ，點「中心（同音演示）」看 RAG + 翻譯

- [ ] **3. 開始錄製注音手語影片**  
  → 放到 `data/raw/`（每人每詞至少 20 次，光線固定、背景簡單）

- [ ] **4. 建立標註表**  
  → 複製 `ml/dataset/labels.csv.example` → `ml/dataset/labels.csv`  
  → 填：`filename,zhuyin,text`（檔名對應你錄的影片）

- [ ] **5. 下載教育部常用詞表**  
  → 放到 `data/raw/`  
  → 完成後跟我說「詞表已放好」，可幫你批次匯入 RAG 詞庫

---

## 環境與帳號

- [ ] 安裝 **Python 3.11+**、**Node.js 18+**
- [ ] 後端依賴：`cd backend && pip install -r requirements.txt`
- [ ] ML 依賴：`pip install -r ml/requirements.txt`（要擷取關鍵點時）
- [ ] 申請 **部署平台**（擇一）：Render / Railway / 學校 VPS  
  > GitHub Pages 只能放前端，**不能**跑 FastAPI 後端
- [ ] （選用）啟用 **GitHub Pages** 部署前端靜態站

---

## 資料蒐集（論文核心，缺了無法訓練模型）

- [ ] **注音手語影片** `.mp4` → `data/raw/`
- [ ] **標註 CSV** → `ml/dataset/labels.csv`
- [ ] 執行關鍵點擷取：
  ```bash
  python ml/extract_features.py \
    --input data/raw/你的影片.mp4 \
    --output ml/dataset/features/
  ```
- [ ] **同音消歧測試集**（至少 30 組）  
  → 複製 `data/eval/homophone_pairs.template.json`  
  → 另存 `data/eval/homophone_pairs.json` 並填寫
- [ ] **37 注音符 + 5 聲調** 標籤表（若學校有標準版，放到 `data/raw/`）
- [ ] 持續擴充 RAG 詞庫：
  ```bash
  python scripts/import_corpus.py --zhuyin "ㄋㄧˇ ㄏㄠˇ" --text "你好" --tags 問候
  ```

---

## 模型訓練（有影片 + 標註後）

- [ ] 確認 `ml/dataset/features/` 有 JSON 特徵檔
- [ ] 確認 `ml/dataset/labels.csv` 與特徵檔名對得上
- [ ] 訓練 CNN+LSTM（需 GPU，Colab 亦可）  
  → `python ml/train_cnn_lstm.py`（訓練邏輯待實作，有資料後可請 AI 完成）
- [ ] 權重放到 `ml/checkpoints/cnn_lstm.pt`
- [ ] 重啟後端，確認 `/api/health` 的 `model_loaded: true`

---

## 論文與專題行政

- [ ] 與指導教授確認中英文題目、口試／繳交日期
- [ ] 若拍攝他人手語 → 準備**受試者同意書**
- [ ] 撰寫：系統架構圖、RAG 同音實驗、辨識準確率、端到端延遲
- [ ] 跑 RAG 評估（需測試集）：
  ```bash
  python scripts/eval_rag.py
  ```

---

## 部署與展示（後期）

- [ ] 後端部署到 Render / Railway（設定 `GEMINI_API_KEY`、CORS）
- [ ] 前端 build：`cd frontend && npm run build`
- [ ] 前端部署（GitHub Pages 或與後端同域）
- [ ] 準備口試/demo：同音詞「ㄓㄨㄥ ㄒㄧㄣ」、多語翻譯、即時 WebSocket

---

## 加值項目（時間夠再做）

- [ ] RAG 升級 **bge-m3 + ChromaDB**
- [ ] **Docker Compose** 一鍵啟動
- [ ] **Zerotier** 私有 LLM（Bonus 資安展示）

---

## 已幫你做好（不用再寫）

- [x] 專案骨架、MIT 授權、README 徽章
- [x] FastAPI + RAG + Gemini（mock）+ WebSocket
- [x] React 前端（攝影機、語言選擇、演示按鈕）
- [x] 示範詞庫 40+ 筆、匯入腳本、MediaPipe 擷取腳本
- [x] CI、版本號 `VERSION`

---

## 完成標準（MVP 口試/demo）

| 項目 | 完成？ |
|------|--------|
| 鏡頭或演示 → 輸出注音序列 | [ ] |
| 同音詞 RAG 可展示 Top-3 | [ ] |
| 中文組句 + ≥2 種外語 | [ ] |
| 有端到端延遲數據（ms）可寫進論文 | [ ] |

---

**有進度時**：在對話標編號，例如「#5 詞表已放 data/raw」，我會接著幫你寫匯入或訓練程式。
