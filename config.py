from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "sqlite:///./ai_studio.db"
    secret_key: str = "dev-secret-key-change-in-production-32-chars-min"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    gemini_api_key: Optional[str] = "your-gemini-api-key-here"
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
