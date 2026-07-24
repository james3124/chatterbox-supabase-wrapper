from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings

from app.routers.health import router as health_router
from app.routers.tts import router as tts_router
from app.routers.history import router as history_router
from app.routers.audio import router as audio_router
from app.exceptions.handlers import register_exception_handlers
from app.middleware.logging import LoggingMiddleware

from app.core.startup import startup
from app.core.shutdown import shutdown


@asynccontextmanager
async def lifespan(app: FastAPI):

    await startup()

    yield

    await shutdown()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

register_exception_handlers(app)

app.add_middleware(LoggingMiddleware)
app.include_router(health_router)
app.include_router(tts_router)
app.include_router(history_router)
app.include_router(audio_router)

@app.get("/")
async def root():

    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }