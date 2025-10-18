"""Mathematical formula extraction helpers."""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

INLINE_MATH = re.compile(r"\\\((?P<formula>.+?)\\\)")
DISPLAY_MATH = re.compile(r"\\\[(?P<formula>.+?)\\\]")
LATEX_DOLLARS = re.compile(r"\$(?P<formula>.+?)\$")


def _extract_from_text(text: str) -> List[Tuple[str, str]]:
    formulas: List[Tuple[str, str]] = []
    for pattern in (DISPLAY_MATH, INLINE_MATH, LATEX_DOLLARS):
        for match in pattern.finditer(text):
            formulas.append((match.group(0), match.group("formula").strip()))
    return formulas


def extract_formulas(page: Any) -> Dict[str, str]:
    """Return LaTeX strings keyed by their location identifiers."""
    text = getattr(page, "extract_text", lambda: "")() or ""
    formulas: Dict[str, str] = {}
    for idx, (_, formula) in enumerate(_extract_from_text(text)):
        formulas[f"formula_{page.page_number}_{idx}"] = formula
    return formulas
