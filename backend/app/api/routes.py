from fastapi import APIRouter, HTTPException, Query

from app.config import settings
from app.models.recognizer import DEMO_ZHUYIN, model_checkpoint_exists, recognize
from app.rag.corpus import load_corpus
from app.schemas import (
    HealthResponse,
    RagSearchResponse,
    RecognizeRequest,
    RecognizeResponse,
    TranslateRequest,
    TranslateResponse,
)
from app.services.pipeline import run_rag_search, run_translate

router = APIRouter()


def _app_version() -> str:
    from app.config import ROOT_DIR

    version_file = ROOT_DIR / "VERSION"
    return version_file.read_text(encoding="utf-8").strip() if version_file.is_file() else "0.1.0"


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        version=_app_version(),
        corpus_entries=len(load_corpus()),
        gemini_configured=bool(settings.gemini_api_key),
        model_loaded=model_checkpoint_exists(),
    )


@router.get("/rag/search", response_model=RagSearchResponse)
def rag_search(
    zhuyin: str = Query(..., description="注音序列"),
    top_k: int = Query(5, ge=1, le=20),
) -> RagSearchResponse:
    return run_rag_search(zhuyin, top_k=top_k)


@router.get("/recognize/demos")
def list_recognize_demos() -> dict[str, dict[str, str]]:
    return DEMO_ZHUYIN


@router.post("/recognize", response_model=RecognizeResponse)
def recognize_sign(req: RecognizeRequest) -> RecognizeResponse:
    zhuyin, source, message = recognize(
        keypoints=req.keypoints,
        demo_id=req.demo_id,
    )
    if not zhuyin:
        raise HTTPException(status_code=400, detail=message)
    return RecognizeResponse(zhuyin=zhuyin, source=source, message=message)


@router.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest) -> TranslateResponse:
    return run_translate(req)
