from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

# ==========================================
# DATABASE ENGINE
# ==========================================

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

# ==========================================
# SESSION FACTORY
# ==========================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ==========================================
# BASE CLASS
# ==========================================

Base = declarative_base()


# ==========================================
# DATABASE DEPENDENCY
# ==========================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()