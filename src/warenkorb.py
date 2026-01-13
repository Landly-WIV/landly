import flet as ft

# import backend.crud as crud
# from backend.db import get_db

_warenkorb = None

def getWarenkorb():
    """Warenkorb-Daten holen (aktuell Dummy-Daten)"""
    global _warenkorb
    if _warenkorb is None:
        _warenkorb = []
    
    # Backend-Version (auskommentiert):
    # db = next(get_db())
    # user_id = 1  # Später aus Session holen
    # warenkorb = crud.get_warenkorb_by_user(db, user_id=user_id)
    # if not warenkorb:
    #     warenkorb = crud.create_warenkorb(db, user_id=user_id)
    # return crud.get_warenkorb_detailed(db, warenkorb_id=warenkorb.warenkorb_id)
    
    return _warenkorb

def addToWarenkorb(prod, menge=1):
    """Produkt zum Warenkorb hinzufügen"""
    warenkorb = getWarenkorb()
    
    # Prüfe ob Produkt schon im Warenkorb
    for item in warenkorb:
        if item['proId'] == prod.proId:
            item['menge'] += menge
            return
    
    # Neues Produkt hinzufügen
    warenkorb.append({
        'proId': prod.proId,
        'name': prod.name,
        'preis': prod.preis,
        'einheit': prod.einheit,
        'menge': menge
    })
    
    # Backend-Version (auskommentiert):
    # db = next(get_db())
    # user_id = 1  # Später aus Session holen
    # warenkorb_obj = crud.get_warenkorb_by_user(db, user_id=user_id)
    # if not warenkorb_obj:
    #     warenkorb_obj = crud.create_warenkorb(db, user_id=user_id)
    # crud.add_to_warenkorb(
    #     db=db,
    #     warenkorb_id=warenkorb_obj.warenkorb_id,
    #     produkt_id=prod.proId,
    #     menge=menge,
    #     preis_je_einheit=prod.preis
    # )

def removeFromWarenkorb(proId):
    """Produkt aus Warenkorb entfernen"""
    warenkorb = getWarenkorb()
    global _warenkorb
    _warenkorb = [item for item in warenkorb if item['proId'] != proId]
    
    # Backend-Version (auskommentiert):
    # db = next(get_db())
    # crud.remove_from_warenkorb(db, position_id=position_id)

def updateMenge(proId, menge):
    """Menge eines Produkts ändern"""
    warenkorb = getWarenkorb()
    for item in warenkorb:
        if item['proId'] == proId:
            item['menge'] = menge
            break
    
    # Backend-Version (auskommentiert):
    # db = next(get_db())
    # crud.update_warenkorb_position(db, position_id=position_id, menge=menge)

def clearWarenkorb():
    """Warenkorb leeren"""
    global _warenkorb
    _warenkorb = []
    
    # Backend-Version (auskommentiert):
    # db = next(get_db())
    # user_id = 1  # Später aus Session holen
    # warenkorb = crud.get_warenkorb_by_user(db, user_id=user_id)
    # if warenkorb:
    #     crud.clear_warenkorb(db, warenkorb_id=warenkorb.warenkorb_id)

def getGesamtpreis():
    """Gesamtpreis berechnen"""
    warenkorb = getWarenkorb()
    return sum(item['preis'] * item['menge'] for item in warenkorb)

def warenkorbItem(item, site):
    """Einzelnes Warenkorb-Item darstellen"""
    # Farben
    PRIMARY_GREEN = "#2D5016"
    WHITE = "#FFFFFF"
    
    def remove_click(e):
        removeFromWarenkorb(item['proId'])
        site.cont.content = warenkorbPage(site)
        site.page.update()
    
    def menge_minus(e):
        if item['menge'] > 1:
            updateMenge(item['proId'], item['menge'] - 1)
            site.cont.content = warenkorbPage(site)
            site.page.update()
    
    def menge_plus(e):
        updateMenge(item['proId'], item['menge'] + 1)
        site.cont.content = warenkorbPage(site)
        site.page.update()
    
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(item['name'], size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{item['preis']:.2f} € / {item['einheit']}", size=14, color="#666666"),
                    ],
                    expand=True,
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.REMOVE,
                            on_click=menge_minus,
                            icon_color=PRIMARY_GREEN,
                            icon_size=20,
                        ),
                        ft.Text(str(item['menge']), size=16, width=30, text_align=ft.TextAlign.CENTER),
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            on_click=menge_plus,
                            icon_color=PRIMARY_GREEN,
                            icon_size=20,
                        ),
                    ],
                    spacing=5,
                ),
                ft.Text(
                    f"{item['preis'] * item['menge']:.2f} €",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    width=80,
                    text_align=ft.TextAlign.RIGHT,
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    on_click=remove_click,
                    icon_color="#FF0000",
                    icon_size=20,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=15,
        bgcolor=WHITE,
        border_radius=10,
        margin=ft.margin.only(bottom=10),
    )

