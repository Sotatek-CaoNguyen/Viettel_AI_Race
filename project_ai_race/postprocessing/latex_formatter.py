"""LaTeX formatting helpers."""
from __future__ import annotations

import re
from typing import Dict

UNWANTED_TOKENS = re.compile(r"\s+")


def _ensure_math_environment(equation: str) -> str:
    stripped = equation.strip()
    if stripped.startswith(r"\begin"):
        return stripped
    if not stripped.startswith(r"\frac") and "=" in stripped:
        return stripped
    return stripped


def format_equations(equations: Dict[str, str]) -> Dict[str, str]:
    """Clean and validate LaTeX equations."""
    formatted: Dict[str, str] = {}
    for key, latex in equations.items():
        cleaned = UNWANTED_TOKENS.sub(" ", latex)
        formatted[key] = _ensure_math_environment(cleaned)
    return formatted
