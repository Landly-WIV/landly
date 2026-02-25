import flet as ft
import content as co
import requests
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import API_URL

_lab = None

def getLab():
    """Labels aus der Datenbank laden"""
    global _lab
    if _lab is None:
        try:
            res = requests.get(f"{API_URL}/labels")
            if res.status_code == 200:
                labels = res.json()
                _lab = [lab['bezeichnung'] for lab in labels if lab.get('bezeichnung')]
            else:
                _lab = []
        except Exception as e:
            print(f"Fehler beim Laden der Labels: {e}")
            _lab = []
    
    return _lab.copy()

class searchState():
    def __init__(self):
        self.mode = None
        self.seaTex = ""
        self.selCat = None
        self.seaEna = False
        self.seaRes = False
        self.seaEnt = 50
        self.priSta = 0
        self.priEnd = 50
        self.lab = []
        self.showAll = True  # Alle Bauern anzeigen (ohne Geo-Filter)
        self.showAllProducts = True  # Alle Produkte anzeigen (ohne Filter)

def sel(e, site, mode):
    site.seaSta.mode = mode
    co.updatePage(site)

def bacCli(e, site):
    site.seaSta.mode = None
    site.seaSta.seaTex = ""
    site.seaSta.seaEna = False
    site.seaSta.seaEnt = 0
    co.updatePage(site)

def seaCli(e, site, seaFie=None, disSli=None):
    if disSli:
        site.seaSta.seaEnt = float(disSli.value)
    if seaFie:
        site.seaSta.seaTex = seaFie.value
    site.seaSta.seaEna = True
    co.updatePage(site)

def remLab(e, site, sel, lab, selRow, catDro):
    if e.control.text in sel:
        site.seaSta.lab.remove(e.control.text)
        sel.remove(e.control.text)
        lab.append(e.control.text)
        lab.sort()
        updLab(site, sel, lab, selRow, catDro)

def selLab(e, site, sel, lab, selRow, catDro):
    if e.control.value and e.control.value not in sel:
        site.seaSta.lab.append(e.control.value)
        sel.append(e.control.value)
        lab.remove(e.control.value)
        catDro.value = None  # Dropdown zurücksetzen für nächste Auswahl
        updLab(site, sel, lab, selRow, catDro)

def updLab(site, sel, lab, selRow, catDro):
    selRow.controls.clear()
    for label_text in sel:
        but = ft.FilledTonalButton(
            text=label_text,
            icon=ft.Icons.CLOSE_SHARP,
            on_click=lambda e, lbl=label_text: remLabByName(e, lbl, site, sel, lab, selRow, catDro)
        )
        selRow.controls.append(but)
    
    catDro.options.clear()
    for label_text in lab:
        catDro.options.append(ft.dropdown.Option(label_text))
    
    site.page.update()

def remLabByName(e, label_name, site, sel, lab, selRow, catDro):
    """Entfernt ein Label anhand des Namens"""
    if label_name in sel:
        site.seaSta.lab.remove(label_name)
        sel.remove(label_name)
        lab.append(label_name)
        lab.sort()
        updLab(site, sel, lab, selRow, catDro)

def sliLab(e, priTex, site):
    site.seaSta.priSta = int(e.control.start_value)
    site.seaSta.priEnd = int(e.control.end_value)
    priTex.value = f"Preisspanne {int(e.control.start_value)},00€ - {int(e.control.end_value)},00€"
    site.page.update()

def sliEnt(e, disTex, site):
    site.seaSta.seaEnt = int(e.control.value)
    disTex.value = f"Entfernung {int(e.control.value)}km"
    site.page.update()