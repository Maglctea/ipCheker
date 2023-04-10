import flet as ft
from typing import Optional, Union
from dataclasses import dataclass
from typing import Optional


@dataclass
class Nav:
    Title: str
    icon: Union[ft.Image, ft.Icon, None]
    selected_icon = Union[ft.Image, ft.Icon, None]
    content: Optional[ft.Control]


class NavBar(ft.UserControl):
    def __init__(self, page: ft.Page, contentPage: ft.Container, destinations: list[Nav] = None,
                 bgcolor: Optional[str] = None,
                 gradient: Optional[ft.LinearGradient] = None):
        super().__init__()
        self.page: ft.Page = page
        self.contentPage: ft.Container = contentPage
        self.destinations: list[Nav] = destinations
        self.bgcolor: str = bgcolor
        self.gradient: Optional[ft.LinearGradient] = gradient

    def change(self, index):
        self.contentPage.content = self.destinations[index].content
        self.contentPage.update()

    def build(self):
        destinations = []
        for dst in self.destinations:
            destinations.append(ft.NavigationRailDestination(
                icon_content=dst.icon, label=dst.Title, padding=5
            ))

        rail = ft.NavigationRail(
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=150,
            min_extended_width=400,
            group_alignment=-0.9,
            destinations=destinations,
            on_change=lambda e: self.change(e.control.selected_index),
            bgcolor="transparent", )

        rail.selected_index = 0
        self.contentPage.content = self.destinations[rail.selected_index].content

        return ft.Container(content=rail, bgcolor=self.bgcolor, gradient=self.gradient,
                            padding=ft.padding.only(15, 60, 15, 15))
