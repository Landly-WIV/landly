import flet as ft
import search as se
import landingpage as lp
import maptest as mt
import warenkorb as wk
import backend.searchFunctions as sf

class contentPage():
    def __init__(self, navRow, page, ind, cont):
        self.navRow = navRow
        self.page = page
        self.ind = ind
        self.cont = cont
        self.seaSta = sf.searchState()

def getPage(ind, site):
    match ind:
        case 0:
            return mt.mapPage(site)
        
        case 1:
            return se.shoSea(site)
        
        case 2:
            return lp.land()
        
        case 3:
            return wk.warenkorbPage(site)
        
        case 4:
            return ft.Row()


def updatePage(site):
    if site.ind.current != 1:
        site.seaSta.mode = None
    
    site.cont.content = getPage(site.ind.current, site)
    site.page.update()

        