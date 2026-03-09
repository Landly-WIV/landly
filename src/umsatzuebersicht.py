import flet as ft
import backend.logRegAuth as au


def getUmsatzContent(site, username, PRIMARY_GREEN, ACCENT_GREEN, WHITE):
    """Gibt nur den Umsatzübersicht-Content zurück (für Tab-System)"""
    
    LIGHT_BG = "#F0F7E6"
    CARD_BG = "#E8F5E0"
    
    # Zeitraum Tabs
    tabs = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text("Tag", size=14, color="#666666"),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    border_radius=20,
                    bgcolor=WHITE,
                ),
                ft.Container(
                    content=ft.Text("Woche", size=14, weight=ft.FontWeight.BOLD, color=WHITE),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    border_radius=20,
                    bgcolor=PRIMARY_GREEN,
                ),
                ft.Container(
                    content=ft.Text("Monat", size=14, color="#666666"),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    border_radius=20,
                    bgcolor=WHITE,
                ),
                ft.Container(
                    content=ft.Text("Jahr", size=14, color="#666666"),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    border_radius=20,
                    bgcolor=WHITE,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        padding=15,
        bgcolor=LIGHT_BG,
    )
    
    # Statistik Karten
    def create_stat_card(title, value, change, bgcolor=CARD_BG):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(title, size=14, color="#666666"),
                    ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.Text(change, size=12, color=ACCENT_GREEN, weight=ft.FontWeight.W_500),
                ],
                spacing=5,
            ),
            padding=20,
            bgcolor=bgcolor,
            border_radius=10,
            expand=True,
        )
    
    stats_row1 = ft.Row(
        controls=[
            create_stat_card("Gesamtumsatz", "€1,280.50", "+15.2%"),
            create_stat_card("Bestellungen", "42", "+8%"),
        ],
        spacing=10,
    )
    
    stats_row2 = ft.Container(
        content=create_stat_card("Ø Bestellwert", "€30.49", "+21%"),
        padding=ft.padding.only(top=10),
    )
    
    stats = ft.Column(
        controls=[stats_row1, stats_row2],
        spacing=0,
    )
    
    # Umsatzentwicklung (Woche) - mit Graph
    umsatz_header = ft.Container(
        content=ft.Text(
            "Umsatzentwicklung (Woche)",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="#333333",
        ),
        padding=ft.padding.only(top=20, bottom=15),
    )
    
    # Daten für den Graphen
    days_data = [
        ("Mo", 150.20),
        ("Di", 110.50),
        ("Mi", 155.00),
        ("Do", 280.80),
        ("Fr", 240.00),
        ("Sa", 164.00),
        ("So", 180.00),
    ]
    
    max_value = max([val for _, val in days_data])
    
    # Einfacher Balken-Graph
    def create_bar(day, value, max_val):
        height_percent = (value / max_val) * 100
        bar_height = (height_percent / 100) * 120  # max 120px Höhe
        
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        f"€{value:.0f}",
                        size=11,
                        color="#666666",
                        weight=ft.FontWeight.W_500,
                    ),
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Container(
                    width=35,
                    height=bar_height,
                    bgcolor=PRIMARY_GREEN if value == max_val else ACCENT_GREEN,
                    border_radius=5,
                    alignment=ft.Alignment.BOTTOM_CENTER,
                ),
                ft.Text(
                    day,
                    size=12,
                    color="#666666",
                    weight=ft.FontWeight.W_500,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        )
    
    graph = ft.Container(
        content=ft.Row(
            controls=[create_bar(day, val, max_value) for day, val in days_data],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor=CARD_BG,
        padding=20,
        border_radius=10,
    )
    
    # Detaillierte Tagesübersicht
    def create_day_card(day, amount, is_highlight=False):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            day[0:2],  # Erste 2 Buchstaben
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=WHITE if is_highlight else PRIMARY_GREEN,
                        ),
                        width=40,
                        height=40,
                        bgcolor=PRIMARY_GREEN if is_highlight else "#C8E6C9",
                        border_radius=20,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Text(
                        day,
                        size=14,
                        color="#333333",
                        expand=True,
                    ),
                    ft.Text(
                        amount,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=PRIMARY_GREEN if is_highlight else "#333333",
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=15,
            ),
            padding=12,
            bgcolor=WHITE,
            border_radius=8,
            border=ft.border.all(2, PRIMARY_GREEN) if is_highlight else None,
        )
    
    days_detail_list = ft.Column(
        controls=[
            create_day_card("Montag", "€150,20"),
            create_day_card("Dienstag", "€110,50"),
            create_day_card("Mittwoch", "€155,00"),
            create_day_card("Donnerstag", "€280,80", is_highlight=True),  # Bester Tag
            create_day_card("Freitag", "€240,00"),
            create_day_card("Samstag", "€164,00"),
            create_day_card("Sonntag", "€180,00"),
        ],
        spacing=8,
    )
    
    detail_header = ft.Container(
        content=ft.Text(
            "Detaillierte Tagesübersicht",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="#333333",
        ),
        padding=ft.padding.only(top=20, bottom=10),
    )
    
    # Meistverkaufte Artikel
    products_header = ft.Container(
        content=ft.Text(
            "Meistverkaufte Artikel",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="#333333",
        ),
        padding=ft.padding.only(top=20, bottom=10),
    )
    
    def create_product_card(emoji, name, sales, revenue):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(emoji, size=30),
                        width=60,
                        height=60,
                        border_radius=10,
                        bgcolor="#2D2D2D",
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(name, size=16, weight=ft.FontWeight.BOLD, color="#333333"),
                            ft.Text(sales, size=12, color="#666666"),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Text(revenue, size=16, weight=ft.FontWeight.W_500, color="#333333"),
                ],
                spacing=15,
            ),
            padding=15,
            bgcolor=CARD_BG,
            border_radius=10,
        )
    
    products_list = ft.Column(
        controls=[
            create_product_card("🥕", "Bio-Karotten", "25 Verkäufe", "€125.00"),
            ft.Container(height=10),
            create_product_card("🍅", "Strauchtomaten", "18 Verkäufe", "€98.50"),
            ft.Container(height=10),
            create_product_card("🍓", "Frische Erdbeeren", "15 Verkäufe", "€82.70"),
        ],
        spacing=0,
    )
    
    # Content ohne Top Navigation
    return ft.Column(
        controls=[
            tabs,
            ft.Container(
                content=ft.Column(
                    controls=[
                        stats,
                        umsatz_header,
                        graph,
                        detail_header,
                        days_detail_list,
                        products_header,
                        products_list,
                        ft.Container(height=30),
                    ],
                    spacing=0,
                ),
                padding=15,
            ),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )


def umsatzuebersichtPage(site):
    """Umsatzübersicht für Bauern mit Dummy-Daten"""
    
    # Farben
    PRIMARY_GREEN = "#2D5016"
    LIGHT_GREEN = "#6B8E23"
    ACCENT_GREEN = "#90C040"
    WHITE = "#FFFFFF"
    LIGHT_BG = "#F0F7E6"
    CARD_BG = "#E8F5E0"
    
    username = au.getUse() if au.getUse() else "Hof Sonnenblume"
    
    # Navigation Drawer (geschlossen bis zum Klick)
    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                username,
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=WHITE,
                            ),
                            bgcolor=PRIMARY_GREEN,
                            padding=20,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.DASHBOARD, color=PRIMARY_GREEN),
                            title=ft.Text("Übersicht", weight=ft.FontWeight.W_500),
                            selected=True,
                            on_click=lambda e: close_drawer_func(e),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.PERSON, color=PRIMARY_GREEN),
                            title=ft.Text("Profil", weight=ft.FontWeight.W_500),
                            on_click=lambda e: navigate_to_profile_func(e),
                        ),
                        ft.Divider(),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.LOGOUT, color="#D32F2F"),
                            title=ft.Text("Abmelden"),
                            on_click=lambda e: logout_handler_func(e),
                        ),
                    ],
                ),
            ),
        ],
    )
    
    # Drawer zur Page hinzufügen
    site.page.drawer = drawer
    site.page.update()  # Drawer registrieren
    
    # Burger Menu - Handler Funktionen (nach drawer-Initialisierung)
    def open_menu(e):
        site.page.drawer.open = True
        site.page.update()
    
    def close_drawer_func(e):
        site.page.drawer.open = False
        site.page.update()
    
    def navigate_to_profile_func(e):
        site.page.drawer.open = False
        site.page.update()
        import content as co
        site.cont.content = co.profilPage(site)
        site.page.update()
    
    def logout_handler_func(e):
        site.page.drawer.open = False
        site.page.update()
        au.logOut()
        import content as co
        co.updatePage(site)
    
    # Top Navigation Bar mit Burger Menu
    top_nav = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.MENU,
                    icon_color="#333333",
                    on_click=open_menu,
                    tooltip="Menü"
                ),
                ft.Text(
                    "Umsatzübersicht",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#333333"
                ),
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.Icons.FILE_DOWNLOAD,
                        icon_color="#333333",
                        tooltip="Exportieren"
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.only(left=10, right=10, top=10, bottom=10),
        bgcolor=WHITE,
    )
    
    # Zeitraum Tabs
    tabs = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text("Tag", size=14, color="#666666"),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    border_radius=20,
                    bgcolor=WHITE,
                ),
                ft.Container(
                    content=ft.Text("Woche", size=14, weight=ft.FontWeight.BOLD, color=WHITE),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    border_radius=20,
                    bgcolor=PRIMARY_GREEN,
                ),
                ft.Container(
                    content=ft.Text("Monat", size=14, color="#666666"),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    border_radius=20,
                    bgcolor=WHITE,
                ),
                ft.Container(
                    content=ft.Text("Jahr", size=14, color="#666666"),
                    padding=ft.padding.symmetric(horizontal=20, vertical=10),
                    border_radius=20,
                    bgcolor=WHITE,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        padding=15,
        bgcolor=LIGHT_BG,
    )
    
    # Statistik Karten
    def create_stat_card(title, value, change, bgcolor=CARD_BG):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(title, size=14, color="#666666"),
                    ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.Text(change, size=12, color=ACCENT_GREEN, weight=ft.FontWeight.W_500),
                ],
                spacing=5,
            ),
            padding=20,
            bgcolor=bgcolor,
            border_radius=10,
            expand=True,
        )
    
    stats_row1 = ft.Row(
        controls=[
            create_stat_card("Gesamtumsatz", "€1,280.50", "+15.2%"),
            create_stat_card("Bestellungen", "42", "+8%"),
        ],
        spacing=10,
    )
    
    stats_row2 = ft.Container(
        content=create_stat_card("Ø Bestellwert", "€30.49", "+21%"),
        padding=ft.padding.only(top=10),
    )
    
    stats = ft.Column(
        controls=[stats_row1, stats_row2],
        spacing=0,
    )
    
    # Umsatzentwicklung (Woche) - mit Graph
    umsatz_header = ft.Container(
        content=ft.Text(
            "Umsatzentwicklung (Woche)",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="#333333",
        ),
        padding=ft.padding.only(top=20, bottom=15),
    )
    
    # Daten für den Graphen
    days_data = [
        ("Mo", 150.20),
        ("Di", 110.50),
        ("Mi", 155.00),
        ("Do", 280.80),
        ("Fr", 240.00),
        ("Sa", 164.00),
        ("So", 180.00),
    ]
    
    max_value = max([val for _, val in days_data])
    
    # Einfacher Balken-Graph
    def create_bar(day, value, max_val):
        height_percent = (value / max_val) * 100
        bar_height = (height_percent / 100) * 120  # max 120px Höhe
        
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(
                        f"€{value:.0f}",
                        size=11,
                        color="#666666",
                        weight=ft.FontWeight.W_500,
                    ),
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Container(
                    width=35,
                    height=bar_height,
                    bgcolor=PRIMARY_GREEN if value == max_val else ACCENT_GREEN,
                    border_radius=5,
                    alignment=ft.Alignment.BOTTOM_CENTER,
                ),
                ft.Text(
                    day,
                    size=12,
                    color="#666666",
                    weight=ft.FontWeight.W_500,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        )
    
    graph = ft.Container(
        content=ft.Row(
            controls=[create_bar(day, val, max_value) for day, val in days_data],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor=CARD_BG,
        padding=20,
        border_radius=10,
    )
    
    # Detaillierte Tagesübersicht (schön gestaltet)
    def create_day_card(day, amount, is_highlight=False):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            day[0:2],  # Erste 2 Buchstaben
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=WHITE if is_highlight else PRIMARY_GREEN,
                        ),
                        width=40,
                        height=40,
                        bgcolor=PRIMARY_GREEN if is_highlight else "#C8E6C9",
                        border_radius=20,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Text(
                        day,
                        size=14,
                        color="#333333",
                        expand=True,
                    ),
                    ft.Text(
                        amount,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=PRIMARY_GREEN if is_highlight else "#333333",
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=15,
            ),
            padding=12,
            bgcolor=WHITE,
            border_radius=8,
            border=ft.border.all(2, PRIMARY_GREEN) if is_highlight else None,
        )
    
    days_detail_list = ft.Column(
        controls=[
            create_day_card("Montag", "€150,20"),
            create_day_card("Dienstag", "€110,50"),
            create_day_card("Mittwoch", "€155,00"),
            create_day_card("Donnerstag", "€280,80", is_highlight=True),  # Bester Tag
            create_day_card("Freitag", "€240,00"),
            create_day_card("Samstag", "€164,00"),
            create_day_card("Sonntag", "€180,00"),
        ],
        spacing=8,
    )
    
    detail_header = ft.Container(
        content=ft.Text(
            "Detaillierte Tagesübersicht",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="#333333",
        ),
        padding=ft.padding.only(top=20, bottom=10),
    )
    
    # Meistverkaufte Artikel
    products_header = ft.Container(
        content=ft.Text(
            "Meistverkaufte Artikel",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="#333333",
        ),
        padding=ft.padding.only(top=20, bottom=10),
    )
    
    def create_product_card(emoji, name, sales, revenue):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(emoji, size=30),
                        width=60,
                        height=60,
                        border_radius=10,
                        bgcolor="#2D2D2D",
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(name, size=16, weight=ft.FontWeight.BOLD, color="#333333"),
                            ft.Text(sales, size=12, color="#666666"),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Text(revenue, size=16, weight=ft.FontWeight.W_500, color="#333333"),
                ],
                spacing=15,
            ),
            padding=15,
            bgcolor=CARD_BG,
            border_radius=10,
        )
    
    products_list = ft.Column(
        controls=[
            create_product_card("🥕", "Bio-Karotten", "25 Verkäufe", "€125.00"),
            ft.Container(height=10),
            create_product_card("🍅", "Strauchtomaten", "18 Verkäufe", "€98.50"),
            ft.Container(height=10),
            create_product_card("🍓", "Frische Erdbeeren", "15 Verkäufe", "€82.70"),
        ],
        spacing=0,
    )
    
    # Zusammensetzen der Seite
    return ft.Column(
        controls=[
            top_nav,
            tabs,
            ft.Container(
                content=ft.Column(
                    controls=[
                        stats,
                        umsatz_header,
                        graph,
                        detail_header,
                        days_detail_list,
                        products_header,
                        products_list,
                        ft.Container(height=30),
                    ],
                    spacing=0,
                ),
                padding=15,
            ),
        ],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
