import flet as ft
import sites as si
import maptest as mt
import threading

def main(page: ft.Page):
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # App direkt starten
    page.add(si.appSite(page))
    
    # Standorte im Hintergrund vorladen (für die Map)
    def preload():
        try:
            data = mt.get_standorte_from_db()
            mt._standorte_cache['data'] = data
            mt._standorte_cache['loaded'] = True
            print(f"✅ Standorte im Hintergrund geladen: {len(data)}")
        except Exception as e:
            print(f"❌ Fehler beim Vorladen: {e}")
    
    thread = threading.Thread(target=preload, daemon=True)
    thread.start()

ft.run(main)