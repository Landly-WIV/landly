import flet as ft

def main(page: ft.Page):
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(ft.Text("Hello Web! Flet funktioniert!", size=30))

ft.run(main)
