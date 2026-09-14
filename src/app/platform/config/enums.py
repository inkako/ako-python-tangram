from enum import StrEnum


class EnvironmentEnum(StrEnum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevelEnum(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFormatEnum(StrEnum):
    SIMPLE = "simple"
    STANDARD = "standard"
    DETAILED = "detailed"
    STRUCTURED = "structured"