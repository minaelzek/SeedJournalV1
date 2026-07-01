from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.core.middleware import RequestContextMiddleware

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    settings = get_settings()
    logger.info("startup", app_env=settings.app_env, llm_provider=settings.llm_provider)
    yield
    logger.info("shutdown")


app = FastAPI(
    title="SeedJournal API",
    version="0.1.0",
    description="Premium AI-guided reflection journal backend",
    lifespan=lifespan,
)

app.add_middleware(RequestContextMiddleware)
_settings = get_settings()
_cors = ["*"] if _settings.app_env == "development" else _settings.cors_origin_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/v1")


@app.get("/health")
async def health_root() -> dict[str, str]:
    return {"status": "ok"}