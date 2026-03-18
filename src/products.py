import flet as ft
import asyncio
import threading
import content as co
import warenkorb as wk
import requests
from config import API_URL, getProIco

_proCac = None
_bauCac = {}
_proDetCac = {}

def _norm_label(value):
    return str(value or "").strip().casefold()

def _extract_label_names(product_data):
    labels = (product_data or {}).get('labels') or []
    result = []

    for label_item in labels:
        if isinstance(label_item, dict):
            label_name = label_item.get('bezeichnung') or label_item.get('name') or label_item.get('label')
        else:
            label_name = str(label_item)

        if label_name:
            result.append(label_name)

    return result

def _get_product_labels_with_fallback(product_data):
    product_id = (product_data or {}).get('produkt_id') or (product_data or {}).get('proId')
    label_names = _extract_label_names(product_data)

    if label_names or not product_id:
        return label_names

    if product_id not in _proDetCac:
        _proDetCac[product_id] = getProDet(product_id) or {}

    details = _proDetCac.get(product_id) or {}
    detail_label_names = _extract_label_names(details)

    if detail_label_names:
        product_data['labels'] = [{"bezeichnung": name} for name in detail_label_names]

    return detail_label_names

def getBauNam(bauId):
    global _bauCac
    
    if bauId in _bauCac:
        return _bauCac[bauId]
    
    try:
        res = requests.get(f"{API_URL}/bauern/{bauId}")
        if res.status_code == 200:
            bau = res.json()
            nam = bau.get('firmenname', 'Unbekannt')
            _bauCac[bauId] = nam
            return nam
    except:
        pass
    
    return "Unbekannt"

def getProFroApi():
    global _proCac
    
    try:
        res = requests.get(f"{API_URL}/produkte")
        if res.status_code == 200:
            _proCac = res.json()
            return _proCac
    except Exception as e:
        print(f"Fehler beim Laden der Produkte: {e}")
        return []
    
    return _proCac if _proCac else []

def getProDet(proId):
    try:
        res = requests.get(f"{API_URL}/produkte/{proId}")
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Fehler beim Laden des Produkts: {e}")
    return None

def calDis(bauId):
    dis = {1: 12.5, 2: 23, 3: 5.2, 4: 40}
    return dis.get(bauId, 0)