def warenkorbPage(site):
    """Warenkorb-Seite"""
    # Farben
    PRIMARY_GREEN = "#2D5016"
    LIGHT_GREEN = "#6B8E23"
    ACCENT_GREEN = "#90C040"
    WHITE = "#FFFFFF"
    LIGHT_GRAY = "#F5F5F5"
    
    warenkorb = getWarenkorb()
    gesamtpreis = getGesamtpreis()
    
    def clear_click(e):
        clearWarenkorb()
        site.cont.content = warenkorbPage(site)
        site.page.update()
    
    def checkout_click(e):
        # Später: Zur Bestellung umwandeln
        site.page.snack_bar = ft.SnackBar(
            content=ft.Text("Bestellung wird bearbeitet..."),
            bgcolor=ACCENT_GREEN
        )
        site.page.snack_bar.open = True
        site.page.update()
        
        # Backend-Version (auskommentiert):
        # db = next(get_db())
        # user_id = 1  # Später aus Session holen
        # warenkorb_obj = crud.get_warenkorb_by_user(db, user_id=user_id)
        # if warenkorb_obj:
        #     bauer_id = 1  # Später vom User auswählen lassen
        #     bestellung = crud.warenkorb_to_bestellung(db, warenkorb_id=warenkorb_obj.warenkorb_id, bauer_id=bauer_id)
        #     clearWarenkorb()
        #     co.updatePage(site)
    
    # Header
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.SHOPPING_BASKET, color=WHITE, size=30),
                ft.Text(
                    "Warenkorb",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=WHITE
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=PRIMARY_GREEN,
        padding=20,
        margin=ft.margin.only(bottom=20),
    )
    
    # Warenkorb-Items
    items_column = ft.Column(
        controls=[],
        spacing=0,
    )
    
    if len(warenkorb) == 0:
        # Leerer Warenkorb
        empty_message = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(ft.Icons.SHOPPING_BASKET_OUTLINED, size=80, color=LIGHT_GREEN),
                    ft.Text(
                        "Ihr Warenkorb ist leer",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color="#666666"
                    ),
                    ft.Text(
                        "Fügen Sie Produkte hinzu",
                        size=14,
                        color="#999999"
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=50,
            alignment=ft.alignment.center,
        )
        items_column.controls.append(empty_message)
    else:
        # Warenkorb-Items anzeigen
        for item in warenkorb:
            items_column.controls.append(warenkorbItem(item, site))
        
        # Gesamtpreis und Buttons
        footer = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Divider(height=20, color="#CCCCCC"),
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Gesamtpreis:",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                f"{gesamtpreis:.2f} €",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=PRIMARY_GREEN,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(height=20),
                    ft.ElevatedButton(
                        "Zur Kasse",
                        icon=ft.Icons.SHOPPING_CART_CHECKOUT,
                        on_click=checkout_click,
                        bgcolor=PRIMARY_GREEN,
                        color=WHITE,
                        width=300,
                        height=50,
                    ),
                    ft.TextButton(
                        "Warenkorb leeren",
                        icon=ft.Icons.DELETE_OUTLINE,
                        on_click=clear_click,
                        style=ft.ButtonStyle(color="#FF0000"),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=20,
            bgcolor=LIGHT_GRAY,
            border_radius=10,
            margin=ft.margin.only(top=20),
        )
        items_column.controls.append(footer)
    
    # Hauptcontainer
    main_column = ft.Column(
        controls=[
            header,
            items_column,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    return ft.Container(
        content=main_column,
        padding=0,
        expand=True,
    )
