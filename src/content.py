import flet as ft
import search as se
import landingpage as lp
import maptest as mt
import warenkorb as wk
import backend.searchFunctions as sf
import backend.logRegAuth as au
import logreg as lr
import umsatzuebersicht as uu

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
                # Alle eingeloggten Nutzer bekommen ihr Profil
                return profilPage(site)
            else:
                return lr.logRegPag(site.page)


def bauerProfilWithTabs(site, username, PRIMARY_GREEN, LIGHT_GREEN, ACCENT_GREEN, WHITE):
    """Zwei-Ansichten-System für Bauern: Profil und Übersicht"""
    
    # State für aktive Ansicht
    current_view = {"value": "profil"}  # "profil" oder "uebersicht"
    
    def logout_click(e):
        au.logOut()
        updatePage(site)
    
    # Container für den Content (wird dynamisch aktualisiert) - mit Scroll
    content_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    
    def switch_to_profil(e):
        current_view["value"] = "profil"
        update_view()
    
    def switch_to_uebersicht(e):
        current_view["value"] = "uebersicht"
        update_view()
    
    def update_view():
        # Buttons aktualisieren
        profil_btn.bgcolor = PRIMARY_GREEN if current_view["value"] == "profil" else WHITE
        profil_btn.content.color = WHITE if current_view["value"] == "profil" else "#666666"
        uebersicht_btn.bgcolor = PRIMARY_GREEN if current_view["value"] == "uebersicht" else WHITE
        uebersicht_btn.content.color = WHITE if current_view["value"] == "uebersicht" else "#666666"
        
        # Content aktualisieren
        if current_view["value"] == "profil":
            content_container.controls = [get_profil_content(site, username, PRIMARY_GREEN, WHITE, product_click)]
        else:
            content_container.controls = [uu.getUmsatzContent(site, username, PRIMARY_GREEN, ACCENT_GREEN, WHITE)]
        
        site.page.update()
    
    def product_click(e, name):
        site.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"{name} ausgewählt"),
            bgcolor=ACCENT_GREEN
        )
        site.page.snack_bar.open = True
        site.page.update()
    
    # Top Navigation Bar mit Logout
    top_nav = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(
                    username,
                    size=18,
                    weight=ft.FontWeight.W_500,
                    color="#333333"
                ),
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_color="#D32F2F",
                    on_click=logout_click,
                    tooltip="Abmelden"
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.only(left=20, right=10, top=10, bottom=10),
        bgcolor=WHITE,
    )
    
    # Umschalt-Buttons
    profil_btn = ft.Container(
        content=ft.Text("Profil", size=14, weight=ft.FontWeight.BOLD, color=WHITE),
        padding=ft.padding.symmetric(horizontal=30, vertical=12),
        border_radius=25,
        bgcolor=PRIMARY_GREEN,
        ink=True,
        on_click=switch_to_profil,
    )
    
    uebersicht_btn = ft.Container(
        content=ft.Text("Übersicht", size=14, weight=ft.FontWeight.BOLD, color="#666666"),
        padding=ft.padding.symmetric(horizontal=30, vertical=12),
        border_radius=25,
        bgcolor=WHITE,
        ink=True,
        on_click=switch_to_uebersicht,
    )
    
    button_row = ft.Container(
        content=ft.Row(
            controls=[profil_btn, uebersicht_btn],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=15,
        bgcolor="#F5F5F5",
    )
    
    # Hof Logo
    logo = ft.Container(
        content=ft.Stack(
            controls=[
                ft.Container(
                    width=80,
                    height=80,
                    border_radius=40,
                    bgcolor=PRIMARY_GREEN,
                ),
                ft.Container(
                    content=ft.Text(
                        "FARM",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=WHITE,
                    ),
                    width=80,
                    height=80,
                    alignment=ft.Alignment.CENTER,
                ),
            ],
        ),
        margin=ft.margin.only(top=10, bottom=10),
    )
    
    # Hof Info
    hof_title = ft.Text(
        username,
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#333333",
        text_align=ft.TextAlign.CENTER,
    )
    
    hof_subtitle1 = ft.Text(
        "Familienbetrieb seit 1985",
        size=13,
        color="#666666",
        text_align=ft.TextAlign.CENTER,
    )
    
    hof_subtitle2 = ft.Text(
        "Bio-Gemüse, Obst und Eier",
        size=13,
        color="#666666",
        text_align=ft.TextAlign.CENTER,
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
                    content=ft.Text("🥬", size=35),
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Text(
                        "Gemüse",
                        size=13,
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
        width=130,
        height=130,
        bgcolor="#2D2D2D",
        border_radius=10,
        on_click=lambda e: product_click(e, "Gemüse"),
        ink=True,
    )
    
    product2 = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("🍎", size=35),
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Text(
                        "Obst",
                        size=13,
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
        width=130,
        height=130,
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
    
    # Kontakt Items
    def create_contact_item(icon, title, subtitle, icon_bg):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, color=PRIMARY_GREEN, size=18),
                        width=35,
                        height=35,
                        bgcolor=icon_bg,
                        border_radius=17,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(title, size=11, color="#666666"),
                            ft.Text(subtitle, size=13, weight=ft.FontWeight.W_500, color="#333333"),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=12,
            ),
            padding=12,
            margin=ft.margin.only(left=20, right=20, bottom=8),
        )
    
    contact_items = ft.Column(
        controls=[
            create_contact_item(ft.Icons.PHONE, "Telefon", "+49 123 456789", "#C8E6C9"),
            create_contact_item(ft.Icons.EMAIL, "E-Mail", "sonnenblume@hof.de", "#C8E6C9"),
            create_contact_item(ft.Icons.ACCESS_TIME, "Öffnungszeiten", "Mo-Fr 8:00-18:00", "#C8E6C9"),
        ],
        spacing=0,
    )
    
    # Profil Tab Content
    profil_content = ft.Column(
        controls=[
            logo,
            hof_title,
            hof_subtitle1,
            hof_subtitle2,
            ft.Container(
                content=ft.Text("Verfügbare Produkte", size=15, weight=ft.FontWeight.BOLD, color="#333333"),
                padding=ft.padding.only(top=15, bottom=10),
            ),
            products_row,
            ft.Container(
                content=ft.Text("Kontakt & Infos", size=15, weight=ft.FontWeight.BOLD, color="#333333"),
                padding=ft.padding.only(top=20, bottom=10),
            ),
            contact_items,
            ft.Container(height=20),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
    )
    
    # Initial: Profil-Content anzeigen
    content_container.controls = [get_profil_content(site, username, PRIMARY_GREEN, WHITE, product_click)]
    
    return ft.Column(
        controls=[
            top_nav,
            button_row,
            content_container,
        ],
        spacing=0,
        expand=True,
    )


def get_profil_content(site, username, PRIMARY_GREEN, WHITE, product_click=None):
    """Erstellt den Profil-Content"""
    
    # Hof Logo
    logo = ft.Container(
        content=ft.Stack(
            controls=[
                ft.Container(
                    width=80,
                    height=80,
                    border_radius=40,
                    bgcolor=PRIMARY_GREEN,
                ),
                ft.Container(
                    content=ft.Text(
                        "FARM",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=WHITE,
                    ),
                    width=80,
                    height=80,
                    alignment=ft.Alignment.CENTER,
                ),
            ],
        ),
        margin=ft.margin.only(top=10, bottom=10),
    )
    
    # Hof Info
    hof_title = ft.Text(
        username,
        size=20,
        weight=ft.FontWeight.BOLD,
        color="#333333",
        text_align=ft.TextAlign.CENTER,
    )
    
    hof_subtitle1 = ft.Text(
        "Familienbetrieb seit 1985",
        size=13,
        color="#666666",
        text_align=ft.TextAlign.CENTER,
    )
    
    hof_subtitle2 = ft.Text(
        "Bio-Gemüse, Obst und Eier",
        size=13,
        color="#666666",
        text_align=ft.TextAlign.CENTER,
    )
    
    # Produkt Kacheln
    product1 = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("🥬", size=35),
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Text(
                        "Gemüse",
                        size=13,
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
        width=130,
        height=130,
        bgcolor="#2D2D2D",
        border_radius=10,
        on_click=lambda e: product_click(e, "Gemüse") if product_click else None,
        ink=True,
    )
    
    product2 = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text("🍎", size=35),
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Text(
                        "Obst",
                        size=13,
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
        width=130,
        height=130,
        bgcolor="#2D2D2D",
        border_radius=10,
        on_click=lambda e: product_click(e, "Obst") if product_click else None,
        ink=True,
    )
    
    products_row = ft.Row(
        controls=[product1, product2],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15,
    )
    
    # Kontakt Items
    def create_contact_item(icon, title, subtitle, icon_bg):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(icon, color=PRIMARY_GREEN, size=18),
                        width=35,
                        height=35,
                        bgcolor=icon_bg,
                        border_radius=17,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(title, size=11, color="#666666"),
                            ft.Text(subtitle, size=13, weight=ft.FontWeight.W_500, color="#333333"),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=12,
            ),
            padding=12,
            margin=ft.margin.only(left=20, right=20, bottom=8),
        )
    
    contact_items = ft.Column(
        controls=[
            create_contact_item(ft.Icons.PHONE, "Telefon", "+49 123 456789", "#C8E6C9"),
            create_contact_item(ft.Icons.EMAIL, "E-Mail", "sonnenblume@hof.de", "#C8E6C9"),
            create_contact_item(ft.Icons.ACCESS_TIME, "Öffnungszeiten", "Mo-Fr 8:00-18:00", "#C8E6C9"),
        ],
        spacing=0,
    )
    
    return ft.Column(
        controls=[
            logo,
            hof_title,
            hof_subtitle1,
            hof_subtitle2,
            ft.Container(
                content=ft.Text("Verfügbare Produkte", size=15, weight=ft.FontWeight.BOLD, color="#333333"),
                padding=ft.padding.only(top=15, bottom=10),
            ),
            products_row,
            ft.Container(
                content=ft.Text("Kontakt & Infos", size=15, weight=ft.FontWeight.BOLD, color="#333333"),
                padding=ft.padding.only(top=20, bottom=10),
            ),
            contact_items,
            ft.Container(height=20),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


def profilPage(site):
    """Profilseite für eingeloggte Benutzer - Hofprofil Design"""
    # Farben
    PRIMARY_GREEN = "#2D5016"
    LIGHT_GREEN = "#6B8E23"
    ACCENT_GREEN = "#90C040"
    WHITE = "#FFFFFF"
    
    username = au.getUse() if au.getUse() else "Hof Sonnenblume"
    useObj = au.getUseObj()
    is_bauer = useObj and useObj.get("rolle") == "bauer"
    
    # Für Bauern: Nutze Tab-System
    if is_bauer:
        return bauerProfilWithTabs(site, username, PRIMARY_GREEN, LIGHT_GREEN, ACCENT_GREEN, WHITE)
    
    # Logout Handler für Kunden
    def logout_click(e):
        au.logOut()
        updatePage(site)
    
    # Top Navigation Bar für Kunden
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
                    alignment=ft.Alignment.CENTER,
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
        alignment=ft.Alignment.CENTER_LEFT,
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
                    alignment=ft.Alignment.CENTER,
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
                    alignment=ft.Alignment.CENTER,
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
        alignment=ft.Alignment.CENTER_LEFT,
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
                        alignment=ft.Alignment.CENTER,
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
    if site.ind != 1:
        site.seaSta.mode = None
    
    site.cont.content = getPage(site.ind, site)
    site.page.update()

        