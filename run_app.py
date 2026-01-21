"""
Landly App Starter
==================
Startet die Flet-App mit korrekter DB-Anbindung.

Starten mit:
    python run_app.py

Oder mit uv:
    uv run python run_app.py
"""

import sys
import os
from pathlib import Path

# ========================================
# 1. Python-Path konfigurieren
# ========================================
# Füge den src-Ordner zum Python-Path hinzu,
# damit alle Imports korrekt funktionieren
ROOT_DIR = Path(__file__).parent
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

# Wechsle ins src-Verzeichnis für relative Pfade
os.chdir(SRC_DIR)

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
    
    # Starte die App
    ft.app(main)
