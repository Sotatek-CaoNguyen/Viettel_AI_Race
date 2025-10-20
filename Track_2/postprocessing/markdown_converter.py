"""Markdown conversion helpers."""
from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, Iterable, List

from .html_table_builder import build_html_table
from .latex_formatter import format_equations

HEADER_SIGNATURES = {
    "VIETTEL AI RACE TD012",
    "HE DIEU HANH LAN BAN HANH: 1",
}

HEADING_PATTERN = re.compile(r"^(\d+(?:\.\d+)*)(?:[\.)])?\s+(.*\S)$")
BULLET_MARKERS = ("-", "*", "\u2022", "\u2023", "\u25aa", "\u25e6")
MULTISPACE_RE = re.compile(r"\s+")


def _signature(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    without_marks = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
    collapsed = MULTISPACE_RE.sub(" ", without_marks)
    return collapsed.strip().upper()


def _is_repeated_header(text: str) -> bool:
    if not text:
        return False
    return _signature(text) in HEADER_SIGNATURES


def _normalize_heading(text: str) -> str | None:
    if _is_repeated_header(text):
        return None
    stripped = text.strip()
    if not stripped:
        return stripped
    if stripped.startswith("#"):
        return stripped
    match = HEADING_PATTERN.match(stripped)
    if not match:
        return stripped
    numbering, title = match.groups()
    heading_level = 1 if numbering.count(".") == 0 else 2
    return f"{'#' * heading_level} {title.strip()}"


def _normalize_bullet_line(text: str, indent: int) -> str:
    if not text:
        return text
    prefix = text.lstrip()
    if not prefix or prefix.startswith("|") or prefix.startswith("#"):
        return text
    for marker in BULLET_MARKERS:
        marker_token = f"{marker} "
        if prefix.startswith(marker_token):
            content = prefix[len(marker_token):]
            return ("* " + content) if indent >= 2 else ("  * " + content)
    return text


def _render_paragraphs(paragraphs: Iterable[str]) -> List[str]:
    rendered: List[str] = []
    for paragraph in paragraphs:
        if paragraph is None:
            continue
        raw = str(paragraph)
        indent = len(raw) - len(raw.lstrip())
        normalized = _normalize_heading(raw)
        if normalized is None:
            continue
        bullet_normalized = _normalize_bullet_line(normalized, indent)
        rendered.append(bullet_normalized)
        rendered.append("")
    return rendered


def _render_tables(tables: Iterable[Dict[str, Any]]) -> List[str]:
    rendered: List[str] = []
    for table in tables:
        rendered.append(build_html_table(table))
        rendered.append("")
    return rendered


def _render_formulas(formulas: Dict[str, str]) -> List[str]:
    formatted = format_equations(formulas)
    rendered: List[str] = []
    for identifier, content in formatted.items():
        rendered.append(f"$$\n{content}\n$$")
        rendered.append("")
    return rendered


def _render_images(images: Iterable[str]) -> List[str]:
    rendered: List[str] = []
    for idx, _ in enumerate(images, start=1):
        rendered.append(f"|<image_{idx}>|")
        rendered.append("")
    return rendered


def to_markdown(document: Dict[str, Any]) -> str:
    """Convert structured extraction output into Markdown."""
    lines: List[str] = []
    metadata = document.get("metadata", {})
    title = metadata.get("title") or document.get("document_name", "Document")
    lines.append(f"# {title}")
    lines.append("")

    for page in document.get("pages", []):
        page_number = page.get("page_number", 0)
        lines.append(f"## Page {page_number}")
        lines.append("")
        lines.extend(_render_paragraphs(page.get("paragraphs", [])))
        lines.extend(_render_tables(page.get("tables", [])))
        lines.extend(_render_formulas(page.get("formulas", {})))
        lines.extend(_render_images(page.get("images", [])))

    return "\n".join(lines).strip() + "\n"
