import threading

import flet as ft

from controller.speed import get_internet_speed
from views.IPTable import IPTable
from Nav import Nav


class EthernetPage(Nav):
    def __init__(self, title, icon_src):
        super().__init__(title=title, icon_src=icon_src)
        self.IPTable = IPTable()
        self.EthernetAdapter = EthernetAdapter()
        self.data = ft.Container(content=ft.Column(controls=[self.EthernetAdapter, self.IPTable]), expand=1)


class EthernetAdapter(ft.UserControl):
    def __init__(self, adapter: str = "", ethernet_speed: str = ""):
        super().__init__()
        self._adapter = ft.Text(value=adapter)
        self._ethernet_speed = ft.Text(value=ethernet_speed)

        thread = threading.Thread(target=lambda: self.speed_control())
        thread.start()

    def speed_control(self):
        while True:
            speed = get_internet_speed()
            if speed:
                self.ethernet_speed = f'Загрузка: {speed["download"]:.2f} mbps | Выгрузка: {speed["upload"]:.2f} mbps'

    @property
    def adapter(self):
        return self._adapter.value

    @adapter.setter
    def adapter(self, adapter: str):
        self._adapter.value = adapter
        self._adapter.update()

    @property
    def ethernet_speed(self):
        return self._ethernet_speed.value

    @ethernet_speed.setter
    def ethernet_speed(self, adapter: str):
        self._ethernet_speed.value = adapter
        self._ethernet_speed.update()

    def build(self):
        return ft.Container(content=ft.Column(controls=[
            ft.Row(controls=[ft.Text("Сетевой адаптер: ", weight=ft.FontWeight.BOLD), self._adapter]),
            ft.Row(controls=[ft.Text("Текущая скорость интернета: ", weight=ft.FontWeight.BOLD), self._ethernet_speed]),
        ]), padding=ft.padding.only(top=35, left=15)
        )
