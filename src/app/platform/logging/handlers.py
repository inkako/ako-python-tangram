import logging
import logging.handlers
import sys
from logging import LogRecord
from pathlib import Path

from app.platform.config.enums import LogFormatterTypeEnum, LogLevelEnum
from app.platform.logging.formatters import get_formatter


class ColoredConsoleHandler(logging.StreamHandler):
    """A console handler with color support."""

    COLORS = {
        # Cyan
        "DEBUG": "\033[36m",
        # Green
        "INFO": "\033[32m",
        # Yellow
        "WARNING": "\033[33m",
        # Red
        "ERROR": "\033[31m",
        # Magenta
        "CRITICAL": "\033[35m",
    }
    # close the color
    RESET = "\033[0m"

    def __init__(self, stream=None):
        super().__init__(stream or sys.stdout)
        self.use_colors = self._can_use_colors()

    def _can_use_colors(self) -> bool:
        return hasattr(self.stream, "isatty") and self.stream.isatty() and sys.platform != "win32"

    def format(self, record: LogRecord) -> str:
        formatted = super().format(record)
        if self.use_colors and record.levelname in self.COLORS:
            color = self.COLORS[record.levelname]
            formatted = formatted.replace(f"[{record.levelname}]", f"[{color}{record.levelname}{self.RESET}]")
        return formatted


def create_console_handler(
        format_type: LogFormatterTypeEnum = LogFormatterTypeEnum.DETAILED,
        level: LogLevelEnum = LogLevelEnum.INFO,
        use_colors: bool = True,
) -> logging.Handler:
    """
    Create a console handler with the given format type, level, and color settings.

    Args:
        format_type (LogFormatterTypeEnum): The format type for the log messages.
        level (LogLevelEnum): The logging level.
        use_colors (bool): Whether to use colors in the console output.

    Returns:
        logging.Handler: The created console handler.
    """
    handler: logging.Handler
    if use_colors:
        handler = ColoredConsoleHandler()
    else:
        handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(get_formatter(format_type))
    return handler


class RotatingFileHandler(logging.handlers.RotatingFileHandler):
    """Enhanced rotating file handler with automatic directory creation."""

    def __init__(
            self,
            filename: str,
            max_bytes: int = 104857600,
            backup_count: int = 10,
            encoding: str = "utf-8",
    ):
        log_path = Path(filename)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        super().__init__(filename, maxBytes=max_bytes, backupCount=backup_count, encoding=encoding)


def create_rotating_file_handler(
        filename: str,
        format_type: LogFormatterTypeEnum = LogFormatterTypeEnum.DETAILED,
        level: LogLevelEnum = LogLevelEnum.INFO,
        max_bytes: int = 104857600,
        backup_count: int = 10,
        encoding: str = "utf-8",
) -> logging.Handler:
    """
    Create a rotating file handler with the given format type, level, and file size settings.

    Args:
        filename (str): The path to the log file.
        format_type (LogFormatterTypeEnum): The format type for the log messages.
        level (LogLevelEnum): The logging level.
        max_bytes (int): The maximum file size in bytes before rotation.
        backup_count (int): The number of backup files to keep.
        encoding (str): The encoding for the log file.

    Returns:
        logging.Handler: The created rotating file handler.
    """
    handler: logging.Handler = RotatingFileHandler(filename, max_bytes, backup_count, encoding)
    handler.setLevel(level)
    handler.setFormatter(get_formatter(format_type))
    return handler
