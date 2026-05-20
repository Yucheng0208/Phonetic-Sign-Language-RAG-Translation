#!/usr/bin/env bash
# 同時啟動後端與前端（需分別安裝依賴）
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "啟動後端 http://localhost:8000"
(cd "$ROOT/backend" && .venv/bin/uvicorn app.main:app --reload --port 8000) &
BACKEND_PID=$!

echo "啟動前端 http://localhost:5173"
(cd "$ROOT/frontend" && npm run dev) &
FRONTEND_PID=$!

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
