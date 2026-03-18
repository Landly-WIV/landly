"""
Landly Frontend – Startpunkt für render.com
=============================================
Startet die Flet Web-App auf dem von Render bereitgestellten PORT.
"""
import os
import sys
from pathlib import Path

# src/ in den Python-Suchpfad aufnehmen – MUSS vor allen lokalen Importen stehen
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

# Umgebungsvariablen beim Start ausgeben (hilfreich für Debugging in Render Logs)
api_url = os.environ.get("API_URL", "http://localhost:8000")
port = int(os.environ.get("PORT", 8080))
print(f"🌐 API_URL  = {api_url}")
print(f"🔌 PORT     = {port}")

# Lokale Module erst NACH sys.path-Setup importieren
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


# ft.app() wird IMMER ausgeführt – nicht nur wenn __main__
# Render startet das Skript direkt mit "python render_app.py"
ft.app(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    port=port,
    host="0.0.0.0",
    assets_dir=str(ROOT / "src" / "assets"),
)
