"""Table detection model wrapper."""
from typing import Any, Dict, List


class TableDetector:
    """Detects table regions inside a document page."""

    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.config = config or {}

    def predict(self, page: Any) -> List[Dict[str, Any]]:
        """Return bounding boxes describing tables on the input page."""
        raise NotImplementedError("Table detection is not implemented yet.")
