from pydantic import BaseModel


class TTSRequest(BaseModel):

    text: str

    voice: str | None = None

    exaggeration: float = 0.5

    cfg_weight: float = 0.5

    temperature: float = 0.8


class TTSResponse(BaseModel):

    request_id: str

    audio_url: str

    storage_path: str

    duration_ms: int

    created_at: str