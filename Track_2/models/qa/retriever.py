"""Vector retrieval model wrapper."""
from typing import Iterable, List, Tuple


class QARetriever:
    """Retrieves relevant document chunks for a question."""

    def __init__(self, top_k: int = 5) -> None:
        self.top_k = top_k

    def embed(self, texts: Iterable[str]) -> List[List[float]]:
        """Generate embeddings for a batch of texts."""
        raise NotImplementedError("Embedding generation is not implemented yet.")

    def retrieve(self, question: str) -> List[Tuple[str, float]]:
        """Return top-k candidate passages for the supplied question."""
        raise NotImplementedError("Retrieval is not implemented yet.")
