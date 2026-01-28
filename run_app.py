"""
Landly App Starter
==================
Startet Backend (FastAPI) und Frontend (Flet) gemeinsam.

Starten mit:
    python run_app.py

Oder mit uv:
    uv run python run_app.py
"""

import sys
import os
import threading
import time
import signal
import atexit
from pathlib import Path

# ========================================
# 1. Python-Path konfigurieren
# ========================================
ROOT_DIR = Path(__file__).parent
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(SRC_DIR))

# Wechsle ins src-Verzeichnis für relative Pfade
os.chdir(SRC_DIR)

# ========================================
# 2. Backend Server (FastAPI)
# ========================================
import uvicorn

# Globale Variable für Server-Thread
_server_thread = None
_server = None

def start_backend():
    """Startet FastAPI Backend im Hintergrund"""
    global _server
    
    config = uvicorn.Config(
        "src.backend.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="warning",  # Weniger Log-Output
        reload=False
    )
    _server = uvicorn.Server(config)
    _server.run()

def stop_backend():
    """Stoppt den Backend-Server"""
    global _server
    if _server:
        _server.should_exit = True
        print("🛑 Backend wird beendet...")

# Registriere Cleanup-Funktion
atexit.register(stop_backend)

# ========================================
# 3. Flet App starten
# ========================================
import flet as ft
import sites as si


def main(page: ft.Page):
    """Hauptfunktion der Landly App"""
    # Fenster-Konfiguration (Mobile-Ansicht)
    page.padding = 0
    page.window.height = 700
    page.window.width = 360
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Landly - Regionale Bauernhöfe"
    
    # App starten
    page.add(si.appSite(page))


if __name__ == "__main__":
    print("🌾 Starte Landly App...")
    print(f"   Root: {ROOT_DIR}")
    print(f"   Src:  {SRC_DIR}")
    
    # Teste DB-Verbindung
    try:
        from backend.db import engine
        with engine.connect() as conn:
            print("✅ Datenbankverbindung erfolgreich!")
    except Exception as e:
        print(f"❌ Datenbankverbindung fehlgeschlagen: {e}")
        print("   App startet trotzdem, aber ohne DB-Funktionen.")
    
    # Backend im Hintergrund-Thread starten
    print("🚀 Starte Backend-Server auf http://127.0.0.1:8000 ...")
    _server_thread = threading.Thread(target=start_backend, daemon=True)
    _server_thread.start()
    
    # Kurz warten bis Server bereit ist
    time.sleep(1.5)
    print("✅ Backend läuft!")
    
    # Frontend starten (blockiert bis Fenster geschlossen)
    print("📱 Starte Frontend...")
    ft.app(main)
    
    # Cleanup
    stop_backend()
    print("👋 Landly beendet.")
