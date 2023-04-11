import flet as ft
from views.IPTable import IPTable1, IPTable


class EthernetPage(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.IPTable = IPTable1()
        self.EthernetAdapter = EthernetAdapter()

    def build(self):
        return ft.Container(content=ft.Column(controls=[self.EthernetAdapter, self.IPTable]), expand=1)


class EthernetAdapter(ft.UserControl):
    def __init__(self, adapter: str = "", ethernet_speed: str = ""):
        super().__init__()
        self._adapter = ft.Text(value=adapter)
        self._ethernet_speed = ft.Text(value=ethernet_speed)

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
