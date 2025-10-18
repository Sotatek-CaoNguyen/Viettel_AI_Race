"""HTML table rendering utilities."""
from __future__ import annotations

import html
from typing import Dict, Iterable, List

from ..extraction.merge_cell_handler import reconcile_merged_cells


def _escape_row(row: Iterable[str]) -> List[str]:
    return [html.escape(str(cell)) for cell in row]


def build_html_table(table: Dict[str, object]) -> str:
    """Turn normalized table data into an HTML string."""
    rows = table.get("rows", [])
    if not rows:
        return "<table></table>"

    normalized_rows = reconcile_merged_cells({str(idx): list(map(str, row)) for idx, row in enumerate(rows)})

    html_lines = ["<table>", "  <tbody>"]
    for idx in range(len(normalized_rows)):
        row = normalized_rows[str(idx)]
        escaped = _escape_row(row)
        html_lines.append("    <tr>")
        for cell in escaped:
            html_lines.append(f"      <td>{cell}</td>")
        html_lines.append("    </tr>")
    html_lines.append("  </tbody>")
    html_lines.append("</table>")
    return "\n".join(html_lines)
