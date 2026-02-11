import flet as ft
import sites as si

def main(page: ft.Page):
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(si.appSite(page))  

ft.run(main)