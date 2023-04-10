import flet as ft
from views.IPTable import IPTable


class EthernetPage(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        deviceRow = ft.Container(content=ft.Column(controls=[
            ft.Text("Сетевой адаптер: "),  # TODO add OOP
            ft.Text("Текущая скорость интернета: ")
        ]), padding=ft.padding.only(top=35, left=15)
        )

        return ft.Column(controls=[deviceRow, IPTable()])
