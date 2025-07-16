import logging
from typing import Optional


class AlignedFormatter(logging.Formatter):
    """Custom formatter for aligned log output."""

    def format(self, record):
        LEVEL_COLORS = {
            "DEBUG": "\033[94m",
            "INFO": "\033[92m",
            "WARNING": "\033[93m",
            "ERROR": "\033[91m",
            "CRITICAL": "\033[95m",
        }
        RESET = "\033[0m"

        level = record.levelname
        color = LEVEL_COLORS.get(level, "")
        padded_level = f"[{level:<8}]"
        return f"{color}{padded_level} {record.getMessage()}{RESET}"


def setup_logger(log_level: int = logging.INFO) -> logging.Logger:
    """Set up and return a configured logger."""
    logger_name = f"fs_analyzer_{logging.getLevelName(log_level)}"

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # Clear existing handlers
    logger.handlers.clear()

    handler = logging.StreamHandler()
    handler.setFormatter(AlignedFormatter())
    logger.addHandler(handler)
    logger.propagate = False

    return logger
