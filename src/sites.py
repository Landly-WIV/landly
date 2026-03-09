import flet as ft
import navbar as nb
import content as co

def appSite(page, start_index=2):
    ind = start_index  # Standardmäßig Landingpage, kann aber überschrieben werden
    
    navRow = ft.Row(
        spacing = 0,
        expand = True,
    )
    
    navCont = ft.Container(
        content = navRow,
        bgcolor = ft.Colors.GREEN,
        height = 80,
    )

    cont = ft.Container(
        content = None,
        expand = True,
        padding = 20,
    )

    site = co.contentPage(navRow, page, ind, cont)

    cont.content = co.getPage(ind, site)
    
    nb.navBar(site)

    re = ft.Column(
        controls=[
            site.cont,
            navCont,
        ],
        expand = True,
        spacing = 0,
    )

    return re