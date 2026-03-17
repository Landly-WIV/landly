import flet as ft
import flet_map as map
import requests
import threading
import math
import asyncio
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


def _distance_m(lat1, lon1, lat2, lon2):
    """Luftlinienentfernung in Metern (Haversine)."""
    r = 6371000.0
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def _spread_nearby_markers(standorte, min_distance_m=40, offset_m=18):
    """Zieht sehr nahe Marker leicht auseinander, damit sie separat sichtbar/klickbar sind."""
    spread_count = 0
    adjusted = []

    for standort in standorte:
        lat = standort["lat"]
        lon = standort["lon"]

        nearby_count = sum(
            1
            for prev in adjusted
            if _distance_m(lat, lon, prev["_orig_lat"], prev["_orig_lon"]) < min_distance_m
        )

        marker_data = dict(standort)
        marker_data["_orig_lat"] = lat
        marker_data["_orig_lon"] = lon

        if nearby_count > 0:
            angle = math.radians((nearby_count * 70) % 360)
            radius = offset_m * (1 + (nearby_count // 6))

            d_lat = (radius / 111320.0) * math.sin(angle)
            cos_lat = max(0.2, math.cos(math.radians(lat)))
            d_lon = (radius / (111320.0 * cos_lat)) * math.cos(angle)

            marker_data["lat"] = lat + d_lat
            marker_data["lon"] = lon + d_lon
            spread_count += 1

        adjusted.append(marker_data)

    if spread_count > 0:
        print(f"🧭 Marker-Spread aktiv: {spread_count} nahe Marker leicht versetzt")

    return adjusted


def create_marker_for_standort(standort, on_click_handler):
    """Erstellt einen Marker für einen Standort."""
    return map.Marker(
        content=ft.GestureDetector(
            content=ft.Icon(
                ft.Icons.LOCATION_ON,
                color=ft.Colors.RED_600,
                size=44,
            ),
            on_tap=lambda e: on_click_handler(e, standort),
        ),
        coordinates=map.MapLatitudeLongitude(standort['lat'], standort['lon']),
    )


def mapPage(site):
    marker_layer_ref = ft.Ref[map.MarkerLayer]()
    standorte_geladen = False
    selected_standort_ref = {"value": None}
    load_toast_timer_ref = {"timer": None}
    load_toast_seq_ref = {"value": 0}

    callout_title = ft.Text(
        "",
        size=14,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_900,
        max_lines=1,
        overflow=ft.TextOverflow.ELLIPSIS,
    )
    callout_address = ft.Text(
        "",
        size=12,
        color=ft.Colors.GREY_800,
        max_lines=2,
        overflow=ft.TextOverflow.ELLIPSIS,
    )
    callout_hint = ft.Text(
        "",
        size=11,
        color=ft.Colors.GREY_700,
    )

    def hide_marker_callout(e=None):
        marker_callout.visible = False
        selected_standort_ref["value"] = None
        site.page.update()

    def open_hof_via_callout(e):
        standort = selected_standort_ref["value"]
        if not standort:
            return

        bauer_id = standort.get('bauer_id')
        if not bauer_id:
            site.page.snack_bar = ft.SnackBar(
                content=ft.Text("Für diesen Standort ist noch kein Hofprofil verknüpft."),
                bgcolor=ft.Colors.AMBER_200,
            )
            site.page.snack_bar.open = True
            site.page.update()
            return

        bau = fa.farm(
            ind=bauer_id,
            name=standort.get('firmenname', 'Unbekannter Hof'),
            banner_image="https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1200",
            address=standort.get('adresse', 'Keine Adresse'),
            opening_hours="Mo-Fr: 8:00-18:00",
            phone="",
            email="",
            distanze=0,
        )
        site.cont.content = fa.bauSit(bau, site)
        site.page.update()

    callout_action_btn = ft.FilledTonalButton(
        content=ft.Text("Zum Hof"),
        icon=ft.Icons.STORE,
        on_click=open_hof_via_callout,
    )

    marker_callout = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.RED_600, size=20),
                        callout_title,
                        ft.Container(expand=True),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            icon_size=16,
                            tooltip="Schließen",
                            on_click=hide_marker_callout,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                callout_address,
                callout_hint,
                ft.Row(
                    controls=[callout_action_btn],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            spacing=6,
            tight=True,
        ),
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREEN_200),
        border_radius=12,
        padding=ft.padding.symmetric(horizontal=10, vertical=8),
        right=16,
        bottom=16,
        width=320,
        visible=False,
    )

    load_toast_text = ft.Text(
        "",
        size=12,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.W_600,
    )

    load_toast = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.INFO, size=16, color=ft.Colors.WHITE),
                load_toast_text,
            ],
            spacing=8,
            tight=True,
        ),
        bgcolor=ft.Colors.GREEN_700,
        border_radius=10,
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        right=16,
        bottom=16,
        visible=False,
    )

    def _hide_load_toast():
        load_toast.visible = False
        try:
            site.page.update()
        except Exception:
            pass

    async def _auto_hide_load_toast(seq):
        await asyncio.sleep(1.2)
        if seq != load_toast_seq_ref["value"]:
            return
        _hide_load_toast()

    def show_load_toast(message, bg_color=ft.Colors.GREEN_700, icon=ft.Icons.INFO):
        load_toast_text.value = message
        load_toast.bgcolor = bg_color
        load_toast.content.controls[0].name = icon
        load_toast.visible = True
        site.page.update()

        load_toast_seq_ref["value"] += 1
        seq = load_toast_seq_ref["value"]

        try:
            site.page.run_task(_auto_hide_load_toast, seq)
            return
        except Exception:
            pass

        if load_toast_timer_ref["timer"] is not None:
            load_toast_timer_ref["timer"].cancel()

        load_toast_timer_ref["timer"] = threading.Timer(1.2, _hide_load_toast)
        load_toast_timer_ref["timer"].daemon = True
        load_toast_timer_ref["timer"].start()

    def on_marker_click(e, standort):
        selected_standort_ref["value"] = standort
        callout_title.value = standort.get('firmenname', 'Unbekannter Hof')
        callout_address.value = standort.get('adresse') or 'Keine Adresse'

        if standort.get('bauer_id'):
            callout_hint.value = "Tippe auf 'Zum Hof', um die Hofseite zu öffnen."
            callout_action_btn.visible = True
        else:
            callout_hint.value = "Für diesen Standort ist noch kein Hofprofil verknüpft."
            callout_action_btn.visible = False

        marker_callout.visible = True
        site.page.update()

    def load_standorte(e=None, force_refresh=False):
        """Lädt alle Bauern-Standorte und zeigt sie als Marker."""
        nonlocal standorte_geladen
        if standorte_geladen and not force_refresh:
            return

        print("🔄 Lade Standorte...")

        if force_refresh:
            print("🔁 Erzwinge Neuladen der Standorte von API...")
            show_load_toast("Höfe werden neu geladen...", ft.Colors.BLUE_700, ft.Icons.REFRESH)
            standorte = get_standorte_from_db()
            _standorte_cache['data'] = standorte
            _standorte_cache['loaded'] = True
            _standorte_cache['loading'] = False
        else:
            standorte = get_cached_standorte()

        if standorte:
            marker_layer_ref.current.markers.clear()
            marker_callout.visible = False
            selected_standort_ref["value"] = None

            standorte = _spread_nearby_markers(standorte)

            for standort in standorte:
                print(f"➕ Erstelle Marker für: {standort['firmenname']}")
                marker = create_marker_for_standort(standort, on_marker_click)
                marker_layer_ref.current.markers.append(marker)

            standorte_geladen = True
            print(f"✅ {len(standorte)} Marker hinzugefügt")
            show_load_toast("Höfe geladen", ft.Colors.GREEN_700, ft.Icons.CHECK_CIRCLE)
            site.page.update()
        else:
            print("⚠️ Keine Standorte gefunden!")
            show_load_toast("Keine Standorte gefunden", ft.Colors.AMBER_700, ft.Icons.WARNING)
            site.page.update()

    def reload_standorte(e):
        """Lädt die Standorte neu."""
        nonlocal standorte_geladen
        standorte_geladen = False
        load_standorte(force_refresh=True)

    header_row = ft.Row(
        controls=[
            ft.Icon(ft.Icons.MAP, color=ft.Colors.GREEN_700),
            ft.Text(
                "Bauernhöfe in der Nähe",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.GREEN_900,
            ),
            ft.Container(expand=True),
            ft.ElevatedButton(
                "Höfe laden",
                icon=ft.Icons.REFRESH,
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                on_click=reload_standorte,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    INITIAL_LAT = 49.48
    INITIAL_LON = 11.03
    INITIAL_ZOOM = 11

    karte = map.Map(
        expand=True,
        initial_center=map.MapLatitudeLongitude(INITIAL_LAT, INITIAL_LON),
        initial_zoom=INITIAL_ZOOM,
        interaction_configuration=map.InteractionConfiguration(
            flags=(
                map.InteractionFlag.DRAG
                | map.InteractionFlag.PINCH_ZOOM
                | map.InteractionFlag.DOUBLE_TAP_ZOOM
                | map.InteractionFlag.SCROLL_WHEEL_ZOOM
            )
        ),
        on_init=load_standorte,
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
                content=ft.Stack(
                    controls=[
                        karte,
                        marker_callout,
                        load_toast,
                    ],
                    expand=True,
                ),
                expand=True,
                border_radius=8,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            ),
        ],
        spacing=10,
        expand=True,
    )