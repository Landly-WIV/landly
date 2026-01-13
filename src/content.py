import flet as ft
import search as se
import landingpage as lp
import maptest as mt
import warenkorb as wk
import backend.searchFunctions as sf
import backend.logRegAuth as au
import logreg as lr

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
            # Profil-Seite: Zeige Login oder Hofseite
            if au.isLog():
                return profilPage(site)
            else:
                return lr.logRegPag(site.page)


def profilPage(site):
    """Profilseite für eingeloggte Benutzer - Hofprofil Design"""
    # Farben
    PRIMARY_GREEN = "#2D5016"
    LIGHT_GREEN = "#6B8E23"
    ACCENT_GREEN = "#90C040"
    WHITE = "#FFFFFF"
    
    username = au.getUse() if au.getUse() else "Hof Sonnenblume"
    
    # Logout Handler
    def logout_click(e):
        au.logOut()
        updatePage(site)
    
    # Top Navigation Bar
    top_nav = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color="#333333",
                    on_click=logout_click,
                    tooltip="Abmelden"
                ),
                ft.Text(
                    username,
                    size=18,
                    weight=ft.FontWeight.W_500,
                    color="#333333"
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.only(left=10, right=10, top=10, bottom=10),
        bgcolor=WHITE,
    )
    
    # Hof Logo (rundes Bild)
    logo = ft.Container(
        content=ft.Stack(
            controls=[
                ft.Container(
                    width=120,
                    height=120,
                    border_radius=60,
                    bgcolor=PRIMARY_GREEN,
                ),
                ft.Container(
                    content=ft.Text(
                        "F A R M",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=WHITE,
                    ),
                    width=120,
                    height=120,
                    alignment=ft.alignment.center,
                ),
            ],
        ),
        margin=ft.margin.only(top=20, bottom=20),
    )
    
    # Hof Info
    hof_title = ft.Text(
        username,
        size=22,
        weight=ft.FontWeight.BOLD,
        color="#333333",
        text_align=ft.TextAlign.CENTER,
    )
    
    hof_subtitle1 = ft.Text(
        "Familienbetrieb seit 1985",
        size=14,
        color="#666666",
        text_align=ft.TextAlign.CENTER,
    )
    
    hof_subtitle2 = ft.Text(
        "Bio-Gemüse, Obst und Eier",
        size=14,
        color="#666666",
        text_align=ft.TextAlign.CENTER,
    )
    
    # Verfügbare Produkte Header
    products_header = ft.Container(
        content=ft.Text(
            "Verfügbare Produkte",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="#333333",
        ),
        padding=ft.padding.only(left=20, top=20, bottom=10),
        alignment=ft.alignment.center_left,
    )
    
    # Produkt Kacheln
    def product_click(e, name):
        site.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"{name} ausgewählt"),
            bgcolor=ACCENT_GREEN
        )
        site.page.snack_bar.open = True
        site.page.update()
    
    product1 = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("🥬", size=40),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Text(
                        "Gemüse",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    bgcolor=PRIMARY_GREEN,
                    padding=8,
                    border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10),
                ),
            ],
            spacing=0,
        ),
        width=150,
        height=150,
        bgcolor="#2D2D2D",
        border_radius=10,
        on_click=lambda e: product_click(e, "Gemüse"),
        ink=True,
    )
    
    product2 = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("🍎", size=40),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Text(
                        "Obst",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    bgcolor=PRIMARY_GREEN,
                    padding=8,
                    border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10),
                ),
            ],
            spacing=0,
        ),
        width=150,
        height=150,
        bgcolor="#2D2D2D",
        border_radius=10,
        on_click=lambda e: product_click(e, "Obst"),
        ink=True,
    )
    
    products_row = ft.Row(
        controls=[product1, product2],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
    )
    
    # Kontakt & Infos Header
    contact_header = ft.Container(
        content=ft.Text(
            "Kontakt & Infos",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="#333333",
        ),
        padding=ft.padding.only(left=20, top=30, bottom=15),
        alignment=ft.alignment.center_left,
    )
    
    # Kontakt Items
    def create_contact_item(icon, title, subtitle, icon_bg):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, color=PRIMARY_GREEN, size=20),
                        width=40,
                        height=40,
                        bgcolor=icon_bg,
                        border_radius=20,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(title, size=12, color="#666666"),
                            ft.Text(subtitle, size=14, weight=ft.FontWeight.W_500, color="#333333"),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=15,
            ),
            padding=15,
            margin=ft.margin.only(left=20, right=20, bottom=10),
        )
    
    contact_items = ft.Column(
        controls=[
            create_contact_item(
                ft.Icons.PHONE,
                "Telefon",
                "+49 123 456789",
                "#C8E6C9"
            ),
            create_contact_item(
                ft.Icons.EMAIL,
                "E-Mail",
                "sonnenblume@hof.de",
                "#C8E6C9"
            ),
            create_contact_item(
                ft.Icons.ACCESS_TIME,
                "Öffnungszeiten",
                "Mo-Fr 8:00, Sa: 8:00-16:00",
                "#C8E6C9"
            ),
        ],
        spacing=0,
    )
    
    # Zusammensetzen der Seite
    return ft.Column(
        controls=[
            top_nav,
            logo,
            hof_title,
            hof_subtitle1,
            hof_subtitle2,
            products_header,
            products_row,
            contact_header,
            contact_items,
            ft.Container(height=20),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


def updatePage(site):
    if site.ind.current != 1:
        site.seaSta.mode = None
    
    site.cont.content = getPage(site.ind.current, site)
    site.page.update()

        