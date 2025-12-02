import flet as ft
import search as se
import landingpage as lp
import maptest as mt

class contentPage():
    def __init__(self, navRow, page, ind, cont):
        self.navRow = navRow
        self.page = page
        self.ind = ind
        self.cont = cont
        self.seaSta = se.searchState()

def getPage(ind, site):
    match ind:
        case 0:
            return mt.mapPage(site)
        
        case 1:
            return se.shoSea(site)
        
        case 2:
            return lp.land()
        
        case 3:
            return ft.Row()
        
        case 4:
            return ft.Row()


def updatePage(site):
    # Reset search state when leaving search page
    if site.ind.current != 1:
        site.seaSta.mode = None
        site.seaSta.seaTex = ""
    
    site.cont.content = getPage(site.ind.current, site)
    site.page.update()