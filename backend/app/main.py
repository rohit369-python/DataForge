"""FastAPI application factory and router registration for DataPulse."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import health, monitoring, pipelines, sources
from backend.app.core.config import settings
from backend.app.core.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables when the application starts."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Automated data engineering and analytics platform",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(sources.router)
app.include_router(pipelines.router)
app.include_router(monitoring.router)
