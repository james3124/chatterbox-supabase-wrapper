from app.dependencies import supabase
from app.config import settings
from app.core.logger import logger


def validate_environment():

    logger.info("Validating environment...")

    required = [
        ("SUPABASE_URL", settings.SUPABASE_URL),
        ("SUPABASE_SERVICE_ROLE_KEY", settings.SUPABASE_SERVICE_ROLE_KEY),
        ("SUPABASE_STORAGE_BUCKET", settings.SUPABASE_STORAGE_BUCKET),
    ]

    for name, value in required:
        if not value:
            raise RuntimeError(f"Missing required environment variable: {name}")

    logger.info("Environment variables OK. Testing Supabase connectivity...")

    try:
        supabase.table("tts_requests").select("count", count="exact").limit(1).execute()
        logger.info("Supabase connection verified.")
    except Exception as e:
        raise RuntimeError(f"Supabase connectivity check failed: {e}")