from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Nexus AI Search Engine Platform"
    DEBUG: bool = False
    SECRET_KEY: str = "nexus_super_secret_jwt_key_2026_change_in_prod"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Secret API Keys (Configured via .env or Environment Variables)
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    GEMINI_API_KEY: str = ""

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/nexus_db"
    REDIS_URL: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
