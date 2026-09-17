import logging

from app.platform.config.enums import LogFormatterTypeEnum, EnvEnum
from app.platform.config.settings import get_settings, Settings
from app.platform.logging.filters import CorrelationIdFilter
from app.platform.logging.handlers import create_console_handler, create_rotating_file_handler


def _configure_logger_filters():
    """Configure logger filters."""
    correlation_id_filter = CorrelationIdFilter()

    root_logger = logging.getLogger()
    root_logger.addFilter(correlation_id_filter)


def _configure_logger_handlers(settings: Settings) -> None:
    """Configure logger handlers."""
    # determine format type based on environment
    format_type: LogFormatterTypeEnum
    if settings.ENV == EnvEnum.DEV:
        format_type = LogFormatterTypeEnum.SIMPLE
    elif settings.ENV == EnvEnum.TEST:
        format_type = LogFormatterTypeEnum.DETAILED
    elif settings.ENV == EnvEnum.STAGING:
        format_type = LogFormatterTypeEnum.DETAILED
    elif settings.ENV == EnvEnum.PRODUCTION:
        format_type = LogFormatterTypeEnum.STRUCTURED
    else:
        format_type = LogFormatterTypeEnum.DETAILED

    handlers = []

    # console handler
    if settings.LOG_CONSOLE_ENABLED:
        console_handler = create_console_handler(
            format_type=format_type,
            level=settings.LOG_LEVEL,
            use_colors=True,
        )
        handlers.append(console_handler)

    # file handler
    if settings.LOG_FILE_ENABLED:
        file_handler = create_rotating_file_handler(
            filename=settings.LOG_FILE_NAME,
            format_type=format_type,
            level=settings.LOG_LEVEL,
            max_bytes=settings.LOG_FILE_MAX_BYTES,
            backup_count=settings.LOG_FILE_BACKUP_COUNT,
        )
        handlers.append(file_handler)

    root_logger = logging.getLogger()
    for handler in handlers:
        root_logger.addHandler(handler)


def _configure_noisy_logger(settings):
    """Configure third-part package loggers."""
    noisy_loggers = {
        "uvicorn": logging.WARNING,
        "asyncpg": logging.WARNING,
        "sqlalchemy": logging.WARNING,
        "redis": logging.WARNING,
    }

    for logger_name, level in noisy_loggers.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)


def setup_logger_configuration() -> None:
    """Setup logger configuration based on application settings.

    This function configures the root logger by setting up appropriate handlers
    and formatters based on the current environment and settings. It should be
    called only once during application startup.

    Configuration by log settings, suggested defaults:
    - Dev: Console, simple format, DEBUG level
    - Test: Console + file, detailed format, DEBUG level
    - Staging: Console + file, detailed format, INFO level
    - Production: Console + file, structured(JSON) format, INFO level
    """
    settings = get_settings()

    root_logger = logging.getLogger()

    root_logger.filters.clear()
    root_logger.handlers.clear()

    _configure_logger_filters()
    _configure_logger_handlers(settings)

    _configure_noisy_logger(settings)

    root_logger.setLevel(settings.LOG_LEVEL)


def get_configured_logger(name: str) -> logging.Logger:
    """Get a logger that inherits from the configured root logger.

    This function returns a logger that will use the handlers, filters and other configurations
    set up by the `setup_logger_configuration` function.

    Args:
        name (str): The name for the logger.
    Returns:
        logging.Logger: A configured logger instance.
    """
    return logging.getLogger(name)
