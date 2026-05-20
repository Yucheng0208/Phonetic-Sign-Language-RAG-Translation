from pydantic import BaseModel, Field


class RagCandidate(BaseModel):
    text: str
    zhuyin: str
    score: float
    tags: list[str] = Field(default_factory=list)


class TranslateRequest(BaseModel):
    zhuyin: str = Field(..., description="空格分隔的注音序列，例如：ㄓㄨㄥ ㄒㄧㄣ")
    target_lang: str = Field(default="zh-TW", description="目標語言代碼")
    top_k: int = Field(default=5, ge=1, le=20)


class TranslateResponse(BaseModel):
    zhuyin: str
    rag_candidates: list[RagCandidate]
    chinese: str
    translation: str
    target_lang: str
    llm_mock: bool = False


class RagSearchResponse(BaseModel):
    zhuyin: str
    candidates: list[RagCandidate]


class RecognizeRequest(BaseModel):
    """手語辨識請求。模型未訓練前可用 demo_id 演示完整流程。"""

    keypoints: list[list[float]] | None = Field(
        default=None,
        description="扁平化關鍵點序列 [frame][dim]，訓練模型後使用",
    )
    demo_id: str | None = Field(
        default=None,
        description="演示用 ID，見 /api/recognize/demos",
    )


class RecognizeResponse(BaseModel):
    zhuyin: str
    source: str = Field(description="model | demo | unavailable")
    message: str = ""


class HealthResponse(BaseModel):
    status: str
    version: str = "0.1.0"
    corpus_entries: int
    gemini_configured: bool
    model_loaded: bool = False


class VersionResponse(BaseModel):
    version: str
    manifest: str = Field(
        default="",
        description="Full VERSION file body after the semver line / VERSION 檔第二行起之內容說明",
    )
