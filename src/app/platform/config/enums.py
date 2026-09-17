from enum import StrEnum


class EnvEnum(StrEnum):
    DEV = "dev"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevelEnum(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFormatterTypeEnum(StrEnum):
    SIMPLE = "simple"
    DETAILED = "detailed"
    STRUCTURED = "structured"
