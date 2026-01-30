import flet as ft
import products as pr
import farmer as fa
import backend.searchFunctions as sf
import requests

def seaSel(site):
    header = ft.Text(
        "Was möchten Sie suchen?",
        theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
        text_align=ft.TextAlign.CENTER
    )
    
    proBut = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.SHOPPING_BAG, size=40, color=ft.Colors.GREEN),
                ft.Text("Produkte suchen", size=15, weight=ft.FontWeight.BOLD)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        bgcolor=ft.Colors.GREEN_50,
        padding=30,
        border_radius=10,
        on_click=lambda e: sf.sel(e, site, "produkt"),
        width=0.7 * site.page.width,
        alignment=ft.Alignment.CENTER
    )
    
    bauBut = ft.Container(
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.AGRICULTURE, size=40, color=ft.Colors.GREEN),
                ft.Text("Bauern suchen", size=15, weight=ft.FontWeight.BOLD)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        bgcolor=ft.Colors.GREEN_50,
        padding=30,
        border_radius=10,
        on_click=lambda e: sf.sel(e, site, "bauer"),
        width=0.7 * site.page.width,
        alignment=ft.Alignment.CENTER
    )
    
    return ft.Column(
        controls=[
            ft.Row(),
            header,
            ft.Row(height=30),
            proBut,
            ft.Row(height=20),
            bauBut
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True
    )

def proSeaMas(site, lab): 

    site.page.theme = ft.Theme(
        slider_theme=ft.SliderTheme(
            value_indicator_color=ft.Colors.with_opacity(0.0, ft.Colors.WHITE),
        )
    )

    seaFie = ft.TextField(
        label="Produktname eingeben",
        prefix_icon=ft.Icons.SEARCH,
        input_filter=ft.InputFilter("^[A-ZÄÖÜa-zäöüß0-9._-]*$"),
        width=400
    )

    sel = []
    opt = []

    selRow = ft.Row(
        controls=sel,
        width=300,
        wrap=True)

    for i in lab:
        opt.append(ft.dropdown.Option(i))
    
    catDro = ft.Dropdown(
        label="Kategorie",
        width=400,
        options=opt,
        on_text_change=lambda e: sf.selLab(e, site, sel, lab, selRow, catDro)
    )
    
    seaBut = ft.ElevatedButton(
        "Suchen",
        icon=ft.Icons.SEARCH,
        on_click=lambda e: sf.seaCli(e, site, seaFie),
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        width=200,
        height=45
    )
    
    header = ft.Row(
        controls=[
            ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: sf.bacCli(e, site)),
            ft.Text("Produkt suchen", theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
        ]
    )

    priTex = ft.Text(value="Preisspanne 0,00€ - 50,00€")

    priSli = ft.RangeSlider(
        min=0,
        max=50,
        start_value=0,
        divisions=10,
        end_value=50,
        inactive_color=ft.Colors.GREEN_300,
        active_color=ft.Colors.GREEN_700,
        overlay_color=ft.Colors.GREEN_100,
        on_change=lambda e: sf.sliLab(e, priTex, site),
        label=None
    )

    disTex = ft.Text(value="Entfernung 50km")

    disSli = ft.Slider(
        min=0,
        max=100,
        value=50,
        divisions=20,
        inactive_color=ft.Colors.GREEN_300,
        active_color=ft.Colors.GREEN_700,
        overlay_color=ft.Colors.GREEN_100,
        on_change=lambda e: sf.sliEnt(e, disTex, site),
        label=None
    )
    
    # Container für Suchoptionen (werden ein-/ausgeblendet)
    searchOptionsContainer = ft.Container(
        content=ft.Column(
            controls=[
                selRow,
                ft.Row(height=10),
                catDro,
                ft.Row(height=10),
                priTex,
                priSli,
                ft.Row(height=10),
                disTex,
                disSli,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        visible=not site.seaSta.showAllProducts,
    )
    
    def onToggleChange(e):
        site.seaSta.showAllProducts = not e.control.value
        searchOptionsContainer.visible = e.control.value
        site.page.update()
    
    # Toggle Switch: Alle anzeigen <-> Suchoptionen
    modeToggle = ft.Row(
        controls=[
            ft.Text("Alle anzeigen", size=14, color=ft.Colors.GREY_700 if not site.seaSta.showAllProducts else ft.Colors.GREEN_700),
            ft.Switch(
                value=not site.seaSta.showAllProducts,
                active_color=ft.Colors.GREEN,
                on_change=onToggleChange,
            ),
            ft.Text("Suchoptionen", size=14, color=ft.Colors.GREEN_700 if not site.seaSta.showAllProducts else ft.Colors.GREY_700),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )
    
    return ft.Column(
        controls=[
            ft.Row(),
            header,
            ft.Divider(),
            ft.Row(height=20),
            seaFie,
            ft.Row(height=15),
            modeToggle,
            ft.Row(height=10),
            searchOptionsContainer,
            ft.Row(height=30),
            seaBut
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )

def bauSeaMas(site):    
    seaFie = ft.TextField(
        label="Bauernname eingeben",
        prefix_icon=ft.Icons.SEARCH,
        input_filter=ft.InputFilter("^[A-ZÄÖÜa-zäöüß0-9._-]*$"),
        width=400
    )
    
    disTex = ft.Text(value="Entfernung 50km")

    disSli = ft.Slider(
        min=0,
        max=100,
        value=50,
        divisions=20,
        inactive_color=ft.Colors.GREEN_300,
        active_color=ft.Colors.GREEN_700,
        overlay_color=ft.Colors.GREEN_100,
        on_change=lambda e: sf.sliEnt(e, disTex, site),
        label=None,
        disabled=site.seaSta.showAll  # Deaktiviert wenn "Alle anzeigen" aktiv
    )
    
    def onShowAllChange(e):
        site.seaSta.showAll = e.control.value
        disSli.disabled = e.control.value
        disTex.visible = not e.control.value
        disSli.visible = not e.control.value
        site.page.update()
    
    showAllChk = ft.Checkbox(
        label="Alle anzeigen",
        value=site.seaSta.showAll,
        on_change=onShowAllChange,
        active_color=ft.Colors.GREEN
    )
    
    # Slider initial ausblenden wenn showAll aktiv
    if site.seaSta.showAll:
        disTex.visible = False
        disSli.visible = False
    
    seaBut = ft.ElevatedButton(
        "Suchen",
        icon=ft.Icons.SEARCH,
        on_click=lambda e: sf.seaCli(e, site, seaFie, disSli),
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        width=200,
        height=45
    )
    
    header = ft.Row(
        controls=[
            ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: sf.bacCli(e, site)),
            ft.Text("Bauer suchen", theme_style=ft.TextThemeStyle.HEADLINE_SMALL)
        ]
    )
    
    return ft.Column(
        controls=[
            ft.Row(),
            header,
            ft.Divider(),
            ft.Row(height=20),
            seaFie,
            ft.Row(height=10),
            showAllChk,
            ft.Row(height=10),
            disTex,
            disSli,
            ft.Row(height=30),
            seaBut
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )
    

def shoSea(site):
    if site.seaSta.seaEna:
        if site.seaSta.mode == "produkt":
            
            # Warten auf DB anbindung !!!

            # url = "http://localhost:8000"

            # res = requests.get(
            #     f"{url}/api/products", 
            #     params={
            #         "search": site.seaSta.seaTex, 
            #         "kategorie": site.seaSta.seaEnt
            #     }
            # )
            # jsoPro = res.json()

            # lisPro = []

            # for i in jsoPro:
            #     lisPro.append(fa.farm(
            #         i["id"],
            #         i["name"],
            #         "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200",
            #         i["adresse"],
            #         i["oeffnungszeiten"],
            #         i["telefon"],
            #         i["email"]))
                
            return pr.shoPro(site)
        
        elif site.seaSta.mode == "bauer":
            zwi = 0
            if fa._bau:
                zwi = 1

            if site.seaSta.seaRes == False:
                zwi = 0
                site.seaSta.seaRes = True

            lisBau = []

            if zwi == 0:
                url = "http://localhost:8000"

                try:
                    # Wenn "Alle anzeigen" aktiv, einfache Bauern-Liste laden
                    if site.seaSta.showAll:
                        res = requests.get(f"{url}/bauern")
                        
                        if res.status_code == 200:
                            jsoBau = res.json()
                            for bauer in jsoBau:
                                # Filter nach Suchtext wenn vorhanden
                                if site.seaSta.seaTex:
                                    searchLower = site.seaSta.seaTex.lower()
                                    firmenname = (bauer.get('firmenname') or '').lower()
                                    kontakt = (bauer.get('kontaktperson') or '').lower()
                                    if searchLower not in firmenname and searchLower not in kontakt:
                                        continue
                                
                                adresse = f"{bauer.get('straße', '')} {bauer.get('hausnr', '')}".strip()
                                
                                lisBau.append(fa.farm(
                                    bauer.get("bauer_id"),
                                    bauer.get("firmenname", "Unbekannter Hof"),
                                    "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200",
                                    adresse if adresse else "Keine Adresse",
                                    "Mo-Fr: 8:00-18:00",
                                    str(bauer.get("telefon", "")),
                                    bauer.get("email", ""),
                                    0  # Keine Distanz bei "Alle anzeigen"
                                ))
                    else:
                        # Mit Geo-Filter suchen
                        params = {
                            "max_distanz": site.seaSta.seaEnt,
                            "user_lat": 49.4521,
                            "user_lon": 11.0767
                        }
                        if site.seaSta.seaTex:
                            params["search"] = site.seaSta.seaTex

                        res = requests.get(f"{url}/bauern/search/advanced", params=params)
                        
                        if res.status_code == 200:
                            jsoBau = res.json()
                            for i in jsoBau:
                                bauer = i.get("bauer", {})
                                distanz = i.get("distanz_km", 0)
                                
                                adresse = f"{bauer.get('straße', '')} {bauer.get('hausnr', '')}".strip()
                                
                                lisBau.append(fa.farm(
                                    bauer.get("bauer_id"),
                                    bauer.get("firmenname", "Unbekannter Hof"),
                                    "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200",
                                    adresse if adresse else "Keine Adresse",
                                    "Mo-Fr: 8:00-18:00",
                                    str(bauer.get("telefon", "")),
                                    bauer.get("email", ""),
                                    distanz if distanz else 0
                                ))
                except Exception as e:
                    print(f"Fehler bei Bauern-Suche: {e}")
                    import traceback
                    traceback.print_exc()
                
                return fa.shoBau(site, lisBau)
            else:
                return fa.shoBau(site, fa._bau)
    
    if site.seaSta.mode == "produkt":
        lab = sf.getLab()
        return proSeaMas(site, lab)
    elif site.seaSta.mode == "bauer":
        return bauSeaMas(site)
    
    return seaSel(site)