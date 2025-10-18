"""File handling utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Sequence


def list_files(directory: str | Path, suffixes: Iterable[str]) -> List[Path]:
    """Return files under directory that match one of the suffixes."""
    path = Path(directory)
    matches: List[Path] = []
    for suffix in suffixes:
        matches.extend(path.glob(f"**/*{suffix}"))
    return sorted({m.resolve() for m in matches})


def ensure_dir(path: str | Path) -> Path:
    """Create directory (and parents) if it does not exist."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def write_text(path: str | Path, content: str) -> None:
    """Persist text content using UTF-8 encoding."""
    Path(path).write_text(content, encoding="utf-8")


def read_text(path: str | Path) -> str:
    """Read text content using UTF-8 encoding."""
    return Path(path).read_text(encoding="utf-8")


def chunk_sequence(items: Sequence[str], chunk_size: int) -> List[List[str]]:
    """Split a sequence into mostly-even chunks."""
    chunks: List[List[str]] = []
    chunk: List[str] = []
    for item in items:
        chunk.append(item)
        if len(chunk) >= chunk_size:
            chunks.append(chunk)
            chunk = []
    if chunk:
        chunks.append(chunk)
    return chunks
