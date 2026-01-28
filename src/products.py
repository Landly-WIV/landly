import flet as ft
import content as co
import warenkorb as wk
import requests

apiUrl = "http://localhost:8000"

_proCac = None
_bauCac = {}

def getBauNam(bauId):
    global _bauCac
    
    if bauId in _bauCac:
        return _bauCac[bauId]
    
    try:
        res = requests.get(f"{apiUrl}/bauern/{bauId}")
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
        res = requests.get(f"{apiUrl}/produkte")
        if res.status_code == 200:
            _proCac = res.json()
            return _proCac
    except Exception as e:
        print(f"Fehler beim Laden der Produkte: {e}")
        return []
    
    return _proCac if _proCac else []

def getProDet(proId):
    try:
        res = requests.get(f"{apiUrl}/produkte/{proId}")
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print(f"Fehler beim Laden des Produkts: {e}")
    return None

def calDis(bauId):
    dis = {1: 12.5, 2: 23, 3: 5.2, 4: 40}
    return dis.get(bauId, 0)

def getProIco(proArtBez):
    ico = {
        "gemüse": "🥕",
        "obst": "🍎",
        "fleisch": "🥩",
        "eier": "🥚",
        "milch": "🥛",
        "brot": "🍞",
        "käse": "🧀"
    }
    
    if proArtBez:
        key = proArtBez.lower()
        return ico.get(key, "🛒")
    return "🛒"

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

    det = getProDet(proDat['produkt_id'])
    if det:
        proDat = det

    bauNam = getBauNam(proDat['bauern_id'])
    
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
        ft.Text(f"von {bauNam}", size=14, color=ft.Colors.GREY_700),
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
        bauNam = getBauNam(prd['bauern_id'])
        dis = calDis(prd['bauern_id'])
        
        ico = "🛒"
        if prd.get('produktart'):
            ico = getProIco(prd['produktart'].get('bezeichnung'))
        
        car = ft.Card(
            content=ft.Container(
                content=ft.Column(controls=[
                    ft.Text(bauNam, size=12),
                    ft.Text(prd['name'], weight=ft.FontWeight.BOLD, size=14),
                    ft.Text(ico, size=50),
                    ft.Text(
                        prd.get('produktart', {}).get('bezeichnung', 'Produkt'), 
                        color=ft.Colors.GREY_700, 
                        size=12
                    ),
                    ft.Text(f"{prd['preis']} € / {prd['einheit']}", size=14),
                    ft.Text(f"{dis} km entfernt", size=12)
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