# import flet as ft
# import sites as si
# from flet_mobile_preview.iPhone import iPhone13

# def main(page: ft.Page):
#     phone = iPhone13(page=page, zoom=1)
#     phone.page.theme_mode = ft.ThemeMode.LIGHT

#     phone.body = si.appSite(page)

#     phone.run() 

# ft.run(main)

import flet as ft
import sites as si

def main(page: ft.Page):
    page.padding = 0
    page.window.height = 700
    page.window.width = 360
    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(si.appSite(page))  

ft.run(main)