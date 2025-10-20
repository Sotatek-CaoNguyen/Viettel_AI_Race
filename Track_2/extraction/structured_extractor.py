"""High-fidelity PDF extraction pipeline leveraging PyMuPDF."""
from __future__ import annotations

import io
import logging
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

try:
    import fitz  # PyMuPDF
except ImportError as exc:  # pragma: no cover - library may be absent during linting
    raise ImportError(
        "PyMuPDF (fitz) is required for the advanced extractor. Install it via 'pip install pymupdf'."
    ) from exc

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "Pillow is required for image extraction. Install it via 'pip install pillow'."
    ) from exc


HEADER_PATTERNS = (
    re.compile(r"VIETTEL\s+AI\s+RACE\s+TD\d+", re.IGNORECASE),
    re.compile(r"HE\s+DIEU\s+HANH\s+LAN\s+BAN\s+HANH:\s*\d+", re.IGNORECASE),
    re.compile(r"LAN\s+BAN\s+HANH:\s*\d+", re.IGNORECASE),
)

MULTISPACE_RE = re.compile(r"\s+")
HEADING_PATTERN = re.compile(r"^(\d+(?:\.\d+)*)(?:[\.)])?\s+(.*\S)$")
BULLET_MARKERS = ("•", "●", "▪", "o", "-", "*")

@dataclass
class FormattedSpan:
    text: str
    bold: bool
    italic: bool
    size: float


@dataclass
class FormattedLine:
    parts: List[FormattedSpan]
    bbox: Tuple[float, float, float, float]


@dataclass
class ExtractedItem:
    type: str
    text: Optional[str] = None
    level: Optional[int] = None
    indent: Optional[int] = None
    data: Optional[Dict[str, Sequence[str]]] = None


