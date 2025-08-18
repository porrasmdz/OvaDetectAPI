import os
from dotenv import load_dotenv

load_dotenv() 

def _env_list(name: str, default: str = ""):
    raw = os.getenv(name, default)
    if not raw:
        return []
    return [x.strip() for x in raw.split(",") if x.strip()]

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "OVA DETECT")

    MODEL_NAME: str = os.getenv("MODEL_NAME", "")
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "app.db")
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "25"))
    SUPPORTED_FILE_TYPES: list[str] = _env_list("SUPPORTED_FILE_TYPES", "pdf")

    # API config
    API_HOST: str = os.getenv("API_HOST", "127.0.0.1")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_BASE_URL: str = os.getenv("API_BASE_URL", "")


settings = Settings()