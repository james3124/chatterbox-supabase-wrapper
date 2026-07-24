import uuid
import os

from fastapi import APIRouter, HTTPException

from app.core.logger import logger
from app.models import TTSRequest
from app.services.chatterbox_service import tts_service
from app.services.storage_service import storage_service
from app.services.database_service import database_service

router = APIRouter(tags=["TTS"])


@router.post("/api/tts")
async def generate(request: TTSRequest):

    request_id = str(uuid.uuid4())

    try:

        wav_path, sample_rate, num_samples = tts_service.generate(
            text=request.text,
            voice_prompt=request.voice,
            exaggeration=request.exaggeration,
            cfg_weight=request.cfg_weight,
            temperature=request.temperature,
        )

        try:
            storage_path, audio_url = storage_service.upload_audio(wav_path)

            duration_ms = int(
                (num_samples / sample_rate) * 1000
            )

            database_service.save_request(
                request_id=request_id,
                text=request.text,
                voice=request.voice or "default",
                duration_ms=duration_ms,
                audio_url=audio_url,
                storage_path=storage_path,
                temperature=request.temperature,
                cfg_weight=request.cfg_weight,
                exaggeration=request.exaggeration,
            )

            return {
                "request_id": request_id,
                "audio_url": audio_url,
                "storage_path": storage_path,
                "duration_ms": duration_ms,
            }
        finally:
            if os.path.exists(str(wav_path)):
                os.remove(wav_path)

    except Exception as e:
        logger.error(
            "TTS generation failed for request %s: %s",
            request_id, str(e), exc_info=e,
        )
        raise HTTPException(
            status_code=500,
            detail="TTS generation failed",
        )