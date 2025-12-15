from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# Finde .env im Root-Verzeichnis (2 Ebenen hoch von src/backend/)
root_dir = Path(__file__).parent.parent.parent
env_path = root_dir / ".env"
load_dotenv(dotenv_path=env_path)

# Hol dir die DATABASE_URL aus .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Falls NeonDB einen postgres:// URL gibt, muss es postgresql:// sein
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLAlchemy Engine erstellen
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Prüft Connection vor Benutzung
    echo=False  # Auf True setzen für SQL-Debugging
)

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Class für Models
Base = declarative_base()

# Dependency für FastAPI
def get_db():
    """
    Erstellt eine neue DB Session für jeden Request
    und schließt sie automatisch nach dem Request
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()