def _normalize_text_for_signature(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    without_marks = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
    collapsed = MULTISPACE_RE.sub(" ", without_marks)
    return collapsed.strip().upper()


def _is_header_footer(text: str, bbox: Tuple[float, float, float, float], page_height: float) -> bool:
    if not text.strip():
        return False
    normalized = _normalize_text_for_signature(text)
    if any(pattern.search(normalized) for pattern in HEADER_PATTERNS):
        return True

    y0, y1 = bbox[1], bbox[3]
    margin = max(page_height * 0.1, 36)  # safeguard for short pages
    return y0 <= margin or y1 >= (page_height - margin)


class FormattedTextExtractor:
    """Extracts text spans along with lightweight formatting flags."""

    def extract_lines(self, block: Dict) -> List[FormattedLine]:
        lines: List[FormattedLine] = []
        if block.get("type") != 0:
            return lines

        for line in block.get("lines", []):
            spans: List[FormattedSpan] = []
            for span in line.get("spans", []):
                text = span.get("text", "")
                if not text:
                    continue
                font_name = span.get("font", "").lower()
                bold = "bold" in font_name or "bd" in font_name
                italic = "italic" in font_name or "it" in font_name or "oblique" in font_name
                spans.append(
                    FormattedSpan(
                        text=text,
                        bold=bold,
                        italic=italic,
                        size=float(span.get("size", 0.0)),
                    )
                )
            if spans:
                lines.append(FormattedLine(parts=spans, bbox=tuple(line.get("bbox", (0, 0, 0, 0)))))
        return lines


class StructureRecognizer:
    """Infers document structure such as headings and bullet lists."""

    def __init__(self) -> None:
        self._in_list = False

    def recognize_heading(self, text: str, line: FormattedLine) -> Tuple[Optional[int], str]:
        stripped = text.strip()
        if not stripped:
            return None, stripped

        match = HEADING_PATTERN.match(stripped)
        if match:
            numbering, title = match.groups()
            level = 1 if numbering.count(".") == 0 else 2
            return level, title.strip()

        avg_size = sum(span.size for span in line.parts) / len(line.parts)
        if avg_size >= 13 and any(span.bold for span in line.parts):
            return 1, stripped

        return None, stripped

    def recognize_bullet(self, text: str) -> Tuple[Optional[int], str]:
        stripped = text.strip()
        if not stripped:
            return None, stripped

        for marker in BULLET_MARKERS:
            if stripped.startswith(marker):
                clean = stripped[len(marker) :].strip()
                self._in_list = True
                return 0, clean

        leading_spaces = len(text) - len(text.lstrip(" "))
        if leading_spaces >= 4 and self._in_list:
            clean = stripped
            indent = leading_spaces // 2
            return indent, clean

        self._in_list = False
        return None, stripped


class ImageExtractor:
    """Pulls raster images from a PDF page and stores them as JPEGs."""

    def __init__(self, images_dir: Path) -> None:
        self.images_dir = images_dir
        self.counter = 1
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def extract(self, page: fitz.Page) -> List[str]:
        placeholders: List[str] = []
        for image_info in page.get_images(full=True):
            xref = image_info[0]
            base_image = page.parent.extract_image(xref)
            image_bytes = base_image.get("image")
            if not image_bytes:
                continue
            image_ext = base_image.get("ext", "jpeg").lower()

            if image_ext != "jpeg":
                with Image.open(io.BytesIO(image_bytes)) as pil_image:
                    buffer = io.BytesIO()
                    pil_image.convert("RGB").save(buffer, format="JPEG", quality=95)
                    image_bytes = buffer.getvalue()
                    image_ext = "jpeg"

            image_name = f"image{self.counter}.jpeg"
            (self.images_dir / image_name).write_bytes(image_bytes)
            placeholders.append(f"|<image_{self.counter}>|")
            self.counter += 1
        return placeholders


def _merge_spans(spans: Iterable[FormattedSpan]) -> str:
    pieces: List[str] = []
    for span in spans:
        text = span.text
        if not text.strip():
            pieces.append(text)
            continue
        if span.bold and span.italic:
            text = f"_**{text}**_"
        elif span.bold:
            text = f"**{text}**"
        elif span.italic:
            text = f"_{text}_"
        pieces.append(text)
    return "".join(pieces)


class MarkdownBuilder:
    """Accumulates Markdown output pieces based on extracted items."""

    def __init__(self, title: str) -> None:
        self.lines: List[str] = [f"# {title}", ""]

    def add_heading(self, level: int, text: str) -> None:
        hashes = "#" * max(level, 1)
        self.lines.extend([f"{hashes} {text}", ""])

    def add_paragraph(self, text: str) -> None:
        if text:
            self.lines.extend([text.strip(), ""])

    def add_bullet(self, indent: int, text: str) -> None:
        indent = max(indent, 0)
        if indent == 0:
            prefix = "  * "
        else:
            prefix = "* "
        self.lines.extend([f"{prefix}{text.strip()}", ""])

    def add_table(self, rows: Sequence[Sequence[str]]) -> None:
        html_lines = ["<table>", "  <tbody>"]
        for row in rows:
            html_lines.append("    <tr>")
            for cell in row:
                html_lines.append(f"      <td>{cell}</td>")
            html_lines.append("    </tr>")
        html_lines.extend(["  </tbody>", "</table>", ""])
        self.lines.extend(html_lines)

    def add_image_placeholders(self, placeholders: Sequence[str]) -> None:
        for placeholder in placeholders:
            self.lines.extend([placeholder, ""])

    def build(self) -> str:
        while self.lines and not self.lines[-1].strip():
            self.lines.pop()
        return "\n".join(self.lines) + "\n"


@dataclass
class PageExtractionResult:
    paragraphs: List[str] = field(default_factory=list)
    headings: List[Tuple[int, str]] = field(default_factory=list)
    bullets: List[Tuple[int, str]] = field(default_factory=list)
    tables: List[List[List[str]]] = field(default_factory=list)
    images: List[str] = field(default_factory=list)


class PDFExtractor:
    """High-level orchestrator that drives the PyMuPDF-based extraction."""

    def __init__(self, pdf_path: Path, output_dir: Path) -> None:
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.images_dir = self.output_dir / "images"
        self.text_extractor = FormattedTextExtractor()
        self.structure_recognizer = StructureRecognizer()
        self.image_extractor = ImageExtractor(self.images_dir)

    def extract(self) -> str:
        logging.debug("Starting extraction for %s", self.pdf_path)
        document = fitz.open(self.pdf_path)
        builder = MarkdownBuilder(title=self.pdf_path.stem)

        for page in document:
            clean_blocks = self._get_clean_blocks(page)
            image_placeholders = self.image_extractor.extract(page)
            if image_placeholders:
                builder.add_image_placeholders(image_placeholders)

            for block in clean_blocks:
                lines = self.text_extractor.extract_lines(block)
                for line in lines:
                    merged_text = _merge_spans(line.parts)
                    if not merged_text.strip():
                        continue

                    heading_level, heading_text = self.structure_recognizer.recognize_heading(merged_text, line)
                    if heading_level:
                        builder.add_heading(heading_level, heading_text)
                        continue

                    bullet_indent, bullet_text = self.structure_recognizer.recognize_bullet(merged_text)
                    if bullet_indent is not None:
                        builder.add_bullet(bullet_indent, bullet_text)
                        continue

                    builder.add_paragraph(merged_text)

        document.close()
        markdown = builder.build()
        return markdown

    def _get_clean_blocks(self, page: fitz.Page) -> List[Dict]:
        payload = page.get_text("dict")
        blocks = payload.get("blocks", [])
        height = page.rect.height
        clean_blocks: List[Dict] = []
        for block in blocks:
            if block.get("type") != 0:
                continue
            text = "".join(
                span.get("text", "")
                for line in block.get("lines", [])
                for span in line.get("spans", [])
            )
            bbox = tuple(block.get("bbox", (0, 0, 0, 0)))
            if _is_header_footer(text, bbox, height):
                continue
            clean_blocks.append(block)
        return clean_blocks


def extract_pdf_to_markdown(pdf_path: Path, output_dir: Path) -> str:
    """Extract a single PDF into Markdown, returning the Markdown string."""
    extractor = PDFExtractor(pdf_path, output_dir)
    markdown = extractor.extract()
    return markdown
