import flet as ft
import backend.logRegAuth as logRegAut
#import backend.bestellungFunctions as besFun

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
    """Produkt zum Warenkorb hinzufügen - unterstützt Dict oder Objekt"""
    warenkorb = getWarenkorb()
    
    # Produkt-ID ermitteln (unterstützt Dict und Objekt)
    if isinstance(prod, dict):
        proId = prod.get('produkt_id') or prod.get('proId')
        name = prod.get('name', 'Unbekannt')
        preis = prod.get('preis', 0)
        einheit = prod.get('einheit', 'Stück')
    else:
        proId = prod.proId
        name = prod.name
        preis = prod.preis
        einheit = prod.einheit
    
    # Prüfe ob Produkt schon im Warenkorb
    for item in warenkorb:
        if item['proId'] == proId:
            item['menge'] += menge
            return
    
    # Neues Produkt hinzufügen
    warenkorb.append({
        'proId': proId,
        'name': name,
        'preis': preis,
        'einheit': einheit,
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
    LIGHT_GREEN = "#6B8E23"
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
        content=ft.Column(
            controls=[
                # Obere Zeile: Produktname + Löschen-Button
                ft.Row(
                    controls=[
                        ft.Text(
                            item['name'], 
                            size=16, 
                            weight=ft.FontWeight.BOLD,
                            color="#333333",
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            on_click=remove_click,
                            icon_color="#999999",
                            icon_size=18,
                            tooltip="Entfernen",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                # Mittlere Zeile: Preis pro Einheit
                ft.Text(
                    f"{item['preis']:.2f} € / {item['einheit']}", 
                    size=13, 
                    color="#888888"
                ),
                ft.Container(height=8),
                # Untere Zeile: Mengensteuerung + Gesamtpreis
                ft.Row(
                    controls=[
                        # Mengensteuerung
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.REMOVE,
                                        on_click=menge_minus,
                                        icon_color=PRIMARY_GREEN,
                                        icon_size=18,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            str(item['menge']), 
                                            size=16, 
                                            weight=ft.FontWeight.BOLD,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        width=35,
                                        alignment=ft.Alignment.CENTER,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.ADD,
                                        on_click=menge_plus,
                                        icon_color=PRIMARY_GREEN,
                                        icon_size=18,
                                    ),
                                ],
                                spacing=0,
                            ),
                            border=ft.border.all(1, "#DDDDDD"),
                            border_radius=8,
                        ),
                        # Gesamtpreis für dieses Item
                        ft.Text(
                            f"{item['preis'] * item['menge']:.2f} €",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=PRIMARY_GREEN,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=2,
        ),
        padding=15,
        bgcolor=WHITE,
        border_radius=12,
        border=ft.border.all(1, "#E8E8E8"),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=6,
            color=ft.Colors.with_opacity(0.08, "#000000"),
            offset=ft.Offset(0, 2),
        ),
        margin=ft.margin.only(bottom=12, left=15, right=15),
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
    
    dlgRef = {"dlg": None}

    def besDurFue(e):
        dlgRef["dlg"].open = False
        clearWarenkorb()
        site.cont.content = warenkorbPage(site)
        site.page.update()

    def besDiaAbr(e):
        dlgRef["dlg"].open = False
        site.page.update()

    def bstAbsClick(e):
        if not logRegAut.isLog():
            import logreg as lr
            site.cont.content = lr.logRegPag(site.page)
            site.page.update()
            return

        usrObj = logRegAut.getUseObj()
        if not usrObj or "user_id" not in usrObj:
            site.page.snack_bar = ft.SnackBar(
                content=ft.Text("Bitte erneut anmelden."),
                bgcolor=ft.Colors.RED
            )
            site.page.snack_bar.open = True
            site.page.update()
            return

        if not getWarenkorb():
            site.page.snack_bar = ft.SnackBar(
                content=ft.Text("Warenkorb ist leer."),
                bgcolor=ft.Colors.ORANGE
            )
            site.page.snack_bar.open = True
            site.page.update()
            return

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Bestellung bestätigen"),
            content=ft.Text(
                f"Möchtest du die Bestellung über {getGesamtpreis():.2f} € wirklich aufgeben?"
            ),
            actions=[
                ft.TextButton("Abbrechen", on_click=besDiaAbr),
                ft.ElevatedButton(
                    "Jetzt bestellen",
                    on_click=besDurFue,
                    bgcolor=PRIMARY_GREEN,
                    color=WHITE,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        dlgRef["dlg"] = dlg
        site.page.overlay.append(dlg)
        dlg.open = True
        site.page.update()
    
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
            alignment=ft.Alignment.CENTER,
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
                    ft.TextButton(
                        "Warenkorb leeren",
                        icon=ft.Icons.DELETE_OUTLINE,
                        on_click=clear_click,
                        style=ft.ButtonStyle(color="#FF0000"),
                    ),
                    ft.ElevatedButton(
                        "Jetzt bestellen",
                        icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                        on_click=bstAbsClick,
                        bgcolor=PRIMARY_GREEN,
                        color=WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        width=250,
                        height=48,
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
