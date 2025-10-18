"""Question parsing helpers."""
from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

Option = Tuple[str, str]
ParsedQuestion = Tuple[str, List[Option]]


def parse_questions(rows: Iterable[Sequence[str]]) -> List[ParsedQuestion]:
    """Convert raw CSV rows into question + options tuples.

    Each row is expected to contain the question followed by up to four answer
    options (A, B, C, D). Header rows are skipped automatically.
    """
    parsed: List[ParsedQuestion] = []
    for row in rows:
        if not row:
            continue
        question = str(row[0]).strip()
        if not question:
            continue
        lowered = question.lower()
        if lowered == "question" or lowered.startswith("question "):
            continue

        labels = ["A", "B", "C", "D"]
        options: List[Option] = []
        for idx, label in enumerate(labels):
            try:
                value = str(row[idx + 1]).strip()
            except IndexError:
                value = ""
            if value:
                options.append((label, value))
        parsed.append((question, options))
    return parsed
