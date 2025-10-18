"""Page segmentation helpers."""
from __future__ import annotations

from typing import Any, Dict, List


def segment_page(page: Any) -> List[Dict[str, Any]]:
    """Split a pdfplumber page into logical blocks for downstream extraction."""
    segments: List[Dict[str, Any]] = []

    if hasattr(page, "extract_tables"):
        segments.append(
            {
                "type": "table_candidates",
                "bboxes": [
                    {"x0": table.bbox[0], "y0": table.bbox[1], "x1": table.bbox[2], "y1": table.bbox[3]}
                    for table in getattr(page, "find_tables", lambda **_: [])(
                        table_settings={"snap_tolerance": 3}
                    )
                ],
            }
        )

    text = getattr(page, "extract_text", lambda **_: "")(x_tolerance=3, y_tolerance=3) or ""
    if text.strip():
        segments.append({"type": "text", "content": text})

    if hasattr(page, "images") and page.images:
        segments.append({"type": "images", "items": page.images})

    return segments
