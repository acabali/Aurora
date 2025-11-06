from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from aurora.core.config import get_settings
settings = get_settings()
engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
def healthcheck():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
