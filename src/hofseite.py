import flet as ft

def main(page: ft.Page):
    page.title = "Landly - Hofprofil"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.scroll = "auto"
    page.bgcolor = "#FFFFFF"

    page.window.height = 700
    page.window.width = 360
    
    
    # Farben
    PRIMARY_GREEN = "#2D5016"
    LIGHT_GREEN = "#6B8E23"
    ACCENT_GREEN = "#90C040"
    WHITE = "#FFFFFF"
    
    # Dummy-Daten für den Hof
    farm_data = {
        "name": "Birkenhof Schmidt",
        "banner_image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200",
        "address": "Dorfstraße 23, 12345 Grünwald",
        "opening_hours": "Mo-Fr: 8:00-18:00\nSa: 8:00-14:00\nSo: Geschlossen",
        "phone": "+49 123 456789",
        "email": "info@birkenhof-schmidt.de"
    }
    
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
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"{product_name} ausgewählt"),
            bgcolor=ACCENT_GREEN
        )
        page.snack_bar.open = True
        page.update()
    
    # Header
    header = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.AGRICULTURE, color=WHITE, size=30),
                ft.Text(
                    farm_data["name"],
                    size=28,
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
            src=farm_data["banner_image"],
            fit=ft.ImageFit.COVER,
            width=float('inf'),
            height=300,
        ),
        height=300,
    )
    
    # Informations-Banner
    info_banner = ft.Container(
        content=ft.Column(
            [
                ft.Row([
                    ft.Icon(ft.Icons.LOCATION_ON, color=PRIMARY_GREEN, size=20),
                    ft.Text(farm_data["address"], size=14, color="#333333"),
                ], spacing=10),
                ft.Row([
                    ft.Icon(ft.Icons.ACCESS_TIME, color=PRIMARY_GREEN, size=20),
                    ft.Text(farm_data["opening_hours"], size=14, color="#333333"),
                ], spacing=10),
                ft.Row([
                    ft.Icon(ft.Icons.PHONE, color=PRIMARY_GREEN, size=20),
                    ft.Column([
                        ft.Text(farm_data["phone"], size=14, color="#333333"),
                        ft.Text(farm_data["email"], size=14, color="#333333"),
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
                    ft.Text(product["image"], size=50),
                    ft.Text(
                        product["name"],
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=PRIMARY_GREEN,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        product["price"],
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=LIGHT_GREEN,
                    ),
                    ft.Text(
                        product["unit"],
                        size=12,
                        color="#666666",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            width=200,
            height=200,
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
    page.add(
        ft.Column(
            [
                header,
                banner,
                info_banner,
                products_header,
                products_grid,
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )
    )

ft.app(target=main)