def proSit(proDat, sit):
    # State für die Menge
    current_menge = {"value": 1}
    add_btn_ref = {"btn": None}
    toast_ref = {"container": None, "text": None}
    reset_timer_ref = {"timer": None}
    
    def bacCli(e):
        sit.seaSta.seaEna = True
        co.updatePage(sit)
    
    def addToCarCli(e):
        wk.addToWarenkorb(proDat, menge=current_menge["value"])

        if add_btn_ref["btn"] is not None:
            add_btn_ref["btn"].text = "Hinzugefügt ✓"
            add_btn_ref["btn"].disabled = True

        if toast_ref["text"] is not None and toast_ref["container"] is not None:
            toast_ref["text"].value = f"{current_menge['value']}x {proDat['name']} im Warenkorb"
            toast_ref["container"].visible = True

        sit.page.update()

        try:
            sit.page.run_task(reset_add_button_feedback)
        except Exception:
            if reset_timer_ref["timer"] is not None:
                reset_timer_ref["timer"].cancel()

            reset_timer_ref["timer"] = threading.Timer(1.4, reset_add_button_feedback_sync)
            reset_timer_ref["timer"].daemon = True
            reset_timer_ref["timer"].start()

    def reset_add_button_feedback_sync():
        if add_btn_ref["btn"] is not None:
            add_btn_ref["btn"].text = "In den Warenkorb"
            add_btn_ref["btn"].disabled = False
        if toast_ref["container"] is not None:
            toast_ref["container"].visible = False
        try:
            sit.page.update()
        except Exception:
            pass

    async def reset_add_button_feedback():
        await asyncio.sleep(1.2)
        if add_btn_ref["btn"] is not None:
            add_btn_ref["btn"].text = "In den Warenkorb"
            add_btn_ref["btn"].disabled = False
        if toast_ref["container"] is not None:
            toast_ref["container"].visible = False
        sit.page.update()
    
    def menge_minus(e):
        if current_menge["value"] > 1:
            current_menge["value"] -= 1
            menge_text.value = str(current_menge["value"])
            sit.page.update()
    
    def menge_plus(e):
        current_menge["value"] += 1
        menge_text.value = str(current_menge["value"])
        sit.page.update()

    # Produkt-ID ermitteln (unterstützt beide Formate)
    proId = proDat.get('produkt_id') or proDat.get('proId')
    
    det = None
    if proId:
        det = getProDet(proId)
        if det:
            proDat = det

    bauId = proDat.get('bauern_id') or proDat.get('bauer_id')
    bauNam = getBauNam(bauId) if bauId else "Unbekannt"
    
    # Produktbild oder Emoji-Fallback
    icoData = getProIco(proDat.get('name', ''))
    if icoData.get("image"):
        proImg = ft.Container(
            content=ft.Image(
                src=icoData["image"],
                fit=ft.BoxFit.COVER,
                width=float('inf'),
                height=200,
            ),
            border_radius=12,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            margin=ft.margin.symmetric(horizontal=20),
        )
    else:
        proImg = ft.Container(
            content=ft.Text(icoData["emoji"], size=80),
            width=160,
            height=160,
            border_radius=80,
            bgcolor=icoData["bg"],
            alignment=ft.Alignment.CENTER,
        )

    hea = ft.Row(controls=[
        ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=bacCli),
        ft.Text("Produkt Details")
    ])

    labTex = ""
    if det and 'labels' in det and det['labels']:
        labNam = [lab['bezeichnung'] for lab in det['labels']]
        labTex = ", ".join(labNam)

    bod = ft.Column(controls=[
        ft.Text(proDat['name'], theme_style=ft.TextThemeStyle.HEADLINE_LARGE),
        proImg,
        ft.Text(f"von {bauNam}", size=14),
        ft.Text(proDat.get('beschreibung', ''), size=16),
        ft.Row(),
        ft.Text("Preis", weight=ft.FontWeight.BOLD),
        ft.Text(f"{proDat['preis']} € / {proDat['einheit']}", size=18),
        ft.Row(),
    ],
    horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    if labTex:
        bod.controls.insert(3, ft.Text(f"Labels: {labTex}", size=12, color=ft.Colors.GREEN))
    
    # Mengen-Counter (wie im Warenkorb)
    menge_text = ft.Text(
        str(current_menge["value"]), 
        size=18, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )
    
    mengen_steuerung = ft.Container(
        content=ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.REMOVE,
                    on_click=menge_minus,
                    icon_color=ft.Colors.GREEN_700,
                    icon_size=22,
                ),
                ft.Container(
                    content=menge_text,
                    width=50,
                    alignment=ft.Alignment.CENTER,
                    padding=ft.padding.symmetric(horizontal=0),
                ),
                ft.IconButton(
                    icon=ft.Icons.ADD,
                    on_click=menge_plus,
                    icon_color=ft.Colors.GREEN_700,
                    icon_size=22,
                ),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        border=ft.border.all(2, ft.Colors.GREEN_700),
        border_radius=8,
        padding=ft.padding.symmetric(horizontal=10, vertical=5),
        width=170,
        alignment=ft.Alignment.CENTER,
    )

    add_to_cart_button = ft.Button(
        "In den Warenkorb",
        on_click=addToCarCli,
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        width=250,
        height=45,
    )
    add_btn_ref["btn"] = add_to_cart_button

    toast_text = ft.Text(
        "",
        size=13,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.W_600,
    )
    toast_container = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE, size=18),
                toast_text,
            ],
            spacing=8,
            tight=True,
        ),
        bgcolor=ft.Colors.GREEN_700,
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=12, vertical=10),
        right=16,
        bottom=16,
        visible=False,
    )
    toast_ref["text"] = toast_text
    toast_ref["container"] = toast_container

    foo = ft.Column(
        controls=[
            ft.Text("Menge:", size=14, weight=ft.FontWeight.BOLD),
            mengen_steuerung,
            ft.Container(height=15),
            add_to_cart_button,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
    )

    main_content = ft.Column(
        controls=[
            ft.Row(),
            hea,
            ft.Divider(),
            bod,
            ft.Divider(),
            foo,
            ft.Divider(),
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    return ft.Stack(
        controls=[
            main_content,
            toast_container,
        ],
        expand=True,
    )

def bacCli(e, sit):
    sit.seaSta.mode = None
    sit.seaSta.seaTex = ""
    sit.seaSta.seaEna = False
    co.updatePage(sit)

def cliPro(sit, proDat):
    sit.seaSta.selectedProduct = proDat
    co.updatePage(sit)

def proSeaRes(pro, sit):
    seaTer = sit.seaSta.seaTex.lower().strip()
    
    if seaTer:
        filPro = [
            p for p in pro 
            if seaTer in p['name'].lower() 
            or (p.get('produktart') and seaTer in p['produktart'].get('bezeichnung', '').lower())
        ]
    else:
        filPro = pro
    
    if not getattr(sit.seaSta, 'showAllProducts', False) and hasattr(sit.seaSta, 'priSta') and hasattr(sit.seaSta, 'priEnd'):
        filPro = [
            p for p in filPro 
            if sit.seaSta.priSta <= p['preis'] <= sit.seaSta.priEnd
        ]
    
    if not getattr(sit.seaSta, 'showAllProducts', False) and hasattr(sit.seaSta, 'lab') and sit.seaSta.lab:
        selected_labels = {
            _norm_label(label_name)
            for label_name in sit.seaSta.lab
            if _norm_label(label_name)
        }

        filPro = [
            p for p in filPro
            if selected_labels.intersection(
                {
                    _norm_label(label_name)
                    for label_name in _get_product_labels_with_fallback(p)
                    if _norm_label(label_name)
                }
            )
        ]
    
    hea = ft.Row(
        controls=[
            ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: bacCli(e, sit)),
            ft.Text(f"Suchergebnisse ({len(filPro)} gefunden)", 
                theme_style=ft.TextThemeStyle.BODY_MEDIUM)
        ]
    )
    
    if len(filPro) == 0:
        return ft.Column(
            controls=[
                ft.Row(),
                hea,
                ft.Divider(),
                ft.Text("Keine Produkte gefunden.", size=16, color=ft.Colors.GREY_700)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    
    proCar = []
    for prd in filPro:
        # Bauern-Name direkt aus der API-Response (kein extra API-Call mehr)
        bauer = prd.get('bauer')
        bauNam = bauer.get('firmenname', 'Unbekannt') if bauer else 'Unbekannt'
        
        icoData = getProIco(prd.get('name', ''))
        
        icoCont = ft.Container(
            content=ft.Text(icoData["emoji"], size=32),
            width=60,
            height=60,
            border_radius=30,
            bgcolor=icoData["bg"],
            alignment=ft.Alignment.CENTER,
        )
        
        car = ft.Card(
            content=ft.Container(
                content=ft.Column(controls=[
                    ft.Text(bauNam, size=12),
                    ft.Text(prd['name'], weight=ft.FontWeight.BOLD, size=14),
                    icoCont,
                    ft.Text(
                        prd.get('produktart', {}).get('bezeichnung', 'Produkt'), 
                        color=ft.Colors.GREY_700, 
                        size=12
                    ),
                    ft.Text(f"{prd['preis']} € / {prd['einheit']}", size=14),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER),
                padding=15,
                on_click=lambda e, p=prd: cliPro(sit, p)
            ),
            width=0.4 * sit.page.width,
        )
        proCar.append(car)
    
    bod = ft.Row(
        wrap=True,
        controls=proCar,
        spacing=10,
    )
    
    return ft.Column(
        controls=[
            ft.Row(),
            hea,
            ft.Divider(),
            bod
        ],
        spacing=20,
        scroll=ft.ScrollMode.ALWAYS
    )

def shoPro(sit):
    pro = getProFroApi()
    
    if hasattr(sit.seaSta, 'selectedProduct') and sit.seaSta.selectedProduct:
        proDat = sit.seaSta.selectedProduct
        sit.seaSta.selectedProduct = None
        return proSit(proDat, sit)
    else:
        return proSeaRes(pro, sit)