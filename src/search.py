import flet as ft
import content as co
import products as pr
import farmer as fa

class searchState():
    def __init__(self):
        self.mode = None
        self.seaTex = ""
        self.selCat = None
        self.seaEna = False
        self.seaEnt = 0

def selPro(e, site):
    site.seaSta.mode = "produkt"
    co.updatePage(site)
    
def selBau(e, site):
    site.seaSta.mode = "bauer"
    co.updatePage(site)

def seaSel(site):
    header = ft.Text(
        "Was möchten Sie suchen?",
        theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
        text_align=ft.TextAlign.CENTER
    )
    
    proBut = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.SHOPPING_BAG, size=40, color=ft.Colors.GREEN),
                ft.Text("Produkte suchen", size=15, weight=ft.FontWeight.BOLD)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        bgcolor=ft.Colors.GREEN_50,
        padding=30,
        border_radius=10,
        on_click=lambda e: selPro(e, site),
        width=0.7 * site.page.width,
        alignment=ft.alignment.center
    )
    
    bauBut = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.AGRICULTURE, size=40, color=ft.Colors.GREEN),
                ft.Text("Bauern suchen", size=15, weight=ft.FontWeight.BOLD)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        bgcolor=ft.Colors.GREEN_50,
        padding=30,
        border_radius=10,
        on_click=lambda e: selBau(e, site),
        width=0.7 * site.page.width,
        alignment=ft.alignment.center
    )
    
    return ft.Column(
        controls=[
            ft.Row(),
            header,
            ft.Row(height=30),
            proBut,
            ft.Row(height=20),
            bauBut
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

def bacCli(e, site):
    site.seaSta.mode = None
    site.seaSta.seaTex = ""
    site.seaSta.seaEna = False
    site.seaSta.seaEnt = 0
    co.updatePage(site)

def seaCli(e, site, seaFie, disSli=None):
    if disSli:
        site.seaSta.seaEnt = float(disSli.value)
    site.seaSta.seaTex = seaFie.value
    site.seaSta.seaEna = True
    co.updatePage(site)

def proSeaMas(site):   
    seaFie = ft.TextField(
        label="Produktname eingeben",
        prefix_icon=ft.Icons.SEARCH,
        width=400
    )
    
    catDro = ft.Dropdown(
        label="Kategorie",
        width=400,
        options=[
            ft.dropdown.Option("Gemüse"),
            ft.dropdown.Option("Obst"),
            ft.dropdown.Option("Fleisch"),
            ft.dropdown.Option("Eier"),
        ]
    )
    
    seaBut = ft.ElevatedButton(
        "Suchen",
        icon=ft.Icons.SEARCH,
        on_click=lambda e: seaCli(e, site, seaFie),
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        width=200,
        height=45
    )
    
    header = ft.Row(
        controls=[
            ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: bacCli(e, site)),
            ft.Text("Produkt suchen", theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
        ]
    )
    
    return ft.Column(
        controls=[
            ft.Row(),
            header,
            ft.Divider(),
            ft.Row(height=20),
            seaFie,
            ft.Row(height=10),
            catDro,
            ft.Row(height=30),
            seaBut
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )

def bauSeaMas(site):    
    seaFie = ft.TextField(
        label="Bauernname eingeben",
        prefix_icon=ft.Icons.SEARCH,
        width=400
    )
    
    disSli = ft.Slider(
        min=0,
        max=50,
        divisions=10,
        label="Entfernung: {value} km",
        width=400
    )
    
    seaBut = ft.ElevatedButton(
        "Suchen",
        icon=ft.Icons.SEARCH,
        on_click=lambda e: seaCli(e, site, seaFie, disSli),
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        width=200,
        height=45
    )
    
    header = ft.Row(
        controls=[
            ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: bacCli(e, site)),
            ft.Text("Bauer suchen", theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
        ]
    )
    
    return ft.Column(
        controls=[
            ft.Row(),
            header,
            ft.Divider(),
            ft.Row(height=20),
            seaFie,
            ft.Row(height=10),
            disSli,
            ft.Row(height=30),
            seaBut
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )

def shoSea(site):
    if site.seaSta.seaEna:
        if site.seaSta.mode == "produkt":
            return pr.shoPro(site)
        elif site.seaSta.mode == "bauer":
            return fa.shoBau(site)
    
    if site.seaSta.mode == "produkt":
        return proSeaMas(site)
    elif site.seaSta.mode == "bauer":
        return bauSeaMas(site)
    
    return seaSel(site)