from fastapi import APIRouter, HTTPException

from app.core.logger import logger
from app.services.storage_service import storage_service
from app.services.database_service import database_service

router = APIRouter(tags=["Audio"])


@router.delete("/api/audio/{request_id}")
async def delete_audio(request_id: str):

    try:

        record = database_service.get_request(request_id)

        if not record.data:
            raise HTTPException(
                status_code=404,
                detail="Audio not found",
            )

        storage_path = record.data.get("storage_path")

        if not storage_path:
            raise HTTPException(
                status_code=404,
                detail="Audio file reference not found",
            )

        storage_service.delete_audio(storage_path)

        database_service.delete(request_id)

        return {
            "success": True,
            "deleted": request_id,
        }

    except Exception as e:
        logger.error(
            "Audio deletion failed for %s: %s",
            request_id, str(e), exc_info=e,
        )
        raise HTTPException(
            status_code=500,
            detail="Audio deletion failed",
        )