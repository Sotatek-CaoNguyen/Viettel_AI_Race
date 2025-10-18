"""Central logging configuration."""
import logging


def configure_logging(level: int = logging.INFO) -> None:
    """Configure the root logger with a sensible formatter."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
