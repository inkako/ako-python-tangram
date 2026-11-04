from enum import StrEnum


class EnvEnum(StrEnum):
    """Environment enum."""

    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class LogLevelEnum(StrEnum):
    """Log level enum."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFormatterTypeEnum(StrEnum):
    """Log formatter types."""

    SIMPLE = "simple"
    DETAILED = "detailed"
    STRUCTURED = "structured"


class SessionStorage(StrEnum):
    """Session storage types."""

    REDIS = "redis"
    MEMORY = "memory"


class CacheStorage(StrEnum):
    """Cache storage types."""

    REDIS = "redis"
    MEMCACHED = "memcached"
    MEMORY = "memory"


class RateLimiterStorage(StrEnum):
    """Rate limiter storage types."""

    REDIS = "redis"
    MEMORY = "memory"
