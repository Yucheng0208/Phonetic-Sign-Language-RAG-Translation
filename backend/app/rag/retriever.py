"""BM25 + 輕量字符 n-gram embedding 的雙支幹 RAG 檢索。"""

from __future__ import annotations

import re
from dataclasses import dataclass

import numpy as np
from rank_bm25 import BM25Okapi

from app.config import settings
from app.rag.corpus import PhraseEntry, load_corpus

_ZHUYIN_RE = re.compile(r"[ㄅ-ㄩˊˇˋ˙]+")


def _tokenize_zhuyin(text: str) -> list[str]:
    return _ZHUYIN_RE.findall(text.replace(" ", ""))


def _char_ngrams(text: str, n: int = 2) -> list[str]:
    chars = list(text.replace(" ", ""))
    if len(chars) < n:
        return chars or [""]
    return ["".join(chars[i : i + n]) for i in range(len(chars) - n + 1)]


def _build_vocab(docs: list[list[str]]) -> dict[str, int]:
    vocab: dict[str, int] = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab


def _doc_vectors(docs: list[list[str]], vocab: dict[str, int]) -> np.ndarray:
    dim = max(len(vocab), 1)
    matrix = np.zeros((len(docs), dim), dtype=np.float32)
    for i, doc in enumerate(docs):
        for token in doc:
            idx = vocab.get(token)
            if idx is not None:
                matrix[i, idx] += 1.0
        norm = np.linalg.norm(matrix[i])
        if norm > 0:
            matrix[i] /= norm
    return matrix


@dataclass
class RankedPhrase:
    text: str
    zhuyin: str
    score: float
    tags: list[str]


class HybridRetriever:
    def __init__(self, entries: list[PhraseEntry] | None = None) -> None:
        self.entries = entries or load_corpus()
        self.zhuyin_texts = [e.zhuyin for e in self.entries]
        self.display_texts = [e.text for e in self.entries]
        self.tags = [list(e.tags) for e in self.entries]

        tokenized = [_tokenize_zhuyin(z) for z in self.zhuyin_texts]
        self._bm25 = BM25Okapi(tokenized)

        ngram_docs = [_char_ngrams(z) for z in self.zhuyin_texts]
        self._vocab = _build_vocab(ngram_docs)
        self._doc_matrix = _doc_vectors(ngram_docs, self._vocab)

    def search(self, query_zhuyin: str, top_k: int = 5) -> list[RankedPhrase]:
        if not self.entries:
            return []

        q_tokens = _tokenize_zhuyin(query_zhuyin)
        bm25_scores = self._bm25.get_scores(q_tokens)
        bm25_max = float(np.max(bm25_scores)) if len(bm25_scores) else 1.0
        if bm25_max <= 0:
            bm25_max = 1.0
        bm25_norm = bm25_scores / bm25_max

        q_ngrams = _char_ngrams(query_zhuyin)
        q_vec = np.zeros(max(len(self._vocab), 1), dtype=np.float32)
        for token in q_ngrams:
            idx = self._vocab.get(token)
            if idx is not None:
                q_vec[idx] += 1.0
        q_norm = np.linalg.norm(q_vec)
        if q_norm > 0:
            q_vec /= q_norm
        embed_scores = self._doc_matrix @ q_vec

        alpha = settings.rag_embedding_alpha
        fused = alpha * embed_scores + (1.0 - alpha) * bm25_norm

        ranked_idx = np.argsort(fused)[::-1][:top_k]
        results: list[RankedPhrase] = []
        for idx in ranked_idx:
            i = int(idx)
            results.append(
                RankedPhrase(
                    text=self.display_texts[i],
                    zhuyin=self.zhuyin_texts[i],
                    score=float(fused[i]),
                    tags=self.tags[i],
                )
            )
        return results
