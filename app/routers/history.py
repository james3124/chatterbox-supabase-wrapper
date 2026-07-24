from fastapi import APIRouter, Query, HTTPException

from app.core.logger import logger
from app.services.database_service import database_service

router = APIRouter(tags=["History"])


@router.get("/api/history")
async def history(limit: int = Query(default=50, le=200)):

    try:
        result = database_service.history(limit)

        return result.data

    except Exception as e:
        logger.error("History fetch failed: %s", str(e), exc_info=e)
        raise HTTPException(status_code=500, detail="Failed to fetch history")