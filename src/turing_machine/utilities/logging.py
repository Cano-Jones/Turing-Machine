import os
import sys
import warnings

from typing import Literal, TypeAlias
import signal

import logging
logger = logging.getLogger(__name__)

LOG_LEVEL: TypeAlias = (
    Literal[10, 20, 30, 40, 50]
    | Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
)

def logging_setup(logging_level: LOG_LEVEL, path: str | None = None) -> None:
    """
    Setup logging configuration for the application.
    Args:
        logging_level (LOG_LEVEL): The logging level to set.
        path (str | None): Optional path to a log file. If None, logs will be printed to console.
    """
    if isinstance(logging_level, str):
        normalized_level = logging_level.strip().upper()
        numeric_level = getattr(logging, normalized_level, None)
        if numeric_level not in {
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL,
        }:
            raise ValueError(
                "Invalid logging level. Use one of: "
                "DEBUG, INFO, WARNING, ERROR, CRITICAL"
            )
        logging_level = numeric_level
    
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging_level)

    log_format = '(%(relativeCreated)d ms) %(name)s [%(levelname)s]: %(message)s'
    formatter = logging.Formatter(log_format)

    if path:
        log_dir = os.path.dirname(path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        handler = logging.FileHandler(path, mode='w', encoding='utf-8')
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # Route Python warnings, including SciPy ODEintWarning, through logging.
    logging.captureWarnings(True)
    warnings.simplefilter("default")

    # Global exception handler
    def handle_exception(exc_type, exc_value, exc_traceback):
        root_logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception

    # Handle SIGINT (Ctrl+C) gracefully
    def handle_sigint(signum, frame):
        root_logger.warning("Program terminated by Ctrl+C")
        sys.exit(1)

    signal.signal(signal.SIGINT, handle_sigint)

    logger.info("Logging is set up.")

__all__ = ['logging_setup']

if __name__ == "__main__":
    raise NotImplementedError("This module is not intended to be run as a standalone script.")