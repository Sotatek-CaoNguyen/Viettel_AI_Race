"""Generic image preprocessing utilities."""
from __future__ import annotations

from typing import Any

import numpy as np

try:
    import cv2
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    cv2 = None


def normalize(image: Any) -> Any:
    """Apply basic normalization steps prior to OCR."""
    if cv2 is None or image is None:
        return image

    array = image if isinstance(image, np.ndarray) else np.array(image)
    grayscale = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY) if array.ndim == 3 else array
    normalized = cv2.normalize(grayscale, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    return normalized
