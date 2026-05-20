"""注音手語辨識推論（CNN+LSTM 訓練完成後替換此 stub）。"""

from __future__ import annotations

from pathlib import Path

from app.config import ML_CHECKPOINT_DIR

# 演示用：前端可選 demo_id 走完整「辨識 → RAG → 翻譯」流程
DEMO_ZHUYIN: dict[str, dict[str, str]] = {
    "center": {"zhuyin": "ㄓㄨㄥ ㄒㄧㄣ", "label": "中心（同音演示）"},
    "hello": {"zhuyin": "ㄋㄧˇ ㄏㄠˇ", "label": "你好"},
    "thanks": {"zhuyin": "ㄒㄧㄝˋ ㄒㄧㄝˋ", "label": "謝謝"},
    "sign_translate": {"zhuyin": "ㄕㄡˇ ㄩˇ ㄈㄢ ㄧˋ", "label": "手語翻譯"},
    "taiwan": {"zhuyin": "ㄊㄞˊ ㄨㄢ", "label": "台灣"},
    "homophone_shiji": {"zhuyin": "ㄕˋ ㄐㄧˋ", "label": "世紀／事跡（同音）"},
}


def model_checkpoint_exists() -> bool:
    return (ML_CHECKPOINT_DIR / "cnn_lstm.pt").is_file()


def recognize(
    keypoints: list[list[float]] | None = None,
    demo_id: str | None = None,
) -> tuple[str, str, str]:
    """
    回傳 (zhuyin, source, message)。
    source: model | demo | unavailable
    """
    if demo_id:
        entry = DEMO_ZHUYIN.get(demo_id)
        if entry:
            return entry["zhuyin"], "demo", f"演示模式：{entry['label']}"
        return "", "unavailable", f"未知 demo_id: {demo_id}"

    if model_checkpoint_exists() and keypoints:
        # TODO: 載入 PyTorch 模型推論
        return "", "unavailable", "模型檔存在但推論尚未實作，請接續 ml/train_cnn_lstm.py"

    if keypoints:
        return (
            "",
            "unavailable",
            "已收到關鍵點，但尚未訓練模型。請提供標註資料並執行 ml/train_cnn_lstm.py",
        )

    return "", "unavailable", "請提供 demo_id 或 keypoints"
