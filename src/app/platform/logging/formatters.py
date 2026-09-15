import json
import logging
import traceback
from datetime import datetime, UTC

from typing_extensions import override


class SimpleFormatter(logging.Formatter):
    """A simple log formatter for basic console output."""

    def __init__(self):
        super().__init__(
            fmt="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
            datefmt="%H:%M:%S"
        )


class StandardFormatter(logging.Formatter):
    """A standard log formatter."""

    @override
    def format(self, record: logging.LogRecord) -> str:
        # basic log parts
        timestamp = datetime.now(UTC).isoformat()
        log_parts = [
            f"timestamp={timestamp}",
            f"level={record.levelname}",
            f"module={record.name}",
            f"function={record.funcName}",
            f"message={record.message}",
            f"line={record.lineno}",
            f"thread_id={record.thread}",
            f"process_id={record.process}",
        ]

        # extra log parts
        extra = getattr(record, "_extra", {})
        for key, value in extra.items():
            log_parts.append(f"{key}={value}")

        # exception log part
        if record.exc_info:
            exc_text = self.formatException(record.exc_info)
            log_parts.append(f"exception={exc_text}")

        return " ".join(log_parts)


class JsonFormatter(logging.Formatter):
    """A JSON log formatter for machine-readable log output."""

    @override
    def format(self, record: logging.LogRecord) -> str:
        # basic log parts
        log_obj: dict[str, object] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "module": record.name,
            "function": record.funcName,
            "message": record.message,
            "line": record.lineno,
            "thread_id": record.thread,
            "process_id": record.process,
        }

        # extra log parts
        extra = getattr(record, "_extra", {})
        log_obj.update(extra)

        # exception log part
        if record.exc_info:
            log_obj["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": traceback.format_exception(*record.exc_info)
            }

        return json.dumps(log_obj, ensure_ascii=False)
