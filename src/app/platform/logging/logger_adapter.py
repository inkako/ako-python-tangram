import logging
from collections.abc import MutableMapping
from typing import Any, override


class LoggerAdapter(logging.LoggerAdapter):
    """A simple logger adapter to add extra context to log records."""

    def __init__(
            self,
            logger: logging.Logger,
            extra: dict[str, object] | None = None,
            merge_extra: bool = False,
    ) -> None:
        super().__init__(logger, extra, merge_extra)

    @override
    def process(
            self,
            msg: Any,
            kwargs: MutableMapping[str, Any],
    ) -> tuple[Any, MutableMapping[str, Any]]:
        adapter_extra = self.extra if self.extra is not None else {}
        caller_extra = kwargs.get("extra", {})

        merged = {**adapter_extra, **caller_extra}
        kwargs["extra"] = {"_ctx": merged}

        return msg, kwargs
