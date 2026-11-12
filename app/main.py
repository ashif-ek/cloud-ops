from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="A hands-on DevOps learning project",
    version="1.0.0",
)

app.include_router(router)