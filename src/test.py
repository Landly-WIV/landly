import flet as ft
import sites as si
from flet_mobile_preview.iPhone import iPhone13

def main(page: ft.Page):
    phone = iPhone13(page=page, zoom=1)
    phone.page.theme_mode = ft.ThemeMode.LIGHT

    phone.body = si.appSite(page)

    phone.run() 

ft.app(main)