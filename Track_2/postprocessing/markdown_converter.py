"""Markdown conversion helpers."""
from __future__ import annotations

from typing import Any, Dict, Iterable, List

from .html_table_builder import build_html_table
from .latex_formatter import format_equations


def _render_paragraphs(paragraphs: Iterable[str]) -> List[str]:
    rendered: List[str] = []
    for paragraph in paragraphs:
        rendered.append(paragraph.strip())
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
    for idx, image in enumerate(images):
        placeholder = f"|<image_{idx}>|"
        rendered.append(f"![{placeholder}]({image})")
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
