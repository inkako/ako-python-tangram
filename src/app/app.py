from app.apis.backend import app_router
from app.platform import create_app

app = create_app(app_router)