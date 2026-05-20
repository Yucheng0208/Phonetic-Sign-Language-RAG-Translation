import json
from dataclasses import dataclass
from pathlib import Path

from app.config import CORPUS_DIR


@dataclass(frozen=True)
class PhraseEntry:
    zhuyin: str
    text: str
    tags: tuple[str, ...]


def _parse_file(path: Path) -> list[PhraseEntry]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    entries: list[PhraseEntry] = []
    for item in raw:
        entries.append(
            PhraseEntry(
                zhuyin=item["zhuyin"].strip(),
                text=item["text"].strip(),
                tags=tuple(item.get("tags", [])),
            )
        )
    return entries


def load_corpus(corpus_dir: Path | None = None) -> list[PhraseEntry]:
    """載入目錄內所有 *.json 詞庫並合併。"""
    directory = corpus_dir or CORPUS_DIR
    if not directory.is_dir():
        return []

    all_entries: list[PhraseEntry] = []
    for path in sorted(directory.glob("*.json")):
        all_entries.extend(_parse_file(path))
    return all_entries
