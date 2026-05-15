from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# On utilise toujours SQLite pour la simplicité et la portabilité
# Si DATABASE_URL est défini et valide (postgresql), on l'utilise
# Sinon on tombe sur SQLite
_raw_url = os.getenv("DATABASE_URL", "")

# Corriger le préfixe Railway postgres:// -> postgresql://
if _raw_url.startswith("postgres://"):
    _raw_url = _raw_url.replace("postgres://", "postgresql://", 1)

# Si l'URL PostgreSQL est fournie, utiliser asyncpg-free psycopg2
# Sinon fallback SQLite
if _raw_url.startswith("postgresql://") or _raw_url.startswith("postgresql+"):
    DATABASE_URL = _raw_url
    # Forcer psycopg2 comme driver
    if "+psycopg2" not in DATABASE_URL and "+asyncpg" not in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    connect_args = {}
else:
    # SQLite par défaut (local ou Railway sans DB configurée)
    DATABASE_URL = "sqlite:///./chatbot_auto.db"
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
