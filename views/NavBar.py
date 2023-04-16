import flet as ft
from typing import Union
from dataclasses import dataclass
from typing import Optional
from EthernetPage import EthernetPage
from Nav import Nav


class NavBar(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page: ft.Page = page
        self.contentPage: ft.Container = ft.Container(expand=1)

        self.Ethernet = EthernetPage(title="Интернет",
                                     icon_src="icons/icons8-signal-30.png")
        self.OfficeEquip = Nav(title="Оргтехника", icon_src="icons/icons8-printer-maintenance-30.png")
        self.Storage = Nav(title="Склад",
                           icon_src="icons/icons8--30.png")
        self.Settings = Nav(title="Настройки",
                            icon_src="icons/icons8-settings-30.png")
        self.Reports = Nav(title="Отчёты",
                           icon_src="icons/icons8-pie-chart-report-30.png")

        self.destinations = [self.Ethernet, self.OfficeEquip, self.Storage, self.Settings, self.Reports]

    def change(self, index):
        self.contentPage.content = self.destinations[index].data
        self.contentPage.update()

    def build(self):
        rail = ft.NavigationRail(
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=150,
            min_extended_width=400,
            group_alignment=-0.9,
            destinations=self.destinations,
            on_change=lambda e: self.change(e.control.selected_index),
            bgcolor="transparent")

        rail.selected_index = 0
        self.contentPage.content = self.destinations[rail.selected_index].data

        return ft.Row(controls=[ft.Container(content=rail,
                                             padding=ft.padding.only(15, 60, 15, 15),
                                             gradient=ft.LinearGradient(
                                                 begin=ft.alignment.top_left,
                                                 end=ft.Alignment(0.8, 1),
                                                 colors=[
                                                     "0x296299",
                                                     "0x142838",
                                                 ],
                                                 tile_mode=ft.GradientTileMode.MIRROR
                                             )
                                             ), self.contentPage], expand=1)
