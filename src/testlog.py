import flet as ft
import backend.logRegAuth as au

def main(page: ft.Page):
    page.padding = 0
    page.window.height = 700
    page.window.width = 360
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(au.sitVie(page))

ft.run(main)