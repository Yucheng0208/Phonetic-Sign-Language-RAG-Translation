<div align="center">

# 注手快譯通

### 注音手語 · RAG 消歧 · 多語翻譯

*Phonetic Sign Language RAG Translation System*

[![Version](https://img.shields.io/badge/version-0.1.0-blue?style=flat-square)](./VERSION)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](./backend/requirements.txt)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi&logoColor=white)](./backend)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](./frontend)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?style=flat-square&logo=typescript&logoColor=white)](./frontend)
[![PyTorch](https://img.shields.io/badge/PyTorch-待整合-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)](./ml)

[功能特色](#-功能特色) ·
[架構](#-系統架構) ·
[快速開始](#-快速開始) ·
[API](#-api-端點) ·
[待辦事項](./docs/TODO.md)

</div>

---

## 📌 專題資訊

| 項目 | 內容 |
|------|------|
| **專題名稱** | 注手快譯通 — 以注音手語為情境的智慧翻譯系統 |
| **論文題目** | 基於多模態特徵融合與 RAG 增強之注音手語辨識翻譯系統 |
| **英文題目** | Multimodal Feature Fusion and RAG-Enhanced Phonetic Sign Language Recognition and Translation System |
| **版本** | `0.1.0`（見 [VERSION](./VERSION)） |
| **授權** | [MIT](./LICENSE) |
| **作者** | Yu-Cheng Chang（張育丞） |

---

## ✨ 功能特色

- 🖐️ **注音手語流程** — 注音序列 → 辨識 → 組句 → 翻譯（CNN+LSTM 訓練中）
- 🔍 **RAG 雙支幹檢索** — BM25 + 注音 n-gram 融合，處理同音消歧（如：中心 / 忠心 / 中新）
- 🤖 **LLM 潤飾** — Google Gemini 組句與多語輸出（未設定 API Key 時自動 mock）
- 📡 **即時通訊** — WebSocket 串流翻譯結果
- 📱 **響應式前端** — React + TypeScript，攝影機預覽、Swiper 語言選擇

---

## 🏗 系統架構

```
[攝影機] → [MediaPipe] → [CNN+LSTM] → [注音序列]
                                        ↓
                              [RAG 候選詞比對] ← 常用語詞庫
                                        ↓
                              [中文組句 + LLM]
                                        ↓
                              [多語言輸出] → [React 前端]
```

---

## 🚀 快速開始

### 環境需求

- Python **3.11+**
- Node.js **18+**
- （選用）Google AI Studio API Key

### 1. 複製環境變數

```bash
cp .env.example .env
# 編輯 .env，填入 GEMINI_API_KEY（可選）
```

### 2. 後端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

→ API 文件：<http://localhost:8000/docs>

### 3. 前端

```bash
cd frontend
npm install
npm run dev
```

→ 應用程式：<http://localhost:5173>

### 一鍵啟動（需已安裝依賴）

```bash
./scripts/dev.sh
```

---

## 📁 專案結構

```
Phonetic-Sign-Language-RAG-Translation/
├── backend/                 # FastAPI 後端
├── frontend/                # React + Vite 前端
├── ml/                      # MediaPipe 特徵、CNN+LSTM 訓練
├── data/zhuyin_corpus/      # RAG 詞庫（*.json）
├── docs/                    # 工作計畫、TODO
├── scripts/                 # 開發與匯入工具
├── VERSION                  # 語意化版本
└── LICENSE                  # MIT
```

---

## 🔌 API 端點

| 方法 | 路徑 | 說明 |
|------|------|------|
| `GET` | `/api/health` | 健康檢查、詞庫筆數、模型狀態 |
| `POST` | `/api/translate` | 注音 → RAG → 中文 → 多語 |
| `GET` | `/api/rag/search` | 僅 RAG 候選詞查詢 |
| `POST` | `/api/recognize` | 手語辨識（演示 / 關鍵點） |
| `WS` | `/ws/translate` | WebSocket 即時翻譯 |

---

## 📋 開發待辦

你需要準備的資料與 API Key，請見 **[docs/TODO.md](./docs/TODO.md)**。

```bash
# 新增詞庫
python scripts/import_corpus.py --zhuyin "ㄋㄧˇ ㄏㄠˇ" --text "你好" --tags 問候
```

---

## 🛠 技術棧

| 層級 | 技術 |
|------|------|
| 關鍵點 | MediaPipe Holistic |
| 辨識模型 | CNN + LSTM（PyTorch，訓練中） |
| RAG | BM25 + n-gram / 規劃 bge-m3 |
| 後端 | FastAPI · Uvicorn |
| LLM | Google Gemini |
| 前端 | React 19 · TypeScript · Vite · Swiper |

---

## 📄 授權

本專案以 **[MIT License](./LICENSE)** 開源。

- 可自由使用、修改、散布與商用
- 需保留版權與授權聲明
- 軟體按「現狀」提供，不提供任何保證

```
MIT License
Copyright (c) 2026 Yu-Cheng Chang（張育丞）
```

---

## 👤 作者

**Yu-Cheng Chang（張育丞）**

- GitHub：[@Yucheng0208](https://github.com/Yucheng0208)
- Repository：[Phonetic-Sign-Language-RAG-Translation](https://github.com/Yucheng0208/Phonetic-Sign-Language-RAG-Translation)
