"""
Landly Frontend – Startpunkt für render.com
=============================================
Startet die Flet Web-App auf dem von Render bereitgestellten PORT.
"""
import os
import sys
from pathlib import Path

# src/ in den Python-Suchpfad aufnehmen
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

import flet as ft
import sites as si
import maptest as mt
import threading


def main(page: ft.Page):
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Landly – Regionale Bauernhöfe"

    page.add(si.appSite(page))

    # Standorte im Hintergrund vorladen
    def preload():
        try:
            data = mt.get_standorte_from_db()
            mt._standorte_cache["data"] = data
            mt._standorte_cache["loaded"] = True
            print(f"✅ Standorte vorgeladen: {len(data)}")
        except Exception as e:
            print(f"❌ Fehler beim Vorladen: {e}")

    thread = threading.Thread(target=preload, daemon=True)
    thread.start()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        port=port,
        host="0.0.0.0",
    )
