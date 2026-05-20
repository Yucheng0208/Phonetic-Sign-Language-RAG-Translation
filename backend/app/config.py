from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[2]
CORPUS_DIR = ROOT_DIR / "data" / "zhuyin_corpus"
ML_CHECKPOINT_DIR = ROOT_DIR / "ml" / "checkpoints"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    gemini_api_key: str = ""
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    rag_embedding_alpha: float = 0.5
    gemini_model: str = "gemini-2.0-flash"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
