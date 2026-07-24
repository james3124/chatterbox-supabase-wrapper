from pathlib import Path
import uuid

from app.dependencies import supabase
from app.config import settings


class StorageService:

    def __init__(self):
        self.client = supabase

    def upload_audio(self, wav_path: Path):

        object_name = f"{uuid.uuid4()}.wav"

        with open(wav_path, "rb") as f:

            self.client.storage.from_(
                settings.SUPABASE_STORAGE_BUCKET
            ).upload(
                object_name,
                f,
                {
                    "content-type": "audio/wav"
                },
            )

        public_url = self.client.storage.from_(
            settings.SUPABASE_STORAGE_BUCKET
        ).get_public_url(object_name)

        return object_name, public_url

    def delete_audio(self, storage_path: str):

        self.client.storage.from_(
            settings.SUPABASE_STORAGE_BUCKET
        ).remove([storage_path])


storage_service = StorageService()