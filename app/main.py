from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.db.database import Base, engine
from app.db import models


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.app_name,
    description="CloudOps learning project",
    version="1.0.0",
)

app.include_router(router)