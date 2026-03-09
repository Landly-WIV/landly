from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# .env suchen: in dieser Datei-Ebene, dann 1-3 Ebenen höher
_here = Path(__file__).parent
for _candidate in [_here, _here.parent, _here.parent.parent, _here.parent.parent.parent]:
    _env = _candidate / ".env"
    if _env.exists():
        load_dotenv(dotenv_path=_env)
        print(f"✅ .env geladen aus: {_env}")
        break
else:
    load_dotenv()  # Fallback: Systemumgebungsvariablen
    print("⚠️  Keine .env Datei gefunden – nutze Systemumgebungsvariablen.")

# DATABASE_URL aus Umgebung lesen
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "\n\n"
        "❌  DATABASE_URL ist nicht gesetzt!\n\n"
        "Bitte lege eine .env Datei im backend/-Ordner an:\n"
        "    cp .env.example .env\n\n"
        "Und trage deine Datenbankverbindung ein, z.B.:\n"
        "    DATABASE_URL=postgresql://user:passwort@host:5432/datenbankname\n"
    )

# NeonDB: postgres:// → postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLAlchemy Engine erstellen
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Prüft Connection vor Benutzung
    echo=False           # Auf True setzen für SQL-Debugging
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
