import flet as ft
import content as co
import products as pr

_bau = None

def getBau():
    global _bau
    if _bau is None:
        _bau = [
            farm(
                "Birkenhof Schmidt",
                "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200",
                "Dorfstraße 23, 12345 Grünwald",
                "Mo-Fr: 8:00-18:00\nSa: 8:00-14:00\nSo: Geschlossen",
                "+49 123 456789",
                "info@birkenhof-schmidt.de")
        ]

    return _bau

class farm():
    def __init__(self, name, banner_image, address, opening_hours, phone, email):
        self.ind = 1
        self.name = name
        self.banner_image = banner_image
        self.address = address
        self.opening_hours = opening_hours
        self.phone = phone
        self.email = email
        self.ope = False

    def opeBau(self):
        for p in getBau():
            p.ope = False
        self.ope = True

    def cloBau(self):
        self.ope = False

def bacCli(e, site):
    site.seaSta.mode = None
    site.seaSta.seaTex = ""
    site.seaSta.seaEna = False
    co.updatePage(site)

def seaCli(e, site, seaFie):
    site.seaSta.seaTex = seaFie.value
    site.seaSta.seaEna = True
    co.updatePage(site)

def cliBau(site, bau):
    bau.opeBau()
    co.updatePage(site)

def bauSit(bau, site):
    def back_click(e):
        bau.cloBau()
        co.updatePage(site)

    header1 = ft.Row(controls=[
        ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=back_click),
        ft.Text("Produkte")
    ])
    
    
    # Farben
    PRIMARY_GREEN = "#2D5016"
    LIGHT_GREEN = "#6B8E23"
    ACCENT_GREEN = "#90C040"
    WHITE = "#FFFFFF"
    
    # Dummy-Daten für den Hof
    # farm_data = {
    #     "name": "Birkenhof Schmidt",
    #     "banner_image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200",
    #     "address": "Dorfstraße 23, 12345 Grünwald",
    #     "opening_hours": "Mo-Fr: 8:00-18:00\nSa: 8:00-14:00\nSo: Geschlossen",
    #     "phone": "+49 123 456789",
    #     "email": "info@birkenhof-schmidt.de"
    # }
    
    # Dummy-Produkte
    products = [
        {"name": "Frische Eier", "price": "3,50 €", "unit": "10 Stück", "image": "🥚"},
        {"name": "Bio-Milch", "price": "1,20 €", "unit": "1 Liter", "image": "🥛"},
        {"name": "Kartoffeln", "price": "2,50 €", "unit": "1 kg", "image": "🥔"},
        {"name": "Äpfel", "price": "3,00 €", "unit": "1 kg", "image": "🍎"},
        {"name": "Honig", "price": "8,50 €", "unit": "500g Glas", "image": "🍯"},
        {"name": "Karotten", "price": "2,00 €", "unit": "1 kg", "image": "🥕"},
    ]
    
    def on_product_click(e, product_name):
        site.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"{product_name} ausgewählt"),
            bgcolor=ACCENT_GREEN
        )
        site.page.snack_bar.open = True
        site.page.update()
    
    # Header
    header = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.AGRICULTURE, color=WHITE, size=30),
                ft.Text(
                    bau.name,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=WHITE
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=PRIMARY_GREEN,
        padding=20,
    )
    
    # Banner mit Hofbild
    banner = ft.Container(
        content=ft.Image(
            src=bau.banner_image,
            fit=ft.ImageFit.COVER,
            width=float('inf'),
            height=200,
        ),
        height=200,
    )
    
    # Informations-Banner
    info_banner = ft.Container(
        content=ft.Column(
            [
                ft.Row([
                    ft.Icon(ft.Icons.LOCATION_ON, color=PRIMARY_GREEN, size=20),
                    ft.Text(bau.address, size=14, color="#333333"),
                ], spacing=10),
                ft.Row([
                    ft.Icon(ft.Icons.ACCESS_TIME, color=PRIMARY_GREEN, size=20),
                    ft.Text(bau.opening_hours, size=14, color="#333333"),
                ], spacing=10),
                ft.Row([
                    ft.Icon(ft.Icons.PHONE, color=PRIMARY_GREEN, size=20),
                    ft.Column([
                        ft.Text(bau.phone, size=14, color="#333333"),
                        ft.Text(bau.email, size=14, color="#333333"),
                    ], spacing=2),
                ], spacing=10),
            ],
            spacing=15,
        ),
        bgcolor=WHITE,
        padding=20,
    )
    
    # Produkte-Überschrift
    products_header = ft.Container(
        content=ft.Text(
            "Unsere Produkte",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=PRIMARY_GREEN,
        ),
        padding=ft.padding.only(left=20, top=30, bottom=20),
    )
    
    # Produkt-Kacheln
    product_tiles = []
    for product in products:
        tile = ft.Container(
            content=ft.Column(
                [
                    ft.Text(product["image"], size=30),
                    ft.Text(
                        product["name"],
                        size=10,
                        weight=ft.FontWeight.BOLD,
                        color=PRIMARY_GREEN,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        product["price"],
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=LIGHT_GREEN,
                    ),
                    ft.Text(
                        product["unit"],
                        size=8,
                        color="#666666",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            width=100,
            height=150,
            bgcolor=WHITE,
            border=ft.border.all(2, LIGHT_GREEN),
            border_radius=10,
            padding=20,
            on_click=lambda e, p=product["name"]: on_product_click(e, p),
            ink=True,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.with_opacity(0.1, "#000000"),
            ),
        )
        product_tiles.append(tile)
    
    # Grid für Produkte
    products_grid = ft.Container(
        content=ft.Row(
            product_tiles,
            wrap=True,
            spacing=20,
            run_spacing=20,
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.only(left=20, right=20, bottom=40),
    )
    
    # Zusammensetzen der Seite
    return ft.Column(
        [
            header1,
            ft.Row(),
            header,
            banner,
            info_banner,
            products_header,
            products_grid,
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

def bauSeaRes(bauLis, site):    
    seaTer = site.seaSta.seaTex.lower().strip()
    seaEnt = site.seaSta.seaEnt

    if seaTer:
        filBau = [bau for bau in bauLis if seaTer in bau.name.lower()]
    else:
        filBau = [bau for bau in bauLis]

    #if seaEnt:
    #    filBau = [(i, name) for i, name in filBau if seaEnt >= pr._ent[i]]
    
    header = ft.Row(
        controls=[
            ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: bacCli(e, site)),
            ft.Text(f"Suchergebnisse ({len(filBau)} gefunden)", 
                   theme_style=ft.TextThemeStyle.BODY_MEDIUM)
        ]
    )
    
    if len(filBau) == 0:
        return ft.Column(
            controls=[
                ft.Row(),
                header,
                ft.Divider(),
                ft.Text("Keine Bauern gefunden.", size=16, color=ft.Colors.GREY_700)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    bauCar = []
    for bau in filBau:
        card = ft.Card(
            content=ft.Container(
                content=ft.Column(controls=[
                    ft.Icon(ft.Icons.AGRICULTURE, size=40, color=ft.Colors.GREEN),
                    ft.Text(bau.name, weight=ft.FontWeight.BOLD, size=18),
                    ft.Text(f"{pr._ent[bau.ind]} km entfernt", size=14, color=ft.Colors.GREY_700)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                on_click=lambda e: cliBau(site, bau)
            ),
            width=0.4 * site.page.width,
            height=0.3 * site.page.height,
        )
        bauCar.append(card)
    
    body = ft.Row(
        wrap=True,
        controls=bauCar,
        spacing=10,
    )
    
    return ft.Column(
        controls=[
            ft.Row(),
            header,
            ft.Divider(),
            body
        ],
        spacing=20,
        scroll=ft.ScrollMode.ALWAYS
    )

def shoBau(site):
    openBau = False
    bau = None

    bauLis = getBau()

    for i in bauLis:
        if i.ope:
            openBau = True
            bau = i
            break

    if openBau:
        return bauSit(bau, site)
    else:
        return bauSeaRes(bauLis, site)