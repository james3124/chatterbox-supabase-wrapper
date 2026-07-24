import asyncio

from app.services.chatterbox_service import tts_service
from app.core.logger import logger
from app.utils.validator import validate_environment


async def startup():

    logger.info("Starting Chatterbox Wrapper...")

    await asyncio.to_thread(validate_environment)

    logger.info("Loading Chatterbox Turbo model...")

    await asyncio.to_thread(tts_service.load)

    logger.info("Startup completed.")