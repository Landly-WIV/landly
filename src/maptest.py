import flet as ft
import flet_map as map
from backend.db import SessionLocal
from backend import crud


def get_standorte_from_db():
    """
    Holt alle Standorte mit Koordinaten aus der Datenbank.
    Returns:
        Liste von Standorten mit lat/lon Koordinaten
    """
    db = SessionLocal()
    try:
        standorte = crud.get_standorte_mit_koordinaten(db)
        print(f"📍 DEBUG: {len(standorte)} Standorte aus DB geladen")
        for s in standorte:
            print(f"   - {s['firmenname']}: lat={s['lat']}, lon={s['lon']}")
        return standorte
    except Exception as e:
        print(f"❌ Fehler beim Laden der Standorte: {e}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        db.close()


def create_marker_for_standort(standort, on_click_handler):
    """
    Erstellt einen Marker für einen Standort.
    
    Args:
        standort: Dictionary mit standort_id, bezeichnung, lat, lon, firmenname
        on_click_handler: Callback-Funktion beim Klicken auf den Marker
    
    Returns:
        map.Marker Objekt
    """
    # Tooltip mit Hof-Informationen
    tooltip_text = f"{standort['firmenname']}\n{standort['bezeichnung'] or ''}\n{standort['adresse'] or ''}"
    
    return map.Marker(
        content=ft.Container(
            content=ft.Icon(
                ft.Icons.AGRICULTURE,
                color=ft.Colors.GREEN_800,
                size=30
            ),
            tooltip=tooltip_text,
            on_click=lambda e, s=standort: on_click_handler(e, s) if on_click_handler else None
        ),
        coordinates=map.MapLatitudeLongitude(standort['lat'], standort['lon']),
    )


def mapPage(site):
    marker_layer_ref = ft.Ref[map.MarkerLayer]()
    
    # Status für geladene Standorte
    standorte_geladen = ft.Ref[bool]()
    standorte_geladen.current = False
    
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
        if standorte_geladen.current:
            return
        
        print("🔄 Lade Standorte...")
        standorte = get_standorte_from_db()
        
        if standorte:
            # Alle bestehenden Marker leeren
            marker_layer_ref.current.markers.clear()
            
            # Marker für jeden Standort erstellen
            for standort in standorte:
                print(f"➕ Erstelle Marker für: {standort['firmenname']}")
                marker = create_marker_for_standort(standort, on_marker_click)
                marker_layer_ref.current.markers.append(marker)
            
            standorte_geladen.current = True
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
        standorte_geladen.current = False
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
        interaction_configuration=map.MapInteractionConfiguration(
            flags=map.MapInteractiveFlag.ALL
        ),
        on_init=load_standorte,  # Standorte beim Laden der Karte laden
        layers=[
            map.TileLayer(
                url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
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
