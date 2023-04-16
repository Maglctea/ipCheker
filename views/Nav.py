import flet as ft


class Nav(ft.NavigationRailDestination):
    def __init__(self, title: str, icon_src: str):
        super().__init__(
            label=title,
            icon_content=ft.Image(src=icon_src, width=30, height=30),
            padding=5,
        )
