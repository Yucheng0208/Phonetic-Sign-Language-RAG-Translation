from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes, websocket
from app.config import settings
from app.rag.corpus import load_corpus
from app.services.pipeline import get_retriever
from app.version_info import read_version


@asynccontextmanager
async def lifespan(_app: FastAPI):
    load_corpus()
    get_retriever()
    yield


app = FastAPI(
    title="Phonetic Sign Translator API",
    description="Zhuyin sign language RAG disambiguation and multilingual translation",
    version=read_version(),
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
    return {"service": "Phonetic Sign Translator", "docs": "/docs", "version": read_version()}
