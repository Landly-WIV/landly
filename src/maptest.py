import random
import flet as ft
import flet_map as map


def mapPage(site):
    marker_layer_ref = ft.Ref[map.MarkerLayer]()
    circle_layer_ref = ft.Ref[map.CircleLayer]()
    

    def handle_tap(e: map.MapTapEvent):
        # print(e)
        if e.name == "tap":
            marker_layer_ref.current.markers.append(
                map.Marker(
                    content=ft.Icon(
                        ft.Icons.LOCATION_ON, color=ft.CupertinoColors.DESTRUCTIVE_RED
                    ),
                    coordinates=e.coordinates,
                )
            )
        elif e.name == "long_press":
            circle_layer_ref.current.circles.append(
                map.CircleMarker(
                    radius=random.randint(5, 10),
                    coordinates=e.coordinates,
                    color=ft.Colors.random(),
                    border_color=ft.Colors.random(),
                    border_stroke_width=4,
                )
            )
        site.page.update()

    # def handle_event(e: map.MapEvent):
    #     print(e)

    return ft.Column(
        controls=[
            ft.Text("Click anywhere to add a Marker, long-click to add a CircleMarker."),
            map.Map(
                expand=True,
                initial_center=map.MapLatitudeLongitude(15, 10),
                initial_zoom=4.2,
                interaction_configuration=map.MapInteractionConfiguration(
                    flags=map.MapInteractiveFlag.ALL
                ),
                #on_init=lambda e: print(f"Initialized Map"),
                on_tap=handle_tap,
                on_secondary_tap=handle_tap,
                on_long_press=handle_tap,
                # on_event=lambda e: print(e),
                layers=[
                    map.TileLayer(
                        url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                        #on_image_error=lambda e: print("TileLayer Error"),
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
                                text="Flet",
                                on_click=lambda e: e.page.launch_url("https://flet.dev"),
                            ),
                        ]
                    ),
                    map.SimpleAttribution(
                        text="Flet",
                        alignment=ft.alignment.top_right,
                        #on_click=lambda e: print("Clicked SimpleAttribution"),
                    ),
                    map.MarkerLayer(
                        ref=marker_layer_ref,
                        markers=[],
                    ),
                    map.CircleLayer(
                        ref=circle_layer_ref,
                        circles=[],
                    ),
                ],
            ),
        ]
    )
