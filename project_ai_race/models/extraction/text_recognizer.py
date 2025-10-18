"""Lightweight OCR/text recognizer wrapper."""
from typing import Any, Dict


class TextRecognizer:
    """Recognizes textual content within detected regions."""

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.config = config or {}

    def recognize(self, image: Any) -> str:
        """Run OCR on the provided image region."""
        raise NotImplementedError("Text recognition is not implemented yet.")
