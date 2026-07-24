from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "Chatterbox Supabase Wrapper"

    APP_VERSION: str = "4.0.0"

    PORT: int = 10000

    CHATTERBOX_MODEL: str = "turbo"

    CHATTERBOX_DEVICE: str = "cpu"

    SUPABASE_URL: str

    SUPABASE_SERVICE_ROLE_KEY: str

    SUPABASE_STORAGE_BUCKET: str = "tts-audio"

    class Config:
        env_file = ".env"


settings = Settings()