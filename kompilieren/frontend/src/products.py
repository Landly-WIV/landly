import flet as ft
import content as co
import warenkorb as wk
import httpx
from config import API_URL, getProIco

_proCac = None
_bauCac = {}

def getBauNam(bauId):
    global _bauCac
    
    if bauId in _bauCac:
        return _bauCac[bauId]
    
    try:
        res = httpx.get(f"{API_URL}/bauern/{bauId}")
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
        res = httpx.get(f"{API_URL}/produkte")
        if res.status_code == 200:
            _proCac = res.json()
            return _proCac
    except Exception as e:
        print(f"Fehler beim Laden der Produkte: {e}")
        return []
    
    return _proCac if _proCac else []

def getProDet(proId):
    try:
        res = httpx.get(f"{API_URL}/produkte/{proId}")
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Fehler beim Laden des Produkts: {e}")
    return None

def calDis(bauId):
    dis = {1: 12.5, 2: 23, 3: 5.2, 4: 40}
    return dis.get(bauId, 0)



def proSit(proDat, sit):
    def bacCli(e):
        sit.seaSta.seaEna = True
        co.updatePage(sit)
    
    def addToCarCli(e):
        wk.addToWarenkorb(proDat, menge=1)
        sit.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"{proDat['name']} zum Warenkorb hinzugefügt"),
            bgcolor="#90C040"
        )
        sit.page.snack_bar.open = True
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
            margin=ft.Margin.symmetric(horizontal=20),
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

    foo = ft.Row(controls=[
        ft.Button("In den Warenkorb", on_click=addToCarCli, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
    ],
    alignment=ft.MainAxisAlignment.CENTER)

    return ft.Column(controls=[
        ft.Row(),
        hea,
        ft.Divider(),
        bod,
        ft.Divider(),
        foo,
        ft.Divider()
    ],
    scroll=ft.ScrollMode.AUTO)

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
    
    if hasattr(sit.seaSta, 'priSta') and hasattr(sit.seaSta, 'priEnd'):
        filPro = [
            p for p in filPro 
            if sit.seaSta.priSta <= p['preis'] <= sit.seaSta.priEnd
        ]
    
    if hasattr(sit.seaSta, 'lab') and sit.seaSta.lab:
        filPro = [
            p for p in filPro
            if any(
                lab['bezeichnung'] in sit.seaSta.lab 
                for lab in p.get('labels', [])
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