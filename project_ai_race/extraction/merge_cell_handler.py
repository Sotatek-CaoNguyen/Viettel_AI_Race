"""Utilities for handling merged table cells."""
from __future__ import annotations

from typing import Dict, List


def reconcile_merged_cells(table: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Normalize merged cells back into a regular grid.

    The heuristic fills blanks with the closest non-empty value in the same row,
    mimicking how merged cells should be interpreted after table extraction.
    """
    normalized: Dict[str, List[str]] = {}
    for key, row in table.items():
        filled: List[str] = []
        carry = ""
        for cell in row:
            value = cell.strip()
            if not value:
                value = carry
            else:
                carry = value
            filled.append(value)
        normalized[key] = filled
    return normalized
