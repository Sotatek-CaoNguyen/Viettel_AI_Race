"""High level table extraction routines."""
from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd


def extract_tables(page: Any) -> List[Dict[str, Any]]:
    """Extract table structures from a pdfplumber page."""
    if not hasattr(page, "extract_tables"):
        return []

    tables: List[Dict[str, Any]] = []
    raw_tables = page.extract_tables()
    for idx, table in enumerate(raw_tables):
        if not table:
            continue
        frame = pd.DataFrame(table).fillna("")
        tables.append(
            {
                "id": f"table_{page.page_number}_{idx}",
                "rows": frame.values.tolist(),
                "shape": frame.shape,
            }
        )
    return tables
