"""Local vector index builders."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


@dataclass
class VectorIndex:
    """Simple in-memory TF-IDF index."""

    vectorizer: TfidfVectorizer
    matrix: np.ndarray
    chunks: List[str]


def build_index(chunks: Iterable[str]) -> VectorIndex:
    """Build a persistent vector index from document chunks."""
    chunk_list = [chunk.strip() for chunk in chunks if chunk and chunk.strip()]
    vectorizer = TfidfVectorizer(
        max_features=4096,
        ngram_range=(1, 2),
        lowercase=True,
        stop_words="english",
    )
    matrix = vectorizer.fit_transform(chunk_list).astype(np.float32)
    return VectorIndex(vectorizer=vectorizer, matrix=matrix, chunks=chunk_list)
