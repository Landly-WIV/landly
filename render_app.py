"""
Startpunkt für render.com Deployment
Startet die FastAPI-Anwendung mit uvicorn
"""
import sys
from pathlib import Path

# Root-Verzeichnis zum Python-Pfad hinzufügen
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Import der FastAPI-App
from src.backend.main import app

# Für lokalen Test
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
