import flet as ft
import content as co

def navButton(icon, label, i, site):
    def click(e):
        site.ind.current = i
        navBar(site)
        co.updatePage(site)
    
    col = None
    if i == site.ind.current:
        col = ft.Colors.GREY_600  
    else:
        col = ft.Colors.TRANSPARENT
    
    return ft.Container(
        content = ft.Column(
            [
                ft.Icon(name = icon, color = ft.Colors.WHITE, size = 24),
                ft.Text(label, color = ft.Colors.WHITE, size = 12),
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            spacing = 4,
        ),
        bgcolor = col,
        expand = True,
        on_click = click,
        alignment = ft.alignment.center,
        padding = ft.padding.symmetric(vertical = 8),
    )


def navBar(site):
    site.navRow.controls = [
        navButton(ft.Icons.MAP, "Map", 0, site),
        navButton(ft.Icons.SEARCH, "Suche", 1, site),
        navButton(ft.Icons.LIST, "Liste", 2, site),
        navButton(ft.Icons.SHOPPING_BASKET, "Warenkorb", 3, site),
        navButton(ft.Icons.PERSON, "Profil", 4, site),
    ]
    site.page.update()
