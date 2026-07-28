"""Logging configuration for Multimind AI Platform."""

import sys
from loguru import logger


def get_logger(name: str = __name__) -> "logger":
    """Return a configured logger instance."""
    logger.configure(
        handlers=[
            {"sink": sys.stdout, "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"}
        ]
    )
    return logger
