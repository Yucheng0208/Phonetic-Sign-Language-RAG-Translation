#!/usr/bin/env python3
"""新增或更新 RAG 詞庫條目。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS_DIR = ROOT / "data" / "zhuyin_corpus"
DEFAULT_FILE = CORPUS_DIR / "user_imports.json"


def load_entries(path: Path) -> list[dict]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


def main() -> None:
    parser = argparse.ArgumentParser(description="匯入注音詞庫條目")
    parser.add_argument("--zhuyin", required=True, help='例：ㄋㄧˇ ㄏㄠˇ')
    parser.add_argument("--text", required=True, help="例：你好")
    parser.add_argument("--tags", default="", help="逗號分隔，例：問候,常用")
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_FILE,
        help=f"寫入的 JSON 檔（預設 {DEFAULT_FILE.name}）",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    entry = {"zhuyin": args.zhuyin.strip(), "text": args.text.strip(), "tags": tags}

    entries = load_entries(args.file)
    for i, e in enumerate(entries):
        if e["zhuyin"] == entry["zhuyin"] and e["text"] == entry["text"]:
            entries[i] = entry
            print(f"更新既有條目：{entry['text']}")
            break
    else:
        entries.append(entry)
        print(f"新增條目：{entry['text']}")

    if args.dry_run:
        print(json.dumps(entry, ensure_ascii=False, indent=2))
        return

    args.file.parent.mkdir(parents=True, exist_ok=True)
    args.file.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"已寫入 {args.file}（共 {len(entries)} 筆）")
    print("重啟後端後生效（或呼叫 reload API，若已實作）")


if __name__ == "__main__":
    main()
