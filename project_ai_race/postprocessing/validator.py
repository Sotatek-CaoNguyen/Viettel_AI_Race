"""Output validation helpers."""
from __future__ import annotations

from typing import Any, List


class ValidationIssue(Exception):
    """Raised when an output artifact fails validation."""


def validate(document: Any) -> List[str]:
    """Return a list of validation warnings for the document."""
    warnings: List[str] = []
    pages = document.get("pages", []) if isinstance(document, dict) else []
    if not pages:
        warnings.append("Document contains no pages.")
    for page in pages:
        if not page.get("paragraphs") and not page.get("tables"):
            warnings.append(f"Page {page.get('page_number', '?')} has no content.")
    return warnings
