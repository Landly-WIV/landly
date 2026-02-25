import flet as ft
import sites as si
import maptest as mt

def main(page: ft.Page):
    # Standorte im Hintergrund vorladen (weckt auch den Server auf)
    mt.preload_standorte()
    
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(si.appSite(page))  

ft.run(main)