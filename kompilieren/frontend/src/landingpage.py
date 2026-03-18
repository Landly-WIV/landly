import flet as ft
from pathlib import Path

def land():
    # Farben
    PRIMARY_GREEN = "#2D5016"
    LIGHT_GREEN = "#6B8E23"
    ACCENT_GREEN = "#90C040"
    WHITE = "#FFFFFF"
    LIGHT_GRAY = "#F5F5F5"
    
    # Dummy-Neuigkeiten
    assets_dir = Path(__file__).parent / "assets"
    asset_name_lookup = {
        p.name.lower(): p.name
        for p in assets_dir.iterdir()
        if p.is_file()
    }

    def resolve_image_source(image_value: str) -> str:
        if image_value.startswith("http://") or image_value.startswith("https://"):
            return image_value

        normalized = str(image_value or "").replace("\\", "/").strip()
        if normalized.startswith("assets/"):
            normalized = normalized.split("/", 1)[1]

        direct_candidate = Path(normalized)
        if direct_candidate.name.lower() in asset_name_lookup:
            # Bei gesetztem assets_dir reicht der Dateiname als src aus.
            return asset_name_lookup[direct_candidate.name.lower()]

        assets_candidate = assets_dir / normalized
        if assets_candidate.exists():
            return assets_candidate.name

        return normalized

    fullscreen_image = ft.Image(
        src="",
        fit=ft.BoxFit.CONTAIN,
        width=float('inf'),
        height=float('inf'),
    )

    def close_fullscreen(e):
        fullscreen_overlay.visible = False
        e.page.update()

    def open_fullscreen(image_src: str):
        def _handler(e):
            fullscreen_image.src = image_src
            fullscreen_overlay.visible = True
            e.page.update()
        return _handler

    fullscreen_overlay = ft.Container(
        visible=False,
        expand=True,
        bgcolor="#FFFFFF",
        content=ft.Stack(
            [
                ft.Container(
                    content=fullscreen_image,
                    padding=20,
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color="#222222",
                        icon_size=30,
                        tooltip="Schließen",
                        on_click=close_fullscreen,
                    ),
                    top=12,
                    right=12,
                ),
            ],
            expand=True,
        ),
    )

    news = [
        {
            "title": "Willkommen bei Landly",
            "date": "19. März 2026",
            "image": "landly.png"
        },
        {
            "title": "Die Spargelzeit kommt",
            "date": "10. März 2026",
            "image": "https://images.unsplash.com/photo-1603309288666-421bc2a729db?q=80&w=1170&auto=format&fit=crop"
        },
        {
            "title": "Neues Hofladen-Café eröffnet",
            "date": "1. Februar 2025",
            "image": "https://plus.unsplash.com/premium_photo-1674327105074-46dd8319164b?q=80&w=1170&auto=format&fit=crop"
        },
        {
            "title": "Wintergemüse",
            "date": "17. Dezember 2025",
            "image": "https://images.unsplash.com/photo-1605279682024-5a25531582dc?q=80&w=1171&auto=format&fit=crop"
        },
        {
            "title": "Der Herbst ist da",
            "date": "5. Oktober 2025",
            "image": "https://images.unsplash.com/photo-1509622905150-fa66d3906e09?q=80&w=735&auto=format&fit=crop"
        },
    ]
    
    # Header
    header = ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.AGRICULTURE, color=WHITE, size=30),
                ft.Text(
                    "Willkommen",
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
    
    # Neuigkeiten-Überschrift
    news_header = ft.Container(
        content=ft.Text(
            "Neuigkeiten",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=PRIMARY_GREEN,
        ),
        padding=ft.padding.only(left=20, top=30, bottom=20),
    )
    
    # Nachrichtenkacheln
    news_items = []
    for article in news:
        image_src = resolve_image_source(article["image"])
        item = ft.Container(
            content=ft.Stack(
                [
                    # Background Image
                    ft.Image(
                        src=image_src,
                        fit=ft.BoxFit.COVER,
                        width=float('inf'),
                        height=150,
                    ),
                    # Dark overlay
                    ft.Container(
                        width=float('inf'),
                        height=150,
                        bgcolor=ft.Colors.with_opacity(0.4, "#000000"),
                    ),
                    # Text content
                    ft.Row(
                        controls=[
                            ft.Column(),
                            ft.Column(
                                [
                                    ft.Text(
                                        article["title"],
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=WHITE,
                                    ),
                                    ft.Text(
                                        article["date"],
                                        size=12,
                                        color=ACCENT_GREEN,
                                    ),
                                    ft.Row()
                                ],
                                spacing=8,
                                alignment=ft.MainAxisAlignment.END,
                            )
                        ]
                    ),
                ],
                width=float('inf'),
                height=150,
            ),
            width=float('inf'),
            height=150,
            border_radius=10,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            margin=ft.margin.only(bottom=15),
            ink=True,
            on_click=open_fullscreen(image_src),
        )
        news_items.append(item)
    
    # News-Container
    news_list = ft.Container(
        content=ft.Column(
            news_items,
            spacing=0,
        ),
        padding=ft.padding.only(left=20, right=20, bottom=40),
    )
    
    # Zusammensetzen der Seite
    return ft.Stack(
        controls=[
            ft.Column(
                [
                    header,
                    news_header,
                    news_list,
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
            ),
            fullscreen_overlay,
        ],
        expand=True,
    )
