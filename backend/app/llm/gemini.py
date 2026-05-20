from __future__ import annotations

from app.config import settings
from app.rag.retriever import RankedPhrase

_LANG_NAMES = {
    "zh-TW": "繁體中文",
    "zh-CN": "簡體中文",
    "en": "English",
    "ja": "日本語",
    "ko": "한국어",
}


def _format_candidates(candidates: list[RankedPhrase]) -> str:
    lines = []
    for i, c in enumerate(candidates, 1):
        tag_str = f" [{', '.join(c.tags)}]" if c.tags else ""
        lines.append(f"{i}. {c.text}（注音：{c.zhuyin}）{tag_str}")
    return "\n".join(lines)


def polish_and_translate(
    zhuyin: str,
    candidates: list[RankedPhrase],
    target_lang: str,
) -> tuple[str, str, bool]:
    """
    回傳 (chinese_sentence, translation, is_mock)。
    無 API key 時使用規則式 fallback。
    """
    if not settings.gemini_api_key:
        return _mock_response(zhuyin, candidates, target_lang)

    try:
        import google.generativeai as genai

        genai.configure(api_key=settings.gemini_api_key)
        model = genai.GenerativeModel(settings.gemini_model)

        lang_name = _LANG_NAMES.get(target_lang, target_lang)
        candidate_block = _format_candidates(candidates)

        prompt = f"""你是注音手語翻譯助理。使用者以注音手語拼出下列序列，請依候選詞挑選最合適的用字並組成通順的中文短句。

注音序列：{zhuyin}

RAG 候選詞（依相關度排序）：
{candidate_block}

請以 JSON 格式回覆，不要加 markdown 程式碼區塊，格式如下：
{{"chinese": "繁體中文句子", "translation": "若目標語言為繁體中文則與 chinese 相同，否則翻譯為{lang_name}"}}

目標語言：{lang_name}（代碼 {target_lang}）
只輸出 JSON，不要其他說明。"""

        response = model.generate_content(prompt)
        text = (response.text or "").strip()
        # 簡易 JSON 擷取
        import json

        if text.startswith("```"):
            text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        data = json.loads(text)
        chinese = str(data.get("chinese", "")).strip()
        translation = str(data.get("translation", chinese)).strip()
        if not chinese:
            return _mock_response(zhuyin, candidates, target_lang)
        return chinese, translation, False
    except Exception:
        return _mock_response(zhuyin, candidates, target_lang)


def _mock_response(
    zhuyin: str,
    candidates: list[RankedPhrase],
    target_lang: str,
) -> tuple[str, str, bool]:
    chinese = candidates[0].text if candidates else zhuyin
    if target_lang in ("zh-TW", "zh-CN"):
        return chinese, chinese, True
    mock_translations = {
        "en": f"[mock] {chinese}",
        "ja": f"[mock] {chinese}",
        "ko": f"[mock] {chinese}",
    }
    return chinese, mock_translations.get(target_lang, f"[mock] {chinese}"), True
