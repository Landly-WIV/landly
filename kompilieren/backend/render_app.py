"""
Startpunkt für render.com Deployment
Startet die FastAPI-Anwendung mit uvicorn
"""
import sys
import os
from pathlib import Path

# src/ in den Python-Suchpfad aufnehmen, damit "from backend import ..." funktioniert
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir / "src"))

# Import der FastAPI-App
from backend.main import app  # noqa: E402

# Für lokalen Test
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
