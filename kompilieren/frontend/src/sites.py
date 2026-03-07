import flet as ft
import navbar as nb
import content as co

def appSite(page):
    ind = 2
    
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