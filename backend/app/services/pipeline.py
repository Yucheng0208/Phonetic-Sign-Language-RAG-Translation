from app.llm.gemini import polish_and_translate
from app.rag.retriever import HybridRetriever
from app.schemas import (
    RagCandidate,
    RagSearchResponse,
    TranslateRequest,
    TranslateResponse,
)

_retriever: HybridRetriever | None = None


def get_retriever() -> HybridRetriever:
    global _retriever
    if _retriever is None:
        _retriever = HybridRetriever()
    return _retriever


def reload_retriever() -> None:
    global _retriever
    _retriever = HybridRetriever()


def run_rag_search(zhuyin: str, top_k: int = 5) -> RagSearchResponse:
    zhuyin_norm = " ".join(zhuyin.split())
    ranked = get_retriever().search(zhuyin_norm, top_k=top_k)
    return RagSearchResponse(
        zhuyin=zhuyin_norm,
        candidates=[
            RagCandidate(text=r.text, zhuyin=r.zhuyin, score=r.score, tags=r.tags)
            for r in ranked
        ],
    )


def run_translate(req: TranslateRequest) -> TranslateResponse:
    zhuyin = " ".join(req.zhuyin.split())
    ranked = get_retriever().search(zhuyin, top_k=req.top_k)
    candidates = [
        RagCandidate(text=r.text, zhuyin=r.zhuyin, score=r.score, tags=r.tags)
        for r in ranked
    ]
    chinese, translation, is_mock = polish_and_translate(
        zhuyin, ranked, req.target_lang
    )
    return TranslateResponse(
        zhuyin=zhuyin,
        rag_candidates=candidates,
        chinese=chinese,
        translation=translation,
        target_lang=req.target_lang,
        llm_mock=is_mock,
    )
