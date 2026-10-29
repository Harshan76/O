import os
from typing import Optional

class Settings:
    PROJECT_NAME: str = "SkillForge AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Environment & Keys
    ENV: str = os.getenv("ENV", "development")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # DB configuration: SQLite fallback file
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "skillforge.db")
    
settings = Settings()
