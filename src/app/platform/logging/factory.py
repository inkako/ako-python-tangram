import logging
import threading

from app.platform.config.settings import get_settings
from app.platform.logging import logger_adapter
from app.platform.logging.config import get_configured_logger, setup_logger_configuration

_logger_configured = False
_configuration_lock = threading.Lock()


def configure_logger():
    global _logger_configured

    with _configuration_lock:
        if not _logger_configured:
            # Configure logger
            setup_logger_configuration()
            _logger_configured = True

            # Log logger configured log message
            logger = logging.getLogger(__name__)
            settings = get_settings()
            logger.info(
                msg=f"Logger configured for [{settings.ENV}] environment!",
                extra={
                    "env": settings.ENV,
                    "log_level": settings.LOG_LEVEL,
                    "log_format": settings.LOG_FORMAT,
                    "log_file_name": settings.LOG_FILE_NAME,
                    "log_file_max_bytes": settings.LOG_FILE_MAX_BYTES,
                    "log_file_backup_count": settings.LOG_FILE_BACKUP_COUNT,
                    "log_console_enabled": settings.LOG_CONSOLE_ENABLED,
                    "log_file_enabled": settings.LOG_FILE_ENABLED,
                },
            )


def _ensure_logger_configured():
    if not _logger_configured:
        configure_logger()


def get_logger(name: str, **extra_context) -> logging.Logger | logging.LoggerAdapter:
    """Get a logger with the given name and extra context.

    Args:
        name (str): The name of the logger.
        **extra_context: Extra context to be added to the logger.

    Returns:
        logging.Logger | logging.LoggerAdapter: The logger.
    """
    _ensure_logger_configured()

    base_logger = get_configured_logger(name)

    logger: logging.Logger | logging.LoggerAdapter
    if extra_context:
        logger = logger_adapter.LoggerAdapter(base_logger, extra_context)
    else:
        logger = base_logger

    return logger
