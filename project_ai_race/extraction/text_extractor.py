"""Body text extraction helpers."""
from __future__ import annotations

import re
from typing import Any, List


def extract_paragraphs(page: Any) -> List[str]:
    """Extract textual paragraphs from the supplied pdfplumber page."""
    extractor = getattr(page, "extract_text", None)
    if extractor is None:
        return []

    raw_text = extractor(x_tolerance=2, y_tolerance=3) or ""
    cleaned = raw_text.replace("\r", "\n")
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    paragraphs = [paragraph.strip() for paragraph in cleaned.split("\n\n") if paragraph.strip()]
    return paragraphs
