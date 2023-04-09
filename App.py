import flet as ft
from typing import Optional, Callable, Union
from dataclasses import dataclass


@dataclass
class Nav:
    Title: str
    icon: Union[ft.Image, ft.Icon, None]
    selected_icon = Union[ft.Image, ft.Icon, None]
    content: Optional[ft.Control]


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.window_title_bar_hidden = True
        self.page.padding = 0
        self.page.spacing = 0

        # page.fonts = {
        #     "Mont": "/fonts/mont_heavydemo.ttf"
        # }
        # page.theme = ft.Theme(font_family="Mont")

        self.TopBar = TopBar(self.page, title="IPChecker", icon=ft.Image(src="icons/icons8-проводная-сеть-30.png"),
                             height=40)

        self.contentPage = ft.Container(content=ft.Text("Всем привет!"), expand=1)
        destinations = [
            Nav(Title="Интернет", icon=ft.Image(src="icons/icons8-signal-30.png"), content=EthernetPage()),
            Nav(Title="Оргтехника", icon=ft.Image(src="icons/icons8-printer-maintenance-30.png"), content=None),
            Nav(Title="Склад", icon=ft.Image(src="icons/icons8-склад-30.png"), content=None),
            Nav(Title="Настройки", icon=ft.Image(src="icons/icons8-настройки-30.png"), content=None),
            Nav(Title="Отчёты", icon=ft.Image(src="icons/icons8-pie-chart-report-30.png"), content=None),
            Nav(Title="Панель SA", icon=ft.Image(src="icons/icons8-user-shield-30.png"), content=None)
        ]
        self.NavBar = NavBar(self.page, contentPage=self.contentPage, destinations=destinations, bgcolor="#225074",
                             gradient=ft.LinearGradient(
                                 begin=ft.alignment.top_left,
                                 end=ft.Alignment(0.8, 1),
                                 colors=[
                                     "0x296299",

                                     "0x142838",
                                 ],
                                 tile_mode=ft.GradientTileMode.MIRROR,

                             ))
        self.page.add(self.TopBar, ft.Row(controls=[self.NavBar, self.contentPage], expand=1))
        self.page.update()


class TopBar(ft.UserControl):
    def __init__(self,
                 page: ft.Page,
                 title: str = "",
                 icon: Optional[ft.Image] = None,
                 bgcolor: Optional[str] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = icon
        self.page = page
        self.title = ft.Text(title, weight=ft.FontWeight.BOLD, size=self.height // 3)
        self.bgcolor = bgcolor

    def minimize(self):
        self.page.window_minimized = True
        self.page.update()

    def build(self):
        c = ft.Container(content=self.title, expand=1)
        Title = ft.WindowDragArea(
            ft.Container(content=ft.Row(controls=[self.icon, c] if self.icon else [self.title]), padding=10), expand=1)

        ButtonsRow = ft.Row(controls=[
            TopBarButton(icon=ft.icons.UPDATE),
            TopBarButton(icon=ft.icons.MINIMIZE, on_click=lambda e: self.minimize()),
            TopBarButton(icon=ft.icons.CLOSE, on_click=lambda e: self.page.window_close()),
        ], alignment=ft.MainAxisAlignment.END, spacing=0)

        return ft.Container(content=ft.Row(controls=[Title, ButtonsRow], expand=1), bgcolor=self.bgcolor)


class TopBarButton(ft.UserControl):
    def __init__(self, icon: Optional[str] = None, on_click: Optional[Callable] = None):
        super().__init__()
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))
        self.icon = icon
        self.on_click = on_click

    def build(self):
        return ft.IconButton(self.icon, on_click=self.on_click, style=self.style, width=50, expand=1)


class NavBar(ft.UserControl):  # TODO add exit button
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
                icon_content=dst.icon, label=dst.Title
            ))

        rail = ft.NavigationRail(
            label_type=ft.NavigationRailLabelType.ALL,
            # extended=True,
            min_width=100,
            min_extended_width=400,
            leading=ft.Row(controls=[  # TODO add leading control
                ft.Image(src="icons/icons8-модератор-100.png", width=60, height=60),
                ft.Container(ft.Column(controls=[
                    ft.Text("Чернышов В. Н.", weight=ft.FontWeight.BOLD),
                    ft.Text("Администратор")]
                ), padding=15)
            ]),
            group_alignment=-0.9,
            destinations=destinations,
            on_change=lambda e: self.change(e.control.selected_index),
            bgcolor="transparent")

        rail.selected_index = 0
        self.contentPage.content = self.destinations[rail.selected_index].content

        return ft.Container(content=rail, bgcolor=self.bgcolor, gradient=self.gradient)


