"""Answer selection helpers."""
from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

Option = Tuple[str, str]


def _build_corpus(question: str, options: Sequence[Option], context: Iterable[str]) -> List[str]:
    context_text = " ".join(context).strip()
    corpus: List[str] = [question]
    if context_text:
        corpus[0] = f"{question} {context_text}"
    for _, option_text in options:
        corpus.append(f"{question} {option_text}")
    return corpus


def select_answers(
    question: str,
    options: Sequence[Option],
    *,
    context: Iterable[str] | None = None,
    base_threshold: float = 0.35,
) -> List[Tuple[str, float]]:
    """Return answers that exceed the multi-label threshold."""
    if not options:
        return []

    context_parts = list(context or [])
    corpus = _build_corpus(question, options, context_parts)

    vectorizer = TfidfVectorizer(max_features=2048, ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(corpus)
    if matrix.shape[0] <= 1:
        return []

    question_vec = matrix[0]
    option_matrix = matrix[1:]
    scores = cosine_similarity(question_vec, option_matrix).flatten()

    dynamic_threshold = base_threshold
    if scores.size:
        max_score = scores.max()
        dynamic_threshold = max(dynamic_threshold, max_score * 0.6)

    selected: List[Tuple[str, float]] = []
    for (label, _), score in zip(options, scores):
        if score >= dynamic_threshold:
            selected.append((label, float(score)))

    if not selected and scores.size:
        best_idx = int(scores.argmax())
        label = options[best_idx][0]
        selected.append((label, float(scores[best_idx])))
    return selected
