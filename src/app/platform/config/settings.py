import logging
import os.path

from app.platform.config.enums import EnvEnum, LogLevelEnum, LogFormatterTypeEnum
from pydantic_settings import BaseSettings
from starlette.config import Config

logger = logging.getLogger(__name__)


def _get_env_path():
    # current file dir
    current_file_dir = os.path.dirname(os.path.realpath(__file__))
    # dir at the same level as src
    project_root = os.path.abspath(os.path.join(current_file_dir, "..", "..", ".."))
    return os.path.join(project_root, ".env")


env_path = _get_env_path()
logger.info(f".env path: {env_path}")

config: Config = Config(env_path)


class EnvironmentSettings(BaseSettings):
    """
    Environment settings
    """
    ENV: EnvEnum = config("ENV", default=EnvEnum.DEV, cast=EnvEnum)


class ApplicationSettings(BaseSettings):
    """
    Application settings
    """
    DEBUG: bool = config("DEBUG", default=False, cast=bool)
    APP_NAME: str = config("APP_NAME", default="TANGRAM PROJECT")
    APP_DESC: str = config("APP_DESC", default="A TANGRAM PROJECT")


class LoggingSettings(BaseSettings):
    """
    Logging settings
    """
    LOG_LEVEL: LogLevelEnum = config("LOG_LEVEL", default=LogLevelEnum.INFO, cast=LogLevelEnum)
    LOG_FORMAT: LogFormatterTypeEnum = config("LOG_FORMAT", default=LogFormatterTypeEnum.DETAILED,
                                              cast=LogFormatterTypeEnum)
    LOG_CONSOLE_ENABLED: bool = config("LOG_CONSOLE_ENABLED", default=True, cast=bool)
    LOG_FILE_ENABLED: bool = config("LOG_FILE_ENABLED", default=False, cast=bool)
    LOG_FILE_NAME: str = config("LOG_FILE_NAME", default="logs/app.log")
    LOG_FILE_MAX_BYTES: int = config("LOG_FILE_MAX_BYTES", default=10485760, cast=int)
    LOG_FILE_BACKUP_COUNT: int = config("LOG_FILE_BACKUP_COUNT", default=10, cast=int)

    # noisy loggers
    LOG_NOISY_LOGGERS: str = config("LOG_NOISY_LOGGERS", default="uvicorn")


class WebServerSettings(BaseSettings):
    """
    Web server settings
    """
    # cors settings
    CORS_ENABLED: bool = config("CORS_ENABLED", default=True, cast=bool)
    CORS_ALLOW_ORIGINS: str = config("CORS_ALLOW_ORIGINS", default="localhost,127.0.0.1")
    CORS_ALLOW_CREDENTIALS: bool = config("CORS_ALLOW_CREDENTIALS", default=True, cast=bool)
    CORS_ALLOW_METHODS: str = config("CORS_ALLOW_METHODS", default="*")
    CORS_ALLOW_HEADERS: str = config("CORS_ALLOW_HEADERS", default="*")

    @property
    def ALLOWED_ORIGINS(self) -> list[str]:
        if not self.CORS_ALLOW_ORIGINS:
            return ["*"]
        return [x.strip() for x in self.CORS_ALLOW_ORIGINS.split(",") if x.strip()]

    @property
    def ALLOWED_METHODS(self) -> list[str]:
        if not self.CORS_ALLOW_METHODS:
            return ["*"]
        return [x.strip() for x in self.CORS_ALLOW_METHODS.split(",") if x.strip()]

    @property
    def ALLOWED_HEADERS(self) -> list[str]:
        if not self.CORS_ALLOW_HEADERS:
            return ["*"]
        return [x.strip() for x in self.CORS_ALLOW_HEADERS.split(",") if x.strip()]

    # gzip settings
    GZIP_ENABLED: bool = config("GZIP_ENABLED", default=True, cast=bool)
    GZIP_MIN_SIZE: int = config("GZIP_MIN_SIZE", default=1024, cast=int)


class AuthenticationSettings(BaseSettings):
    """
    Authentication settings
    """
    SECRET_KEY: str = config("SECRET_KEY", default="set-a-secure-key")

    # session settings
    SESSION_TIMEOUT_MINUTES: int = config("SESSION_TIMEOUT_MINUTES", default=30, cast=int)

    # csrf settings
    CSRF_PROTECTION_ENABLED: bool = config("CSRF_PROTECTION_ENABLED", default=True, cast=bool)


class DatabaseSettings(BaseSettings):
    """
    Database settings
    """
    POSTGRES_USER: str = config("POSTGRES_USER", default="postgres")
    POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="postgres")
    POSTGRES_PREFIX: str = config("POSTGRES_PREFIX", default="postgresql+asyncpg://")
    POSTGRES_SERVER: str = config("POSTGRES_SERVER", default="localhost")
    POSTGRES_PORT: int = config("POSTGRES_PORT", default=5432)
    POSTGRES_DATABASE: str = config("POSTGRES_DATABASE", default="postgres")

    POSTGRES_POOL_SIZE: int = config("POSTGRES_POOL_SIZE", default=20, cast=int)
    POSTGRES_MAX_OVERFLOW: int = config("POSTGRES_MAX_OVERFLOW", default=0, cast=int)

    POSTGRES_ECHO: bool = config("POSTGRES_ECHO", default=False, cast=bool)

    @property
    def DATABASE_URL(self) -> str:
        direct_url = config("DATABASE_URL", default=None)
        if direct_url:
            return direct_url

        return (
            f"{self.POSTGRES_PREFIX}{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"
        )


class Settings(
    EnvironmentSettings,
    ApplicationSettings,
    LoggingSettings,
    WebServerSettings,
    AuthenticationSettings,
    DatabaseSettings,
):
    pass


settings = Settings()


def get_settings() -> Settings:
    return settings
