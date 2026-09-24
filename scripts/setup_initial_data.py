import asyncio

from app.platform.auth.schemas import UserCreateSchema
from app.platform.auth.service import UserService
from app.platform.config.settings import get_settings
from app.platform.database.session import local_async_session
from app.platform.logging import get_logger

logger = get_logger(__name__)

settings = get_settings()


async def create_first_superuser() -> None:
    """Create the first superuser."""
    try:
        name = settings.ADMIN_NAME
        email = settings.ADMIN_EMAIL
        phone = settings.ADMIN_PHONE
        username = settings.ADMIN_USERNAME
        password = settings.ADMIN_PASSWORD

        if not all([name, email, phone, username, password]):
            logger.warning("Admin configuration is incomplete. Please check environment variables.")
            return

        user_service = UserService()
        async with local_async_session() as session:
            user_create_schema = UserCreateSchema(
                name=name,
                email=email,
                phone=phone,
                username=username,
                password=password,
            )
            created_user = await user_service.create_user(session, user_create_schema)
            logger.info(f"Superuser created successfully: {created_user}")
    except Exception as e:
        logger.error(f"Error creating superuser: {e}")


async def setup_initial_data():
    """Set up initial data for the application."""
    logger.info("Setting up initial data...")

    logger.info("Creating first superuser...")
    await create_first_superuser()

    logger.info("Initial data setup completed.")


if __name__ == "__main__":
    asyncio.run(setup_initial_data())
