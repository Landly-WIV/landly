"""
Landly Frontend – Startpunkt für render.com
"""
import os
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

api_url = os.environ.get("API_URL", "http://localhost:8000")
port = int(os.environ.get("PORT", 8080))
print(f"🌐 API_URL  = {api_url}")
print(f"🔌 PORT     = {port}")

import flet as ft
import httpx
import sites as si
import maptest as mt


def wake_up_backend(api_url: str, on_ready, on_error):
    """Pingt das Backend bis es antwortet, dann ruft on_ready() auf."""
    print("🔔 Wecke Backend auf...")
    max_versuche = 20       # max. ~60 Sekunden warten
    wartezeit = 3           # Sekunden zwischen Versuchen

    for versuch in range(1, max_versuche + 1):
        try:
            res = httpx.get(f"{api_url}/", timeout=5)
            if res.status_code < 500:
                print(f"✅ Backend ist bereit! (Versuch {versuch})")
                on_ready()
                return
        except Exception as e:
            print(f"⏳ Versuch {versuch}/{max_versuche} – Backend schläft noch: {e}")
        time.sleep(wartezeit)

    print("❌ Backend nicht erreichbar nach maximalem Warten")
    on_error()


def main(page: ft.Page):
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Landly – Regionale Bauernhöfe"

    # ── Ladescreen ──────────────────────────────────────────────
    loading_view = ft.Container(
        expand=True,
        bgcolor="#f9fafb",
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(
                    src="icon.png",
                    width=80,
                    height=80,
                    fit=ft.ImageFit.CONTAIN,
                    error_content=ft.Text("🌱", size=60),
                ),
                ft.Container(height=20),
                ft.Text(
                    "Landly wird gestartet...",
                    size=20,
                    weight=ft.FontWeight.W_600,
                    color="#2D5016",
                ),
                ft.Container(height=8),
                ft.Text(
                    "Der Server wird aufgeweckt, bitte einen Moment Geduld.",
                    size=14,
                    color="#6B7280",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=24),
                ft.ProgressRing(color="#6B8E23", width=36, height=36),
            ],
        ),
    )

    page.add(loading_view)
    page.update()

    # ── Callbacks ──────────────────────────────────────────────
    def zeige_app():
        page.controls.clear()
        page.add(si.appSite(page))
        page.update()

        # Standorte im Hintergrund vorladen
        def preload():
            try:
                data = mt.get_standorte_from_db()
                mt._standorte_cache["data"] = data
                mt._standorte_cache["loaded"] = True
                print(f"✅ Standorte vorgeladen: {len(data)}")
            except Exception as e:
                print(f"❌ Fehler beim Vorladen: {e}")

        threading.Thread(target=preload, daemon=True).start()

    def zeige_fehler():
        page.controls.clear()
        page.add(
            ft.Container(
                expand=True,
                bgcolor="#f9fafb",
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("⚠️", size=60),
                        ft.Container(height=16),
                        ft.Text(
                            "Server nicht erreichbar",
                            size=20,
                            weight=ft.FontWeight.W_600,
                            color="#DC2626",
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Bitte die Seite neu laden.",
                            size=14,
                            color="#6B7280",
                        ),
                        ft.Container(height=24),
                        ft.ElevatedButton(
                            "Neu laden",
                            on_click=lambda _: page.window.reload(),
                            bgcolor="#6B8E23",
                            color="white",
                        ),
                    ],
                ),
            )
        )
        page.update()

    # ── Backend im Hintergrund aufwecken ───────────────────────
    threading.Thread(
        target=wake_up_backend,
        args=(api_url, zeige_app, zeige_fehler),
        daemon=True,
    ).start()


ft.run(
    target=main,
    view=ft.AppView.WEB_BROWSER,
    port=port,
    host="0.0.0.0",
)
