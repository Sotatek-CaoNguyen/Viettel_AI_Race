"""High-fidelity PDF extraction pipeline leveraging PyMuPDF."""
from __future__ import annotations

import io
import logging
logger = logging.getLogger(__name__)
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple
from collections import deque

try:
    import fitz  # PyMuPDF
except ImportError as exc:
    raise ImportError(
        "PyMuPDF (fitz) is required for the advanced extractor. Install it via 'pip install pymupdf'."
    ) from exc

try:
    from PIL import Image
except ImportError as exc:
    raise ImportError(
        "Pillow is required for image extraction. Install it via 'pip install pillow'."
    ) from exc

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

# Import table extractor
try:
    from .table_extractor import format_table_for_markdown, extract_tables
except ImportError:
    # Fallback
    def format_table_for_markdown(table_data):
        return ""
    def extract_tables(page):
        return []

CONTENT_MARGIN_FRACTION = 0.05

@dataclass
class HeadingCandidate:
    level: Optional[int]
    text: str
    numbering: Optional[str]
    kind: str

HEADER_PATTERNS = (
    re.compile(r"VIETTEL\s+AI\s+RACE\s+TD\d+", re.IGNORECASE),
    re.compile(r"HE\s+DIEU\s+HANH\s+LAN\s+BAN\s+HANH:\s*\d+", re.IGNORECASE),
    re.compile(r"LAN\s+BAN\s+HANH:\s*\d+", re.IGNORECASE),
)

MULTISPACE_RE = re.compile(r"\s+")
HEADING_PATTERN = re.compile(r"^(\d+(?:\.\d+)*)(?:[\.)])?\s+(.*\S)$")
BULLET_MARKERS = ("•", "●", "▪", "o", "-", "*")
NUMERIC_TOKEN = re.compile(r"[0-9~–-]")

def _is_bold_line(line) -> bool:
    spans = [span for span in line.parts if span.text.strip()]
    return bool(spans) and all(span.bold for span in spans)

def _is_numeric_cell(text: str) -> bool:
    return bool(NUMERIC_TOKEN.search(text))

def _content_crop_rect(rect: fitz.Rect) -> fitz.Rect:
    margin = rect.height * CONTENT_MARGIN_FRACTION
    return fitz.Rect(rect.x0, rect.y0 + margin, rect.x1, rect.y1 - margin)

def _extract_two_column_table(entries: Sequence[Dict[str, object]]) -> Optional[List[List[str]]]:
    if len(entries) < 4 or len(entries) % 2 != 0:
        return None

    rows: List[List[str]] = []
    pending: Optional[Dict[str, object]] = None

    for entry in entries:
        plain = str(entry["plain"]).strip()
        formatted = str(entry["formatted"]).strip()
        if not plain:
            continue
        if pending is None:
            pending = entry
            continue

        row_index = len(rows)
        second_is_numeric = _is_numeric_cell(plain)
        if row_index == 0:
            first_is_bold = bool(entry.get("is_bold"))
            pending_is_bold = bool(pending.get("is_bold"))
            is_header_pair = pending_is_bold or first_is_bold or second_is_numeric
            if not is_header_pair:
                return None
        else:
            if not second_is_numeric:
                return None

        left = str(pending["formatted"]).strip()
        right = formatted
        rows.append([left, right])
        pending = None

    if pending is not None or not rows:
        return None
    return rows

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

