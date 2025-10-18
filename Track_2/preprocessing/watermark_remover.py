"""Watermark removal utilities."""
from __future__ import annotations

from typing import Any

import numpy as np

try:
    import cv2
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    cv2 = None


def remove_watermarks(page_image: Any) -> Any:
    """Return a cleaned page image with watermarks suppressed.

    The default implementation performs a gentle high-pass filter that reduces
    light, semi-transparent watermarks commonly found on technical PDFs. When
    OpenCV is not available, the function simply returns the input image to
    keep the pipeline functional.
    """
    if cv2 is None or page_image is None:
        return page_image

    image = page_image.copy()
    if isinstance(image, np.ndarray):
        blurred = cv2.GaussianBlur(image, (11, 11), 0)
        cleaned = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)
        return cleaned

    return page_image
