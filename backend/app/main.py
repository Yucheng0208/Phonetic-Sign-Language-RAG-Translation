from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes, websocket
from app.config import ROOT_DIR, settings


def _app_version() -> str:
    version_file = ROOT_DIR / "VERSION"
    if version_file.is_file():
        return version_file.read_text(encoding="utf-8").strip()
    return "0.1.0"
from app.rag.corpus import load_corpus
from app.services.pipeline import get_retriever


@asynccontextmanager
async def lifespan(_app: FastAPI):
    load_corpus()
    get_retriever()
    yield


app = FastAPI(
    title="注手快譯通 API",
    description="注音手語 RAG 消歧與多語翻譯",
    version=_app_version(),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router, prefix="/api", tags=["api"])
app.include_router(websocket.router, tags=["websocket"])


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "注手快譯通", "docs": "/docs"}
