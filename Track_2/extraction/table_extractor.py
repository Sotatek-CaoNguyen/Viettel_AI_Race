"""Table extraction helpers with header filtering and continuation support."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

import pandas as pd

HEADER_FOOTER_PATTERNS = [
    re.compile(r"VIETTEL\s+AI\s+RACE", re.IGNORECASE),
    re.compile(r"TD\d+", re.IGNORECASE),
    re.compile(r"LAN\s+BAN\s+HANH:\s*\d+", re.IGNORECASE),
    re.compile(r"GII THIU", re.IGNORECASE),
    re.compile(r"TRANG\s*\d+", re.IGNORECASE),
    re.compile(r"PAGE\s*\d+", re.IGNORECASE),
    re.compile(r"\d{4}-\d{2}-\d{2}"),
]


@dataclass
class TableCandidate:
    rows: List[List[str]]
    bbox: Tuple[float, float, float, float]
    page_number: int
    table_id: str
    header: Optional[List[str]] = None


def _clean_rows(table: Sequence[Sequence[Any]]) -> List[List[str]]:
    cleaned: List[List[str]] = []
    for row in table:
        cleaned_row = [str(cell).strip() if cell is not None else "" for cell in row]
        if any(cell for cell in cleaned_row):
            cleaned.append(cleaned_row)
    return cleaned


def extract_tables(page: Any) -> List[Dict[str, Any]]:
    if page is None or not hasattr(page, "extract_tables"):
        return []

    tables: List[Dict[str, Any]] = []
    raw_tables = page.extract_tables()
    for idx, table in enumerate(raw_tables):
        if not table:
            continue
        cleaned = _clean_rows(table)
        if not cleaned:
            continue
        frame = pd.DataFrame(cleaned).fillna("")
        tables.append(
            {
                "id": f"table_{getattr(page, 'page_number', idx)}_{idx}",
                "rows": frame.values.tolist(),
                "shape": frame.shape,
                "bbox": _get_table_bbox(page, idx),
            }
        )
    return tables


def _get_table_bbox(page: Any, table_index: int) -> Tuple[float, float, float, float]:
    try:
        if hasattr(page, 'find_tables'):
            tables = page.find_tables()
            if 0 <= table_index < len(tables):
                rect = tables[table_index].bbox
                return (rect[0], rect[1], rect[2], rect[3])
    except Exception:
        pass
    return (0.0, 0.0, 0.0, 0.0)


def is_valid_table(table_data: List[List[str]]) -> bool:
    if not table_data or len(table_data) < 2:
        return False
    num_cols = len(table_data[0])
    if num_cols < 2:
        return False
    valid_rows = 0
    for row in table_data:
        non_empty = sum(1 for cell in row if cell and cell.strip())
        if non_empty >= 2:
            valid_rows += 1
    return valid_rows >= 2


def is_table_header_footer(table_data: List[List[str]], page_number: int) -> bool:
    all_text = " ".join(" ".join(row) for row in table_data)
    for pattern in HEADER_FOOTER_PATTERNS:
        if pattern.search(all_text):
            return True
    if len(table_data) == 1 and len(table_data[0]) == 1:
        cell = table_data[0][0].strip()
        if cell.isdigit() and int(cell) == page_number + 1:
            return True
    return False


def detect_table_continuation(current_table: List[List[str]], next_table: List[List[str]]) -> bool:
    if not current_table or not next_table:
        return False
    if len(current_table[0]) != len(next_table[0]):
        return False
    last_row = current_table[-1]
    first_row = next_table[0]
    if len(last_row) != len(first_row):
        return False
    if not all(cell.strip() for cell in last_row):
        return False
    if not all(cell.strip() for cell in first_row):
        return False
    return True


def merge_tables(table1: List[List[str]], table2: List[List[str]]) -> List[List[str]]:
    merged = list(table1)
    if table1 and table2 and table1[0] == table2[0]:
        merged.extend(table2[1:])
    else:
        merged.extend(table2)
    return merged


def normalize_table_cells(table_data: List[List[str]]) -> List[List[str]]:
    normalized: List[List[str]] = []
    for row in table_data:
        normalized.append([
            re.sub(r"\s+", " ", str(cell).strip()).replace("|", "\\|")
            for cell in row
        ])
    return normalized


def format_table_for_markdown(table_data: List[List[str]]) -> str:
    if not table_data:
        return ""
    normalized = normalize_table_cells(table_data)
    header = normalized[0]
    lines = [f"| {' | '.join(header)} |"]
    separator = ["---"] * len(header)
    lines.append(f"| {' | '.join(separator)} |")
    for row in normalized[1:]:
        if len(row) < len(header):
            row = row + [""] * (len(header) - len(row))
        elif len(row) > len(header):
            row = row[:len(header)]
        lines.append(f"| {' | '.join(row)} |")
    return "\n".join(lines) + "\n"


class TableExtractor:
    def __init__(self) -> None:
        self.current_table: Optional[TableCandidate] = None

    def process_page(self, page: Any, page_number: int) -> Tuple[List[str], Set[str]]:
        markdown_tables: List[str] = []
        cell_values: Set[str] = set()
        tables = extract_tables(page)
        for table in tables:
            rows = _clean_rows(table.get("rows", []))
            if not rows or not is_valid_table(rows):
                continue
            if is_table_header_footer(rows, page_number):
                continue
            for row in rows:
                for cell in row:
                    if cell:
                        cell_values.add(cell.strip())

            if (
                self.current_table
                and page_number <= self.current_table.page_number + 1
                and detect_table_continuation(self.current_table.rows, rows)
            ):
                self.current_table.rows = merge_tables(self.current_table.rows, rows)
                self.current_table.page_number = page_number
            else:
                if self.current_table:
                    markdown_tables.append(format_table_for_markdown(self.current_table.rows))
                self.current_table = TableCandidate(
                    rows=rows,
                    bbox=table.get("bbox", (0.0, 0.0, 0.0, 0.0)),
                    page_number=page_number,
                    table_id=table["id"],
                    header=rows[0] if rows else None,
                )
        return markdown_tables, cell_values

    def finish_extraction(self) -> List[str]:
        markdown_tables: List[str] = []
        if self.current_table:
            markdown_tables.append(format_table_for_markdown(self.current_table.rows))
            self.current_table = None
        return markdown_tables
