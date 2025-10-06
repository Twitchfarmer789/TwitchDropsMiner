# error_logger.py
# Enhanced error logging module with structured detailed logging and rotation
import logging
import sys
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path
import traceback
from typing import Optional

ERROR_LOG_FILE = 'error.log'
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3


class DetailedFormatter(logging.Formatter):
    """Custom formatter that adds detailed exception and context information."""
    def formatException(self, exc_info):
        # Get the full traceback string
        result = super().formatException(exc_info)
        # Add extra divider for clarity
        return f"\n{result}\n{'-'*70}"


def setup_error_logger(
    log_file: str = ERROR_LOG_FILE,
    level: int = logging.ERROR,
    enable_console: bool = True,
    max_bytes: int = MAX_LOG_SIZE,
    backup_count: int = BACKUP_COUNT
) -> logging.Logger:
    """
    Setup a robust error logger with file and optional console output.
    
    Args:
        log_file: path to error log file
        level: logging level (default ERROR)
        enable_console: if True, also log to console (stderr)
        max_bytes: max log file size before rotation
        backup_count: number of backup files to keep
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("TwitchDrops.ErrorLogger")
    logger.setLevel(level)
    
    # Prevent duplicate handlers if setup is called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Detailed formatter
    formatter = DetailedFormatter(
        fmt='%(asctime)s [%(levelname)s] %(name)s - %(funcName)s:%(lineno)d\n%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Rotating file handler
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler (stderr)
    if enable_console:
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def log_exception(
    logger: Optional[logging.Logger] = None,
    message: str = "An error occurred",
    exc_info: bool = True
) -> None:
    """
    Convenience function to log an exception with full traceback.
    
    Args:
        logger: Logger instance (if None, uses default error logger)
        message: Custom error message
        exc_info: If True, includes exception traceback
    """
    if logger is None:
        logger = setup_error_logger()
    logger.error(message, exc_info=exc_info)


def format_error_report(exc: Exception, context: Optional[dict] = None) -> str:
    """
    Format a detailed error report with exception and optional context.
    
    Args:
        exc: Exception instance
        context: Optional dictionary with additional context info
    
    Returns:
        Formatted error report string
    """
    lines = [
        f"Error Report - {datetime.now().isoformat()}",
        f"Exception Type: {type(exc).__name__}",
        f"Exception Message: {str(exc)}",
    ]
    
    if context:
        lines.append("Context:")
        for key, val in context.items():
            lines.append(f"  {key}: {val}")
    
    lines.append("\nTraceback:")
    lines.append(''.join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
    
    return '\n'.join(lines)
