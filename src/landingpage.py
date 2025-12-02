import flet as ft

def land():
    # Farben
    PRIMARY_GREEN = "#2D5016"
    LIGHT_GREEN = "#6B8E23"
    ACCENT_GREEN = "#90C040"
    WHITE = "#FFFFFF"
    LIGHT_GRAY = "#F5F5F5"
    
    # Dummy-Neuigkeiten
    news = [
        {
            "title": "Neue Bio-Zertifizierung erhalten",
            "date": "15. November 2024",
            "image": "https://images.unsplash.com/photo-1621719225574-736570b520ad?q=80&w=2070&auto=format&fit=crop"
        },
        {
            "title": "Herbsternte beginnt",
            "date": "10. Oktober 2024",
            "image": "https://images.unsplash.com/photo-1464226184485-280280541ee4?w=600&h=300&fit=crop"
        },
        {
            "title": "Neues Hofladen-Café eröffnet",
            "date": "1. September 2024",
            "image": "https://images.unsplash.com/photo-1460306855393-0c6688c30566?w=600&h=300&fit=crop"
        },
        {
            "title": "Sommerferien-Öffnungszeiten",
            "date": "20. Juli 2024",
            "image": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=600&h=300&fit=crop"
        },
        {
            "title": "Frühjahrsmarkt auf dem Hof",
            "date": "5. Mai 2024",
            "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=300&fit=crop"
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
        item = ft.Container(
            content=ft.Stack(
                [
                    # Background Image
                    ft.Image(
                        src=article["image"],
                        fit=ft.ImageFit.COVER,
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
    return ft.Column(
        [
            header,
            news_header,
            news_list,
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )
