"""
Landly Frontend – Haupteinstiegspunkt
======================================
Startet die Flet-App (Desktop / Web / APK).

Starten:
    flet run src/main.py              # Desktop
    flet run --web src/main.py        # Browser
    flet build apk                    # Android APK
"""

import flet as ft
import sys
from pathlib import Path

# Sicherstellen, dass src/ im Suchpfad liegt
SRC_DIR = Path(__file__).parent
sys.path.insert(0, str(SRC_DIR))

import sites as si
import maptest as mt
import threading


def main(page: ft.Page):
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Landly – Regionale Bauernhöfe"

    # App direkt starten
    page.add(si.appSite(page))

    # Standorte im Hintergrund vorladen (für die Map)
    def preload():
        try:
            data = mt.get_standorte_from_db()
            mt._standorte_cache['data'] = data
            mt._standorte_cache['loaded'] = True
            print(f"✅ Standorte vorgeladen: {len(data)}")
        except Exception as e:
            print(f"❌ Fehler beim Vorladen: {e}")

    thread = threading.Thread(target=preload, daemon=True)
    thread.start()


ft.run(main)
