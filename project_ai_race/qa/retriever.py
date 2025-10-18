"""Retrieval utilities for the QA pipeline."""
from __future__ import annotations

from typing import List, Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .indexer import VectorIndex


def retrieve(index: VectorIndex, question: str, top_k: int = 5) -> List[Tuple[str, float]]:
    """Fetch candidate passages with similarity scores."""
    if not question.strip():
        return []

    query_vec = index.vectorizer.transform([question]).astype(np.float32)
    similarities = cosine_similarity(query_vec, index.matrix).flatten()
    top_indices = np.argsort(similarities)[::-1][:top_k]
    return [(index.chunks[idx], float(similarities[idx])) for idx in top_indices if similarities[idx] > 0.0]
