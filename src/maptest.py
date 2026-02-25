import flet as ft
import flet_map as map
import requests
import threading
from config import API_URL
import farmer as fa

# Globaler Cache für Standorte
_standorte_cache = {
    'data': None,
    'loading': False,
    'loaded': False
}

def preload_standorte():
    """
    Lädt Standorte im Hintergrund vor (beim App-Start aufrufen).
    """
    if _standorte_cache['loading'] or _standorte_cache['loaded']:
        return
    
    def _load():
        _standorte_cache['loading'] = True
        print("🚀 Vorladen der Standorte gestartet...")
        data = get_standorte_from_db()
        _standorte_cache['data'] = data
        _standorte_cache['loaded'] = True
        _standorte_cache['loading'] = False
        print(f"✅ Standorte vorgeladen: {len(data)} Einträge")
    
    thread = threading.Thread(target=_load, daemon=True)
    thread.start()

def get_cached_standorte():
    """Gibt gecachte Standorte zurück oder lädt sie neu."""
    if _standorte_cache['loaded'] and _standorte_cache['data'] is not None:
        return _standorte_cache['data']
    return get_standorte_from_db()

def get_standorte_from_db():
    """
    Holt alle Standorte mit Koordinaten über die API.
    Returns:
        Liste von Standorten mit lat/lon Koordinaten
    """
    try:
        res = requests.get(f"{API_URL}/standorte/karte")
        if res.status_code == 200:
            standorte = res.json()
            print(f"📍 DEBUG: {len(standorte)} Standorte aus API geladen")
            return standorte
        return []
    except Exception as e:
        print(f"❌ Fehler beim Laden der Standorte: {e}")
        return []


def create_marker_for_standort(standort, on_click_handler, site):
    """
    Erstellt einen Marker für einen Standort.
    
    Args:
        standort: Dictionary mit standort_id, bezeichnung, lat, lon, firmenname, bauer_id
        on_click_handler: Callback-Funktion beim Klicken auf den Marker
        site: Site-Objekt für Navigation
    
    Returns:
        map.Marker Objekt
    """
    def handle_click(e):
        """Handler für Marker-Klick - navigiert zur Bauernseite"""
        bauer_id = standort.get('bauer_id')
        if bauer_id:
            # Farm-Objekt erstellen
            bau = fa.farm(
                ind=bauer_id,
                name=standort.get('firmenname', 'Unbekannter Hof'),
                banner_image="https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200",
                address=standort.get('adresse', 'Keine Adresse'),
                opening_hours="Mo-Fr: 8:00-18:00",
                phone="",
                email="",
                distanze=0
            )
            # Direkt die Bauernseite im Content anzeigen
            site.cont.content = fa.bauSit(bau, site)
            site.page.update()
        else:
            # Kein Bauer verknüpft - Snackbar zeigen
            on_click_handler(e, standort)
    
    return map.Marker(
        content=ft.GestureDetector(
            content=ft.Icon(
                ft.Icons.LOCATION_ON,
                color=ft.Colors.RED_600,
                size=40
            ),
            on_tap=handle_click,
        ),
        coordinates=map.MapLatitudeLongitude(standort['lat'], standort['lon']),
    )


def mapPage(site):
    marker_layer_ref = ft.Ref[map.MarkerLayer]()
    
    # Status für geladene Standorte
    standorte_geladen = False
    
    # Snackbar für Marker-Klick
    def on_marker_click(e, standort):
        """Handler wenn ein Bauern-Marker angeklickt wird"""
        site.page.snack_bar = ft.SnackBar(
            content=ft.Text(
                f"🌾 {standort['firmenname']}\n📍 {standort['adresse'] or 'Keine Adresse'}"
            ),
            bgcolor=ft.Colors.GREEN_100
        )
        site.page.snack_bar.open = True
        site.page.update()
    
    def load_standorte(e=None):
        """Lädt alle Bauern-Standorte aus der Datenbank und zeigt sie als Marker"""
        nonlocal standorte_geladen
        if standorte_geladen:
            return
        
        print("🔄 Lade Standorte...")
        standorte = get_cached_standorte()  # Nutzt Cache wenn verfügbar
        
        if standorte:
            # Alle bestehenden Marker leeren
            marker_layer_ref.current.markers.clear()
            
            # Marker für jeden Standort erstellen
            for standort in standorte:
                print(f"➕ Erstelle Marker für: {standort['firmenname']}")
                marker = create_marker_for_standort(standort, on_marker_click, site)
                marker_layer_ref.current.markers.append(marker)
            
            standorte_geladen = True
            print(f"✅ {len(standorte)} Marker hinzugefügt")
            site.page.update()
            
            # Info anzeigen
            site.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✅ {len(standorte)} Bauernhöfe geladen"),
                bgcolor=ft.Colors.GREEN_200
            )
            site.page.snack_bar.open = True
            site.page.update()
        else:
            print("⚠️ Keine Standorte gefunden!")
            site.page.snack_bar = ft.SnackBar(
                content=ft.Text("⚠️ Keine Standorte gefunden oder Fehler beim Laden"),
                bgcolor=ft.Colors.AMBER_200
            )
            site.page.snack_bar.open = True
            site.page.update()
    
    def reload_standorte(e):
        """Lädt die Standorte neu"""
        nonlocal standorte_geladen
        standorte_geladen = False
        load_standorte()
    
    # Header mit Lade-Button
    header_row = ft.Row(
        controls=[
            ft.Icon(ft.Icons.MAP, color=ft.Colors.GREEN_700),
            ft.Text(
                "Bauernhöfe in der Nähe",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.GREEN_900
            ),
            ft.Container(expand=True),
            ft.ElevatedButton(
                "Höfe laden",
                icon=ft.Icons.REFRESH,
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                on_click=load_standorte
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    
    # Deutschland-zentrierte Kartenansicht (Nürnberg als Zentrum)
    INITIAL_LAT = 49.45
    INITIAL_LON = 11.08
    INITIAL_ZOOM = 8
    
    karte = map.Map(
        expand=True,
        initial_center=map.MapLatitudeLongitude(INITIAL_LAT, INITIAL_LON),
        initial_zoom=INITIAL_ZOOM,
        interaction_configuration=map.InteractionConfiguration(
            flags=map.InteractionFlag.ALL
        ),
        on_init=load_standorte,  # Standorte beim Laden der Karte laden
        layers=[
            map.TileLayer(
                url_template="https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png",
                subdomains=["a", "b", "c"],
            ),
            map.RichAttribution(
                attributions=[
                    map.TextSourceAttribution(
                        text="OpenStreetMap Contributors",
                        on_click=lambda e: e.page.launch_url(
                            "https://openstreetmap.org/copyright"
                        ),
                    ),
                    map.TextSourceAttribution(
                        text="Landly",
                        on_click=lambda e: e.page.launch_url("https://flet.dev"),
                    ),
                ]
            ),
            map.MarkerLayer(
                ref=marker_layer_ref,
                markers=[],
            ),
        ],
    )
    
    return ft.Column(
        controls=[
            ft.Container(
                content=header_row,
                padding=10,
                bgcolor=ft.Colors.GREEN_50,
                border_radius=8,
            ),
            ft.Container(
                content=karte,
                expand=True,
                border_radius=8,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            ),
        ],
        spacing=10,
        expand=True,
    )