class IPTable(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.SaveButton = None
        self.datatable = None
        self.inputs = []
        self.selected = []

    def save_changes(self, e):
        e.control.disabled = True
        if e.control.data in self.datatable.rows:
            e.control.data.cells = [
                *[ft.DataCell(content=ft.Text(value=input.value)) for input in self.inputs]
            ]
        self.update()

    def delete_selected(self):
        for row in self.selected:
            self.datatable.rows.remove(row)
        self.selected = []
        self.update()

    def on_select(self, e):
        e.control.selected = not e.control.selected
        if e.control.selected:
            self.selected.append(e.control)
        else:
            self.selected.remove(e.control)
        self.update()

    def change(self, e):
        for index, input in enumerate(self.inputs):
            input.value = e.control.cells[index].content.value
        self.SaveButton.disabled = False
        self.SaveButton.data = e.control
        self.update()

    def __add_input_field(self, label: str, expand):
        inputF = ft.TextField(
            border_color="transparent",
            height=30,
            text_size=15,
            content_padding=0,
            cursor_color="black",
            cursor_width=1,
            cursor_height=18,
            color="black",
        )
        self.inputs.append(inputF)
        return ft.Container(content=ft.Column(
            spacing=1,
            controls=[
                ft.Text(value=label, size=13, color="black", weight=ft.FontWeight.BOLD),
                inputF
            ]
        ),
            expand=expand,
            height=60,
            bgcolor="#ebebeb",
            border_radius=6,
            padding=8
        )

    def add_row(self, e):
        self.SaveButton.data = None
        self.SaveButton.disabled = True
        row = ft.DataRow(cells=[
            *[ft.DataCell(content=ft.Text(value=input.value)) for input in self.inputs]
        ], on_select_changed=self.on_select, on_long_press=self.change)
        e.control.data = row
        self.datatable.rows.append(row)
        self.update()

    def build(self):
        self.datatable = ft.DataTable(columns=[
            ft.DataColumn(label=ft.Text(value="Название")),
            ft.DataColumn(label=ft.Text(value="IP-Адрес")),
            ft.DataColumn(label=ft.Text(value="Статус")),
            ft.DataColumn(label=ft.Text(value="Пинг")),
            ft.DataColumn(label=ft.Text(value="Примечания")),
        ], show_checkbox_column=True,
            horizontal_lines=ft.BorderSide(2),
            vertical_lines=ft.BorderSide(2),
            border=ft.border.all(2),
            divider_thickness=0,
            rows=[

            ],
            expand=1,
        )

        self.SaveButton = ft.ElevatedButton(text="Сохранить", disabled=True, on_click=self.save_changes)

        InputRow = ft.Container(border=ft.border.all(1, "#ebebeb"), border_radius=8, padding=15, expand=True,
                                content=ft.Column(controls=[
                                    ft.Row(controls=[self.__add_input_field("Название", 3),
                                                     self.__add_input_field("IP-Адрес", 1)]),
                                    ft.Row(controls=[
                                        self.__add_input_field("Статус", 1),
                                        self.__add_input_field("Пинг", 1),
                                        self.__add_input_field("Примечания", 3)
                                    ]),
                                    ft.Row(controls=[
                                        ft.ElevatedButton(text="Добавить", on_click=self.add_row),
                                        self.SaveButton,
                                        ft.ElevatedButton(text="Удалить", on_click=lambda e: self.delete_selected())
                                    ])
                                ]))

        return ft.Container(content=ft.Column(controls=[
            ft.Row(controls=[InputRow]),
            ft.ListView(controls=[ft.Container(self.datatable)])
        ], expand=1), padding=15)


class EthernetPage(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        deviceRow = ft.Container(content=ft.Column(controls=[
            ft.Text("Сетевой адаптер: "),  # TODO add OOP
            ft.Text("Текущая скорость интернета: ")
        ]), padding=15
        )

        return ft.Column(controls=[deviceRow, IPTable()])


if __name__ == "__main__":
    ft.app(App, assets_dir="Resources")
