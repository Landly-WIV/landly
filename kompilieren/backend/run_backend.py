"""
Landly Backend – Startdatei
============================
Startet den FastAPI-Server via Uvicorn.

Lokal starten:
    python run_backend.py

Oder direkt mit Uvicorn:
    uvicorn src.backend.main:app --reload --host 0.0.0.0 --port 8000

Auf Render / Production wird render.yaml verwendet.
"""

import sys
from pathlib import Path

# src/ in den Python-Suchpfad aufnehmen damit "from backend import ..." funktioniert
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import uvicorn

if __name__ == "__main__":
    print("🚀 Starte Landly Backend auf http://0.0.0.0:8000 ...")
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
