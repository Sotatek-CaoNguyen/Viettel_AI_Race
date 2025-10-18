"""Answer selection model wrapper."""
from typing import Iterable, List, Tuple


class AnswerSelectorModel:
    """Scores candidate answers for multi-label QA."""

    def __init__(self, threshold: float = 0.5) -> None:
        self.threshold = threshold

    def score(self, question: str, options: Iterable[str]) -> List[Tuple[str, float]]:
        """Return scores for each answer option."""
        raise NotImplementedError("Answer scoring is not implemented yet.")
