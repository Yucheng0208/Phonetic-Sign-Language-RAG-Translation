"""Read VERSION file: line 1 = semver, remainder = manifest text."""

from __future__ import annotations

import re

from app.config import ROOT_DIR

_VERSION_FILE = ROOT_DIR / "VERSION"
_SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(-[\w.]+)?(\+[\w.]+)?$")


def read_version() -> str:
    if not _VERSION_FILE.is_file():
        return "0.1.0"
    for line in _VERSION_FILE.read_text(encoding="utf-8").splitlines():
        candidate = line.strip()
        if candidate and _SEMVER_RE.match(candidate):
            return candidate
    return "0.1.0"


def read_manifest() -> str:
    if not _VERSION_FILE.is_file():
        return ""
    lines = _VERSION_FILE.read_text(encoding="utf-8").splitlines()
    if len(lines) <= 1:
        return ""
    return "\n".join(lines[1:]).strip()
