import os
from pydantic import BaseModel
from functools import lru_cache
class Settings(BaseModel):
    env: str = os.getenv("ENV", "dev")
    name: str = os.getenv("AURORA_NAME", "Aurora")
    objective: str = os.getenv("AURORA_OBJECTIVE", "Evolve into SURPA")
    database_url: str = os.getenv("DATABASE_URL")
    redis_url: str = os.getenv("REDIS_URL")
    ingest_local_root: str = os.getenv("INGEST_LOCAL_ROOT", "/app/data")
@lru_cache
def get_settings() -> Settings:
    return Settings()
