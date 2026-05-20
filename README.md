<div align="center">

# Phonetic Sign Translator

### Zhuyin Sign Language · RAG Disambiguation · Multilingual Translation

*Phonetic Sign Language RAG Translation System*

[![Version](https://img.shields.io/badge/version-0.1.0-blue?style=flat-square)](./VERSION)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](./backend/requirements.txt)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi&logoColor=white)](./backend)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)](./frontend)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?style=flat-square&logo=typescript&logoColor=white)](./frontend)
[![PyTorch](https://img.shields.io/badge/PyTorch-planned-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)](./ml)

[Features](#features) ·
[Architecture](#architecture) ·
[Quick Start](#quick-start) ·
[API](#api-endpoints) ·
[Roadmap](./TODO.md) ·
[Citation](#citation)

</div>

---

## Overview

| Item | Description |
|------|-------------|
| **Project** | Phonetic Sign Translator — intelligent translation for Zhuyin (phonetic) sign language |
| **Thesis title** | Multimodal Feature Fusion and RAG-Enhanced Phonetic Sign Language Recognition and Translation System |
| **Version** | `0.1.0` — see [VERSION](./VERSION) for release manifest / 版本內容說明 |
| **License** | [MIT](./LICENSE) |

---

## Features

- **Zhuyin sign pipeline** — phonetic sequence → recognition → sentence building → translation (CNN+LSTM in progress)
- **Hybrid RAG retrieval** — BM25 + Zhuyin n-gram fusion for homophone disambiguation (e.g., 中心 / 忠心 / 中新)
- **LLM refinement** — Google Gemini for fluency and multilingual output (mock mode without API key)
- **Real-time channel** — WebSocket streaming of translation results
- **Responsive UI** — React + TypeScript, camera preview, Swiper language picker

---

## Architecture

```
[Camera] → [MediaPipe] → [CNN+LSTM] → [Zhuyin sequence]
                                        ↓
                              [RAG candidate matching] ← phrase corpus
                                        ↓
                              [Chinese sentence + LLM]
                                        ↓
                              [Multilingual output] → [React frontend]
```

---

## Quick Start

### Requirements

- Python **3.11+**
- Node.js **18+**
- (Optional) Google AI Studio API key

### 1. Environment variables

```bash
cp .env.example .env
# Edit .env and set GEMINI_API_KEY (optional)
```

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: <http://localhost:8000/docs>

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

App: <http://localhost:5173>

### One-command dev (dependencies must be installed)

```bash
./scripts/dev.sh
```

---

## Project Structure

```
Phonetic-Sign-Language-RAG-Translation/
├── backend/                 # FastAPI service
├── frontend/                # React + Vite app
├── ml/                      # MediaPipe features, CNN+LSTM training
├── data/zhuyin_corpus/      # RAG corpus (*.json)
├── docs/                    # plans and technical notes
├── scripts/                 # dev and import utilities
├── VERSION                  # semver (line 1) + bilingual manifest / 版本號與內容清單
├── LICENSE                  # MIT
└── CITATION.bib             # BibTeX entry
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Health check, corpus size, model status |
| `GET` | `/api/version` | Semver + full VERSION manifest text |
| `POST` | `/api/translate` | Zhuyin → RAG → Chinese → target language |
| `GET` | `/api/rag/search` | RAG candidates only |
| `POST` | `/api/recognize` | Sign recognition (demo / keypoints) |
| `WS` | `/ws/translate` | WebSocket live translation |

---

## Roadmap

See **[TODO.md](./TODO.md)** for required data, API keys, and milestones. Technical breakdown: [docs/TODO.md](./docs/TODO.md).

```bash
# Add a corpus entry
python scripts/import_corpus.py --zhuyin "ㄋㄧˇ ㄏㄠˇ" --text "你好" --tags greeting
```

---

## Tech Stack

| Layer | Stack |
|-------|--------|
| Keypoints | MediaPipe Holistic |
| Recognition | CNN + LSTM (PyTorch, in progress) |
| RAG | BM25 + n-gram (bge-m3 planned) |
| Backend | FastAPI · Uvicorn |
| LLM | Google Gemini |
| Frontend | React 19 · TypeScript · Vite · Swiper |

---

## License

This project is released under the **[MIT License](./LICENSE)**.

- Free to use, modify, distribute, and use commercially
- Include copyright and license notice in copies
- Provided "as is" without warranty

---

## Citation

If you use this software in academic work, please cite:

```bibtex
@misc{phonetic_sign_rag_2026,
  title        = {Multimodal Feature Fusion and {RAG}-Enhanced Phonetic Sign Language Recognition and Translation System},
  year         = {2026},
  howpublished = {Software},
  url          = {https://github.com/Yucheng0208/Phonetic-Sign-Language-RAG-Translation},
  note         = {Zhuyin sign language translation with hybrid RAG and LLM refinement}
}
```

A standalone BibTeX file is available at [CITATION.bib](./CITATION.bib).
