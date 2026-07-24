from datetime import datetime, timezone
from app.dependencies import supabase
from app.config import settings


class DatabaseService:

    def __init__(self):
        self.client = supabase
        self.table = "tts_requests"

    def save_request(
        self,
        request_id: str,
        text: str,
        voice: str,
        duration_ms: int,
        audio_url: str,
        storage_path: str,
        temperature: float,
        cfg_weight: float,
        exaggeration: float,
    ):

        preview = text[:200]

        data = {
            "id": request_id,
            "text_preview": preview,
            "voice": voice,
            "duration_ms": duration_ms,
            "audio_url": audio_url,
            "storage_path": storage_path,
            "temperature": temperature,
            "cfg_weight": cfg_weight,
            "exaggeration": exaggeration,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        self.client.table(self.table).insert(data).execute()

        return data

    def history(self, limit: int = 50):

        return (
            self.client
            .table(self.table)
            .select("*")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )

    def get_request(self, request_id: str):

        return (
            self.client
            .table(self.table)
            .select("*")
            .eq("id", request_id)
            .single()
            .execute()
        )

    def delete(self, request_id: str):

        return (
            self.client
            .table(self.table)
            .delete()
            .eq("id", request_id)
            .execute()
        )


database_service = DatabaseService()