import os
from typing import Optional

class Settings:
    PROJECT_NAME: str = "SkillForge AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Server & Port
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    # Environment & CORS
    ENV: str = os.getenv("ENV", "production" if os.getenv("RENDER") else "development")
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "*")
    
    # External APIs (Read securely from environment)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Optional Remote Database (Supabase PostgreSQL)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    
    # DB configuration: SQLite fallback file (Can point to a Render Persistent Disk path e.g. /var/data/skillforge.db)
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "skillforge.db")
    
settings = Settings()
