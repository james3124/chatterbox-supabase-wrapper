from fastapi import APIRouter, HTTPException

from app.config import settings
from app.dependencies import get_supabase_client
from app.services.chatterbox_service import tts_service

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health():

    if tts_service._model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        supabase = get_supabase_client()
        supabase.table("tts_requests").select("count", count="exact").limit(1).execute()
    except Exception:
        raise HTTPException(status_code=503, detail="Supabase unreachable")

    return {
        "status": "ok",
        "provider": "Chatterbox",
        "model": settings.CHATTERBOX_MODEL,
        "version": settings.APP_VERSION,
    }