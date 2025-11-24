import flet as ft
import products as pr

class contentPage():
    def __init__(self, navRow, page, ind, cont):
        self.navRow = navRow
        self.page = page
        self.ind = ind
        self.cont = cont

def getPage(ind, page, site):
    match ind:
        case 0:
            return ft.Row()
        
        case 1:
            return pr.showProducts(page, site)
        
        case 2:
            return ft.Row()
        
        case 3:
            return ft.Row()
        
        case 4:
            return ft.Row()


def updatePage(site):
    site.cont.content = getPage(site.ind.current, site.page, site)
    site.page.update()