def _normalize_text_for_signature(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    without_marks = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
    collapsed = MULTISPACE_RE.sub(" ", without_marks)
    return collapsed.strip().upper()

def _is_header_footer(text: str, bbox: Tuple[float, float, float, float], page_rect: fitz.Rect) -> bool:
    if not text.strip():
        return False
    normalized = _normalize_text_for_signature(text)
    if any(pattern.search(normalized) for pattern in HEADER_PATTERNS):
        return True

    margin = max(page_rect.height * CONTENT_MARGIN_FRACTION, 36)
    y0, y1 = bbox[1], bbox[3]
    return y0 <= page_rect.y0 + margin or y1 >= page_rect.y1 - margin

class FormattedTextExtractor:
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

class ImprovedStructureRecognizer:
    """Structure recognizer được cải tiến để xử lý chỉ mục đa cấp độ"""
    
    def __init__(self) -> None:
        self._in_list = False
        self.last_numbering = None
        self.current_level = 0
        self.max_heading_level = 3
        
    def reset_list(self) -> None:
        self._in_list = False

    def _parse_numbering_level(self, numbering: str) -> int:
        """Phân tích cấp độ từ chuỗi đánh số"""
        if '.' in numbering:
            return min(numbering.count('.') + 1, self.max_heading_level)
        else:
            return 1

    def recognize_heading(self, text: str, line: FormattedLine) -> HeadingCandidate:
        stripped = text.strip()
        if not stripped:
            return HeadingCandidate(level=None, text=stripped, numbering=None, kind="none")

        # Pattern cho các định dạng đánh số
        numbering_patterns = [
            r'^(\d+(?:\.\d+)*)(?:[\.\)\s])?\s+(.*\S)$',  # 1, 1.1, 1.1.1
            r'^([IVXLCDM]+)(?:[\.\)\s])?\s+(.*\S)$',     # I, II, III
            r'^([a-z]){1}(?:[\.\)\s])?\s+(.*\S)$',       # a, b, c
        ]

        for pattern in numbering_patterns:
            match = re.match(pattern, stripped, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    numbering, title = match.groups()
                else:
                    continue
                    
                level = self._parse_numbering_level(numbering)
                title_text = title.strip().rstrip(":")
                self.reset_list()
                self.last_numbering = numbering
                self.current_level = level
                return HeadingCandidate(level=level, text=title_text, numbering=numbering, kind="numbered")

        # Kiểm tra heading không đánh số dựa trên formatting
        if line.parts:
            avg_size = sum(span.size for span in line.parts) / len(line.parts)
            is_bold = any(span.bold for span in line.parts)
            is_large = avg_size >= 13
        else:
            avg_size = 0
            is_bold = False
            is_large = False

        if is_large and is_bold:
            self.reset_list()
            level = min(self.current_level + 1 if self.current_level > 0 else 1, self.max_heading_level)
            return HeadingCandidate(level=level, text=stripped.rstrip(":"), numbering=None, kind="bold_large")
        elif is_bold and not self._in_list:
            self.reset_list()
            level = min(3, self.current_level + 1 if self.current_level > 0 else 2)
            return HeadingCandidate(level=level, text=stripped.rstrip(":"), numbering=None, kind="bold")

        return HeadingCandidate(level=None, text=stripped, numbering=None, kind="none")

    def recognize_bullet(self, text: str) -> Tuple[Optional[int], str]:
        stripped = text.strip()
        if not stripped:
            return None, stripped

        leading_spaces = len(text) - len(text.lstrip(" "))
        
        # Bullet markers
        for marker in BULLET_MARKERS:
            if stripped.startswith(marker):
                clean = stripped[len(marker):].strip()
                self._in_list = True
                indent_level = leading_spaces // 4
                return indent_level, clean

        # Numbered list patterns
        numbered_patterns = [
            r'^(\d+)\.\s+(.*)$',
            r'^(\d+)\)\s+(.*)$',
        ]
        
        for pattern in numbered_patterns:
            match = re.match(pattern, stripped)
            if match:
                clean = match.group(2).strip()
                self._in_list = True
                indent_level = leading_spaces // 4
                return indent_level, clean

        # Indentation-based nesting
        if leading_spaces >= 4 and self._in_list:
            indent_level = (leading_spaces // 4)
            return indent_level, stripped

        self._in_list = False
        return None, stripped

NOISE_NUMBERING_PATTERN = re.compile(r"^\**\s*\d+(?:\.\d+)*\.?\**$")

def _is_numbering_noise(formatted: str, plain: str) -> bool:
    formatted_clean = formatted.strip().strip('*').strip()
    plain_clean = plain.strip().strip('*').strip()
    return bool(NOISE_NUMBERING_PATTERN.match(formatted_clean) or NOISE_NUMBERING_PATTERN.match(plain_clean))

def _merge_paragraph_fragments(fragments: Sequence[str]) -> str:
    merged = ''
    for fragment in fragments:
        frag = fragment.strip()
        if not frag:
            continue
        if not merged:
            merged = frag
            continue
        # Giữ nguyên các đoạn văn liền mạch
        merged = merged + ' ' + frag
    return merged.strip()

def _is_figure_caption(text: str) -> bool:
    text = text.strip()
    patterns = [
        r'^Hình\s+\d+\.\d+',
        r'^Hình\s+\d+',
        r'^Figure\s+\d+\.\d+',
        r'^Figure\s+\d+',
    ]
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)

def _find_header_rects(page: fitz.Page) -> List[fitz.Rect]:
    page_rect = page.rect
    candidate_rects: List[fitz.Rect] = []
    blocks = page.get_text("dict").get("blocks", [])
    for block in blocks:
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text", "").strip()
                if not text:
                    continue
                normalized = _normalize_text_for_signature(text)
                if "VIETTEL AI RACE" not in normalized and "LAN BAN HANH" not in normalized:
                    continue
                bbox = span.get("bbox", [])
                if not bbox:
                    continue
                rect = fitz.Rect(
                    page_rect.x0,
                    max(page_rect.y0, bbox[1] - 15),
                    page_rect.x1,
                    min(page_rect.y1, bbox[3] + 25),
                )
                candidate_rects.append(rect)
    merged: List[fitz.Rect] = []
    for rect in candidate_rects:
        merged_flag = False
        for idx, existing in enumerate(merged):
            if rect.intersects(existing):
                merged[idx] = existing | rect
                merged_flag = True
                break
        if not merged_flag:
            merged.append(rect)
    return merged

def _rect_area(rect: fitz.Rect) -> float:
    return max(rect.width, 0.0) * max(rect.height, 0.0)

def _is_image_in_header_region(image_rect: fitz.Rect, header_rects: List[fitz.Rect]) -> bool:
    for header_rect in header_rects:
        if not image_rect.intersects(header_rect):
            continue
        intersection = image_rect & header_rect
        if intersection.is_empty:
            continue
        image_area = max(_rect_area(image_rect), 1.0)
        overlap_ratio = _rect_area(intersection) / image_area
        if overlap_ratio > 0.3:
            return True
    return False

def _crop_image_to_region(image: Image.Image, image_rect: fitz.Rect, crop_rect: fitz.Rect) -> Image.Image | None:
    intersection = fitz.Rect(image_rect)
    intersection &= crop_rect
    if intersection.is_empty:
        return None
    height = image_rect.height or 1
    top_ratio = max(0.0, (intersection.y0 - image_rect.y0) / height)
    bottom_ratio = min(1.0, (intersection.y1 - image_rect.y0) / height)
    upper = int(round(image.height * top_ratio))
    lower = int(round(image.height * bottom_ratio))
    upper = max(0, min(image.height, upper))
    lower = max(upper + 1, min(image.height, lower))
    return image.crop((0, upper, image.width, lower))

class ImageExtractor:
    def __init__(self, images_dir: Path) -> None:
        self.images_dir = images_dir
        self.counter = 1
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def extract(self, page: fitz.Page) -> List[Tuple[float, str]]:
        crop_rect = _content_crop_rect(page.rect)
        header_rects = _find_header_rects(page)

        image_entries: List[Dict[str, object]] = []
        for image_info in page.get_images(full=True):
            xref = image_info[0]
            base_image = page.parent.extract_image(xref)
            image_bytes = base_image.get("image")
            if not image_bytes:
                continue

            rects = []
            try:
                rects = page.get_image_rects(xref) or []
            except Exception:
                rects = []
            if rects:
                image_rect = fitz.Rect(rects[0])
                for extra_rect in rects[1:]:
                    image_rect |= extra_rect
            else:
                image_rect = None
            if image_rect is None or not image_rect.intersects(crop_rect):
                continue
            if _is_image_in_header_region(image_rect, header_rects):
                continue

            try:
                with Image.open(io.BytesIO(image_bytes)) as pil_image:
                    cropped = _crop_image_to_region(pil_image, image_rect, crop_rect)
                    if cropped is None:
                        continue
                    buffer = io.BytesIO()
                    cropped.convert("RGB").save(buffer, format="PNG")
                    processed_bytes = buffer.getvalue()
            except Exception:
                continue

            page_h = float(page.rect.height)
            y_fitz = float(image_rect.y0) if image_rect else 0.0
            y_doctop = page_h - float(image_rect.y1) if image_rect else 0.0
            image_entries.append({
                "y_fitz": y_fitz,
                "y_doctop": y_doctop,
                "bytes": processed_bytes,
            })

        image_entries.sort(key=lambda entry: (entry.get("y_doctop", 0.0), entry.get("y_fitz", 0.0)))

        result: List[Tuple[float, str]] = []
        for entry in image_entries:
            image_name = f"image{self.counter}.png"
            (self.images_dir / image_name).write_bytes(entry["bytes"])
            placeholder = f"![]({{\"images/{image_name}\"}})"
            result.append((entry["y_doctop"], placeholder))
            self.counter += 1

        return result

def _merge_spans(spans: Iterable[FormattedSpan]) -> Tuple[str, str]:
    formatted_parts: List[str] = []
    plain_parts: List[str] = []
    for span in spans:
        text = span.text
        plain_parts.append(text)
        if not text.strip():
            formatted_parts.append(text)
            continue
        # Giữ nguyên bold text
        if span.bold:
            formatted = f"**{text}**"
        elif span.italic:
            formatted = f"_{text}_"
        else:
            formatted = text
        formatted_parts.append(formatted)
    return "".join(formatted_parts), "".join(plain_parts)

class MathAwareMarkdownBuilder:
    """Markdown builder với hỗ trợ công thức toán học LaTeX"""
    
    def __init__(self, title: str) -> None:
        self.lines: List[str] = [f"# {title}", ""]
        self.current_image_group: List[str] = []
        self.in_math_context = False

    def _flush_image_group(self) -> None:
        if self.current_image_group:
            self.lines.extend(self.current_image_group)
            self.lines.append("")
            self.current_image_group.clear()

    def _process_math_content(self, text: str) -> str:
        return text

    def add_heading(self, level: int, text: str) -> None:
        self._flush_image_group()
        hashes = "#" * max(level, 1)
        clean_text = self._process_math_content(text.strip())
        if clean_text:
            self.lines.extend([f"{hashes} {clean_text}", ""])

    def add_paragraph(self, text: str) -> None:
        self._flush_image_group()
        clean_text = self._process_math_content(text.strip())
        if clean_text:
            if _is_math_formula(clean_text):
                self.lines.extend([f"${clean_text}$", ""])
            else:
                self.lines.extend([clean_text, ""])

    def add_bullet(self, indent: int, text: str) -> None:
        self._flush_image_group()
        indent = max(indent, 0)
        clean_text = self._process_math_content(text.strip())
        if not clean_text:
            return
        
        prefix = "  " * indent + "* "
        bullet_text = f"{prefix}{clean_text}"
        
        if _is_math_formula(clean_text):
            bullet_text = f"{prefix}${clean_text}$"
            
        self.lines.extend([bullet_text, ""])

    def add_table(self, rows: List[List[str]]) -> None:
        self._flush_image_group()
        try:
            processed_rows = []
            for row in rows:
                processed_row = [self._process_math_content(str(cell)) for cell in row]
                processed_rows.append(processed_row)
                
            markdown = format_table_for_markdown(processed_rows).strip()
        except Exception:
            return
            
        if markdown:
            self.lines.extend(markdown.splitlines())
            self.lines.append("")

    def add_image_placeholders(self, placeholders: Sequence[str]) -> None:
        for placeholder in placeholders:
            clean_placeholder = placeholder.strip()
            if clean_placeholder:
                self.current_image_group.append(clean_placeholder)

    def build(self) -> str:
        self._flush_image_group()
        cleaned_lines = []
        for line in self.lines:
            if line.strip() or (cleaned_lines and cleaned_lines[-1].strip()):
                cleaned_lines.append(line)
        
        while cleaned_lines and not cleaned_lines[-1].strip():
            cleaned_lines.pop()
            
        return "\n".join(cleaned_lines) + "\n"

class AccuratePDFExtractor:
    """PDF extractor được cải tiến để extract chính xác nội dung"""
    
    def __init__(self, pdf_path: Path, output_dir: Path) -> None:
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.images_dir = self.output_dir / "images"
        self.text_extractor = FormattedTextExtractor()
        self.structure_recognizer = ImprovedStructureRecognizer()
        self.image_extractor = ImageExtractor(self.images_dir)
        self._pdfplumber_doc = None
        
        if pdfplumber is not None:
            try:
                self._pdfplumber_doc = pdfplumber.open(str(self.pdf_path))
            except Exception as exc:
                logging.debug("Failed to open pdfplumber: %s", exc)

    def extract(self) -> str:
        document = fitz.open(self.pdf_path)
        builder = MathAwareMarkdownBuilder(title="Public_026")  # Sửa title cho đúng

        for page in document:
            image_placeholders = deque(self.image_extractor.extract(page))
            clean_blocks = self._get_clean_blocks(page)
            
            table_rows_list, table_cells = self._extract_tables_from_pdfplumber(page.number)

            pending_paragraph: List[str] = []
            pending_figure_caption: Optional[str] = None
            last_heading_level = 0

            def flush_paragraph() -> None:
                if pending_paragraph:
                    paragraph_text = _merge_paragraph_fragments(pending_paragraph)
                    if paragraph_text:
                        builder.add_paragraph(paragraph_text)
                    pending_paragraph.clear()

            def flush_figure() -> None:
                nonlocal pending_figure_caption
                if pending_figure_caption:
                    if image_placeholders:
                        builder.add_image_placeholders([image_placeholders.popleft()[1]])
                    builder.add_paragraph(pending_figure_caption)
                    pending_figure_caption = None

            # Xử lý tables trước
            for rows in table_rows_list:
                flush_paragraph()
                flush_figure()
                builder.add_table(rows)

            for block in clean_blocks:
                lines = self.text_extractor.extract_lines(block)
                line_entries: List[Dict[str, object]] = []

                for line in lines:
                    formatted_text, plain_text = _merge_spans(line.parts)
                    plain_stripped = plain_text.strip()
                    if not plain_stripped:
                        continue
                    if plain_stripped in table_cells:
                        continue
                    line_entries.append({
                        "line": line,
                        "formatted": formatted_text.strip(),
                        "plain": plain_stripped,
                        "is_bold": _is_bold_line(line),
                    })

                if not line_entries:
                    flush_paragraph()
                    flush_figure()
                    continue

                # Kiểm tra two-column table
                table_rows = _extract_two_column_table(line_entries)
                if table_rows:
                    flush_paragraph()
                    flush_figure()
                    builder.add_table(table_rows)
                    continue

                for entry in line_entries:
                    formatted_text = entry["formatted"]
                    plain_text = entry["plain"]
                    line = entry["line"]

                    if _is_numbering_noise(formatted_text, plain_text):
                        continue

                    # Kiểm tra figure caption
                    if _is_figure_caption(plain_text):
                        flush_paragraph()
                        flush_figure()
                        pending_figure_caption = formatted_text
                        continue

                    # Nhận diện heading với improved recognizer
                    heading_candidate = self.structure_recognizer.recognize_heading(plain_text, line)
                    
                    if heading_candidate.level is not None:
                        flush_paragraph()
                        flush_figure()
                        
                        if heading_candidate.kind == "numbered":
                            level = heading_candidate.level
                            last_heading_level = level
                            builder.add_heading(level, heading_candidate.text)
                        elif heading_candidate.kind in ["bold_large", "bold"]:
                            if last_heading_level > 0:
                                level = min(last_heading_level + 1, 3)
                            else:
                                level = 1
                            builder.add_heading(level, heading_candidate.text)
                            last_heading_level = level
                        continue

                    # Kiểm tra bullet
                    bullet_indent, bullet_text = self.structure_recognizer.recognize_bullet(plain_text)
                    if bullet_indent is not None:
                        flush_paragraph()
                        flush_figure()
                        builder.add_bullet(bullet_indent, bullet_text)
                        continue

                    # Văn bản thông thường
                    pending_paragraph.append(formatted_text)

                flush_paragraph()
                flush_figure()

            # Thêm ảnh còn lại
            while image_placeholders:
                _, placeholder = image_placeholders.popleft()
                builder.add_image_placeholders([placeholder])

        document.close()
        if self._pdfplumber_doc is not None:
            self._pdfplumber_doc.close()
        return builder.build()

    def _get_clean_blocks(self, page: fitz.Page) -> List[Dict]:
        """Lấy các block sạch"""
        payload = page.get_text("dict")
        blocks = payload.get("blocks", [])
        page_rect = page.rect
        crop_rect = _content_crop_rect(page_rect)
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
            if _is_header_footer(text, bbox, page_rect):
                continue
            block_rect = fitz.Rect(bbox)
            if not block_rect.intersects(crop_rect):
                continue
            clean_blocks.append(block)
        
        # Sắp xếp theo vị trí
        clean_blocks.sort(key=lambda b: b['bbox'][1])
        return clean_blocks

    def _extract_tables_from_pdfplumber(self, page_number: int) -> Tuple[List[List[List[str]]], Set[str]]:
        """Trích xuất bảng"""
        if self._pdfplumber_doc is None:
            return [], set()
        try:
            pdfplumber_page = self._pdfplumber_doc.pages[page_number]
        except (IndexError, AttributeError):
            return [], set()

        tables = extract_tables(pdfplumber_page)
        collected: List[List[List[str]]] = []
        cell_values: Set[str] = set()
        
        for table in tables:
            rows = table.get("rows", [])
            if not rows:
                continue
                
            all_text = " ".join(" ".join(str(cell) for cell in row) for row in rows).upper()
            if any(pattern.search(all_text) for pattern in HEADER_PATTERNS):
                continue
                
            normalized_rows: List[List[str]] = []
            for row in rows:
                normalized_row = [str(cell).strip() for cell in row if str(cell).strip()]
                if normalized_row:
                    normalized_rows.append(normalized_row)
                    for cell in normalized_row:
                        if cell:
                            cell_values.add(cell)
            
            if len(normalized_rows) >= 2:
                collected.append(normalized_rows)
        
        return collected, cell_values

def extract_pdf_to_markdown(pdf_path: Path, output_dir: Path) -> str:
    """Phiên bản cải tiến để extract chính xác nội dung PDF"""
    extractor = AccuratePDFExtractor(pdf_path, output_dir)
    return extractor.extract()