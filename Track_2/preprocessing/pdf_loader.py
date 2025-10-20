"""Utilities for loading raw PDF documents."""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator, List

try:
    import pdfplumber  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    pdfplumber = None


@contextmanager
def open_pdf(path: str | Path) -> Iterator["pdfplumber.PDF"]:
    """Context manager that yields an opened pdfplumber document."""
    if pdfplumber is None:
        raise ImportError("pdfplumber is required for open_pdf but is not installed.")

    pdf = pdfplumber.open(str(path))
    try:
        yield pdf
    finally:
        pdf.close()


def load_pdf_paths(input_dir: str | Path) -> List[Path]:
    """Return all PDF files inside the provided directory."""
    directory = Path(input_dir)
    if not directory.exists():
        return []
    return sorted(directory.glob("**/*.pdf"))


def load_pdfs(paths: Iterable[str | Path]) -> List["pdfplumber.PDF"]:
    """Load PDFs from disk and return the pdfplumber handles."""
    if pdfplumber is None:
        raise ImportError("pdfplumber is required for load_pdfs but is not installed.")

    documents: List["pdfplumber.PDF"] = []
    for path in paths:
        documents.append(pdfplumber.open(str(path)))
    return documents
