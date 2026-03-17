import flet as ft
import auth as au


def getUmsatzContent(site, username, PRIMARY_GREEN, ACCENT_GREEN, WHITE):
    """Gibt nur den Umsatzübersicht-Content zurück (für Tab-System)"""
    LIGHT_BG = "#F0F7E6"
    CARD_BG = "#E8F5E0"

    period_data = {
        "Tag": {
            "stats": (182.40, "+4.8%", 8, "+1", 22.80, "+2.1%"),
            "chart_title": "Umsatzentwicklung (Tag)",
            "chart_points": [("08", 12), ("10", 24), ("12", 38), ("14", 42), ("16", 36), ("18", 30)],
            "detail_title": "Stündliche Übersicht",
            "details": [("08:00", 12), ("10:00", 24), ("12:00", 38), ("14:00", 42), ("16:00", 36), ("18:00", 30)],
            "products": [("🥕", "Bio-Karotten", "5 Verkäufe", 24.50), ("🍅", "Strauchtomaten", "4 Verkäufe", 21.30), ("🥛", "Frische Milch", "3 Verkäufe", 15.90)],
        },
        "Woche": {
            "stats": (1280.50, "+15.2%", 42, "+8%", 30.49, "+21%"),
            "chart_title": "Umsatzentwicklung (Woche)",
            "chart_points": [("Mo", 150.2), ("Di", 110.5), ("Mi", 155.0), ("Do", 280.8), ("Fr", 240.0), ("Sa", 164.0), ("So", 180.0)],
            "detail_title": "Detaillierte Tagesübersicht",
            "details": [("Montag", 150.2), ("Dienstag", 110.5), ("Mittwoch", 155.0), ("Donnerstag", 280.8), ("Freitag", 240.0), ("Samstag", 164.0), ("Sonntag", 180.0)],
            "products": [("🥕", "Bio-Karotten", "25 Verkäufe", 125.00), ("🍅", "Strauchtomaten", "18 Verkäufe", 98.50), ("🍓", "Frische Erdbeeren", "15 Verkäufe", 82.70)],
        },
        "Monat": {
            "stats": (5460.00, "+9.7%", 176, "+12%", 31.02, "-1.4%"),
            "chart_title": "Umsatzentwicklung (Monat)",
            "chart_points": [("W1", 1160), ("W2", 1285), ("W3", 1410), ("W4", 1605)],
            "detail_title": "Wöchentliche Übersicht",
            "details": [("Woche 1", 1160), ("Woche 2", 1285), ("Woche 3", 1410), ("Woche 4", 1605)],
            "products": [("🥔", "Kartoffeln", "92 Verkäufe", 498.00), ("🥬", "Salatmix", "64 Verkäufe", 344.80), ("🍎", "Äpfel", "58 Verkäufe", 301.40)],
        },
        "Jahr": {
            "stats": (64320.00, "+22.4%", 2148, "+17%", 29.94, "+4.0%"),
            "chart_title": "Umsatzentwicklung (Jahr)",
            "chart_points": [("Q1", 14800), ("Q2", 15650), ("Q3", 16420), ("Q4", 17450)],
            "detail_title": "Quartalsübersicht",
            "details": [("Quartal 1", 14800), ("Quartal 2", 15650), ("Quartal 3", 16420), ("Quartal 4", 17450)],
            "products": [("🥩", "Rinderhack", "610 Verkäufe", 7350.00), ("🥛", "Frischmilch", "540 Verkäufe", 4860.00), ("🥕", "Karotten", "502 Verkäufe", 3514.00)],
        },
    }

    selected_period = {"value": "Woche"}
    tab_controls = {}
    content_container = ft.Container(padding=15)

    def format_euro(value):
        formatted = f"{value:,.2f}".replace(",", "#").replace(".", ",").replace("#", ".")
        return f"€{formatted}"

    def format_int(value):
        return f"{value:,}".replace(",", ".")

    def create_stat_card(title, value, change, bgcolor=CARD_BG):
        change_color = ACCENT_GREEN if str(change).startswith("+") else "#C62828"
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(title, size=14, color="#666666"),
                    ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.Text(change, size=12, color=change_color, weight=ft.FontWeight.W_500),
                ],
                spacing=5,
            ),
            padding=20,
            bgcolor=bgcolor,
            border_radius=10,
            expand=True,
        )

    def create_bar(label, value, max_val):
        max_val = max(max_val, 1)
        bar_height = max(12, (value / max_val) * 120)
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text(format_euro(value), size=11, color="#666666", weight=ft.FontWeight.W_500),
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Container(
                    width=35,
                    height=bar_height,
                    bgcolor=PRIMARY_GREEN if value == max_val else ACCENT_GREEN,
                    border_radius=5,
                ),
                ft.Text(label, size=12, color="#666666", weight=ft.FontWeight.W_500),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        )

    def create_detail_card(label, amount, is_highlight=False):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            label[0:2],
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
                    ft.Text(label, size=14, color="#333333", expand=True),
                    ft.Text(
                        format_euro(amount),
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=PRIMARY_GREEN if is_highlight else "#333333",
                    ),
                ],
                spacing=15,
            ),
            padding=12,
            bgcolor=WHITE,
            border_radius=8,
            border=ft.border.all(2, PRIMARY_GREEN) if is_highlight else None,
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
                    ft.Text(format_euro(revenue), size=16, weight=ft.FontWeight.W_500, color="#333333"),
                ],
                spacing=15,
            ),
            padding=15,
            bgcolor=CARD_BG,
            border_radius=10,
        )

    def build_period_content(period_key):
        data = period_data[period_key]
        stat_total, stat_total_change, stat_orders, stat_orders_change, stat_avg, stat_avg_change = data["stats"]
        points = data["chart_points"]
        details = data["details"]
        products = data["products"]
        max_value = max(v for _, v in points)
        max_detail = max(v for _, v in details)

        stats = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        create_stat_card("Gesamtumsatz", format_euro(stat_total), stat_total_change),
                        create_stat_card("Bestellungen", format_int(stat_orders), stat_orders_change),
                    ],
                    spacing=10,
                ),
                ft.Container(
                    content=create_stat_card("Ø Bestellwert", format_euro(stat_avg), stat_avg_change),
                    padding=ft.padding.only(top=10),
                ),
            ],
            spacing=0,
        )

        graph = ft.Container(
            content=ft.Row(
                controls=[create_bar(label, value, max_value) for label, value in points],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            ),
            bgcolor=CARD_BG,
            padding=20,
            border_radius=10,
        )

        detail_list = ft.Column(
            controls=[
                create_detail_card(label, value, is_highlight=(value == max_detail))
                for label, value in details
            ],
            spacing=8,
        )

        products_list = ft.Column(
            controls=[
                create_product_card(*products[0]),
                ft.Container(height=10),
                create_product_card(*products[1]),
                ft.Container(height=10),
                create_product_card(*products[2]),
            ],
            spacing=0,
        )

        return ft.Column(
            controls=[
                stats,
                ft.Container(
                    content=ft.Text(data["chart_title"], size=16, weight=ft.FontWeight.BOLD, color="#333333"),
                    padding=ft.padding.only(top=20, bottom=15),
                ),
                graph,
                ft.Container(
                    content=ft.Text(data["detail_title"], size=16, weight=ft.FontWeight.BOLD, color="#333333"),
                    padding=ft.padding.only(top=20, bottom=10),
                ),
                detail_list,
                ft.Container(
                    content=ft.Text("Meistverkaufte Artikel", size=16, weight=ft.FontWeight.BOLD, color="#333333"),
                    padding=ft.padding.only(top=20, bottom=10),
                ),
                products_list,
                ft.Container(height=30),
            ],
            spacing=0,
        )

    def apply_tab_styles():
        for key, controls in tab_controls.items():
            is_active = key == selected_period["value"]
            controls["container"].bgcolor = PRIMARY_GREEN if is_active else WHITE
            controls["text"].color = WHITE if is_active else "#666666"
            controls["text"].weight = ft.FontWeight.BOLD if is_active else ft.FontWeight.W_400

    def on_period_select(key):
        selected_period["value"] = key
        apply_tab_styles()
        content_container.content = build_period_content(key)
        site.page.update()

    def create_period_tab(label):
        tab_text = ft.Text(label, size=14, color="#666666")
        tab_container = ft.Container(
            content=tab_text,
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            border_radius=20,
            bgcolor=WHITE,
        )
        tab_controls[label] = {"container": tab_container, "text": tab_text}
        return ft.GestureDetector(
            content=tab_container,
            on_tap=lambda e, k=label: on_period_select(k),
        )

    tabs = ft.Container(
        content=ft.Row(
            controls=[
                create_period_tab("Tag"),
                create_period_tab("Woche"),
                create_period_tab("Monat"),
                create_period_tab("Jahr"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        ),
        padding=15,
        bgcolor=LIGHT_BG,
    )

    apply_tab_styles()
    content_container.content = build_period_content(selected_period["value"])

    return ft.Column(
        controls=[
            tabs,
            content_container,
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
