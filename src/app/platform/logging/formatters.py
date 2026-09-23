import json
import logging
import traceback
from datetime import UTC, datetime
from typing import override

from app.platform.config.enums import LogFormatterTypeEnum


class SimpleFormatter(logging.Formatter):
    """A simple log formatter for basic console output."""

    def __init__(self):
        super().__init__(
            fmt="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        )


class DetailedFormatter(logging.Formatter):
    """A detailed log formatter."""

    @override
    def format(self, record: logging.LogRecord) -> str:
        # basic log parts
        timestamp = datetime.now(UTC).isoformat()
        log_parts = [
            f"timestamp={timestamp}",
            f"level={record.levelname}",
            f"thread_id={record.thread}",
            f"process_id={record.process}",
            f"module={record.name}",
            f"function={record.funcName}",
            f"line={record.lineno}",
            f"message={record.msg}",
        ]

        # extra log parts
        extra = getattr(record, "_ctx", {})
        for key, value in extra.items():
            log_parts.append(f"{key}={value}")

        # exception log part
        if record.exc_info:
            exc_text = self.formatException(record.exc_info)
            log_parts.append(f"exception={exc_text}")

        return " ".join(log_parts)


class StructuredFormatter(logging.Formatter):
    """A Structured(JSON) log formatter for machine-readable log output."""

    @override
    def format(self, record: logging.LogRecord) -> str:
        # basic log parts
        log_obj: dict[str, object] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "thread_id": record.thread,
            "process_id": record.process,
            "module": record.name,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.msg,
        }

        # extra log parts
        extra = getattr(record, "_ctx", {})
        log_obj.update(extra)

        # exception log part
        if record.exc_info:
            log_obj["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "stacktrace": traceback.format_exception(*record.exc_info),
            }

        return json.dumps(log_obj, ensure_ascii=False)


def get_formatter(format_type: LogFormatterTypeEnum) -> logging.Formatter:
    formatters: dict[str, type[logging.Formatter]] = {
        LogFormatterTypeEnum.SIMPLE: SimpleFormatter,
        LogFormatterTypeEnum.DETAILED: DetailedFormatter,
        LogFormatterTypeEnum.STRUCTURED: StructuredFormatter,
    }

    formatter_class = formatters.get(format_type)
    if formatter_class is None:
        raise ValueError(
            f"Invalid format type: {format_type}. Available: {', '.join(formatters.keys())}",
        )

    return formatter_class()
