from app.facade.api import app_router
from app.platform import create_app

app = create_app(app_router)