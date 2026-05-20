import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.schemas import TranslateRequest
from app.services.pipeline import run_translate

router = APIRouter()


@router.websocket("/ws/translate")
async def translate_ws(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            raw = await websocket.receive_text()
            try:
                payload = json.loads(raw)
                req = TranslateRequest(**payload)
                result = run_translate(req)
                await websocket.send_json(result.model_dump())
            except Exception as exc:
                await websocket.send_json(
                    {"error": str(exc), "type": type(exc).__name__}
                )
    except WebSocketDisconnect:
        pass
