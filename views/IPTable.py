import flet as ft
from typing import Optional, Callable


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
            e.control.data.cells = self.create_row().cells
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

    def create_row(self, ping: str = "", status: str = ""):
        return ft.DataRow(cells=[
            *[ft.DataCell(content=ft.Text(value=input.value)) for input in self.inputs],
            ft.DataCell(content=ft.Text(value=ping)),
            ft.DataCell(content=ft.Text(value=status,
                                        color="green" if status == "Online" else "red" if status == "Offline" else None))
            # TODO need refactoring
        ], on_select_changed=self.on_select, on_long_press=self.change)

    def add_row(self):
        self.SaveButton.data = None
        self.SaveButton.disabled = True
        self.datatable.rows.append(self.create_row())
        self.update()

    def build(self):
        self.datatable = ft.DataTable(columns=[
            ft.DataColumn(label=ft.Text(value="Название")),
            ft.DataColumn(label=ft.Text(value="IP-Адрес")),
            ft.DataColumn(label=ft.Text(value="Примечания")),
            ft.DataColumn(label=ft.Text(value="Пинг")),
            ft.DataColumn(label=ft.Text(value="Статус")),
        ], show_checkbox_column=True,
            divider_thickness=1,
            rows=[],
            expand=1,
        )

        self.SaveButton = ft.ElevatedButton(text="Сохранить", disabled=True, on_click=self.save_changes)

        InputRow = ft.Container(border=ft.border.all(1, "#ebebeb"), border_radius=8, padding=15, expand=True,
                                content=ft.Column(controls=[
                                    ft.Row(controls=[self.__add_input_field("Название", 3),
                                                     self.__add_input_field("IP-Адрес", 1)]),
                                    ft.Row(controls=[
                                        self.__add_input_field("Примечания", 1)
                                    ]),
                                    ft.Row(controls=[
                                        ft.ElevatedButton(text="Добавить", on_click=lambda e: self.add_row()),
                                        self.SaveButton,
                                        ft.ElevatedButton(text="Удалить", on_click=lambda e: self.delete_selected())
                                    ])
                                ]))
        self.datatable.rows.extend([self.create_row(status="Online", ping="171 ms."),
                                    self.create_row(status="Offline")])
        return ft.Container(content=ft.Column(controls=[
            ft.Row(controls=[InputRow]),
            ft.Container(content=ft.ListView(controls=[self.datatable], expand=1))
        ],
        ), padding=15, expand=1)


class IPTableRow(ft.UserControl):
    def __init__(self, name: str, ip: str, notes: str, ping: str = "", status: bool = False,
                 on_create: Optional[Callable] = None, on_delete: Optional[Callable] = None,
                 on_select: Optional[Callable] = None,
                 on_long_press: Optional[Callable] = None):
        super().__init__()
        self._row = None
        self.name = ft.DataCell(ft.Text(value=name))
        self.ip = ft.DataCell(ft.Text(value=ip))
        self.notes = ft.DataCell(ft.Text(value=notes))
        self.ping = ft.DataCell(ft.Text(value=ping))
        self.__status = ft.DataCell(ft.Text(value=""))
        self.status = status
        self.__on_create = on_create
        self.__on_delete = on_delete
        self.__on_select = on_select
        self.__on_long_press = on_long_press

    def update(self):
        if self._row is not None:
            self._row.update()

    def did_mount(self):
        if self.__on_create is not None:
            self.__on_create()

    def will_unmount(self):
        if self.__on_delete is not None:
            self.__on_delete()

    @property
    def status(self) -> bool:
        return True if self.__status.content.value == "Online" else False

    @status.setter
    def status(self, status: bool):
        if status:
            self.__status.value = "Online"
            self.__status.color = "green"
        else:
            self.__status.value = "Offline"
            self.__status.color = "red"
        self.update()

    def build(self):
        row = ft.DataRow(cells=[self.name,
                                self.ip,
                                self.notes,
                                self.ping,
                                self.__status
                                ], on_select_changed=self.__on_select,
                         on_long_press=self.__on_long_press
                         )
        row.data = self
        self._row = row
        return row


class IPTable1(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.Table = Table(columns=["Название", "IP-Адрес", "Примечания", "Пинг", "Статус"])
        self.InputContainer = InputContainer()
        self.selected = []
        self.on_create_row: Optional[Callable] = None
        self.on_delete_row: Optional[Callable] = None

        self.InputContainer.AddButton.on_click = lambda e: self.__add_row()
        self.InputContainer.DeleteButton.on_click = lambda e: self.__delete_selected()
        self.InputContainer.SaveButton.on_click = self.__save_changes

    def __save_changes(self, e):
        e.control.disabled = True
        if e.control.data in self.Table.datatable.rows:
            index = self.Table.datatable.rows.index(e.control.data)
            self.Table.datatable.rows.remove(e.control.data)
            row = self.create_row(name=self.InputContainer.Inputs[0].value, ip=self.InputContainer.Inputs[1].value,
                                  notes=self.InputContainer.Inputs[2].value, on_create=self.on_create_row,
                                  on_delete=self.on_delete_row)
            self.Table.datatable.rows.insert(index, row.build())
        self.Table.update()
        e.control.update()

    def __on_change(self, e):
        for index, input in enumerate(self.InputContainer.Inputs):
            input.value = e.control.cells[index].content.value
        self.InputContainer.SaveButton.disabled = False
        self.InputContainer.SaveButton.data = e.control
        self.InputContainer.update()

    def __on_select(self, e):
        e.control.selected = not e.control.selected
        if e.control.selected:
            self.selected.append(e.control.data)
        else:
            self.selected.remove(e.control.data)
        e.control.update()

    def __delete_selected(self):
        for row in self.selected:
            self.Table.datatable.rows.remove(row._row)
        self.selected = []
        self.Table.datatable.update()

    def create_row(self, name: str, ip: str, notes: str, ping: str = "", status: bool = False,
                   on_create: Optional[Callable] = None,
                   on_delete: Optional[Callable] = None):
        return IPTableRow(name=name, ip=ip, notes=notes, ping=ping, status=status, on_create=on_create,
                          on_delete=on_delete, on_select=self.__on_select, on_long_press=self.__on_change)

    def add_rows_to_table(self, rows: list[IPTableRow]):
        self.Table.datatable.rows.extend([row.build() for row in rows])
        self.Table.datatable.update()

    def __add_row(self):
        row = self.create_row(name=self.InputContainer.Inputs[0].value, ip=self.InputContainer.Inputs[1].value,
                              notes=self.InputContainer.Inputs[2].value, on_create=self.on_create_row,
                              on_delete=self.on_delete_row)
        self.add_rows_to_table([row])

    def build(self):
        return ft.Container(content=ft.Column(controls=[
            self.InputContainer,
            self.Table]
        ), padding=15, expand=1)


class Table(ft.UserControl):
    def __init__(self, columns: list[str]):
        super().__init__()
        self.datatable: Optional[ft.DataTable] = None
        self.__columns = columns

    def build(self):
        self.datatable = ft.DataTable(columns=[
            ft.DataColumn(label=ft.Text(value=value)) for value in self.__columns
        ],
            show_checkbox_column=True,
            divider_thickness=1,
            rows=[],
            expand=1,
        )
        return ft.Row(controls=[ft.Container(ft.ListView(controls=[self.datatable]), expand=1)])


class InputContainer(ft.UserControl):
    def __init__(self):  # TODO inputs args
        super().__init__()
        self.AddButton = ft.ElevatedButton(text="Добавить")
        self.SaveButton = ft.ElevatedButton(text="Сохранить", disabled=True)
        self.DeleteButton = ft.ElevatedButton(text="Удалить")
        self.Inputs = []

    def __add_input_field(self, label: str, expand):
        input_field = ft.TextField(
            border_color="transparent",
            height=30,
            text_size=15,
            content_padding=0,
            cursor_color="black",
            cursor_width=1,
            cursor_height=18,
            color="black",
        )
        self.Inputs.append(input_field)
        return ft.Container(content=ft.Column(
            spacing=1,
            controls=[
                ft.Text(value=label, size=13, color="black", weight=ft.FontWeight.BOLD),
                input_field
            ]
        ),
            expand=expand,
            height=60,
            bgcolor="#ebebeb",
            border_radius=6,
            padding=8
        )

    def build(self):
        return ft.Container(border=ft.border.all(1, "#ebebeb"), border_radius=8, padding=15, expand=True,
                            content=ft.Column(controls=[
                                ft.Row(controls=[self.__add_input_field("Название", 3),
                                                 self.__add_input_field("IP-Адрес", 1)]),
                                ft.Row(controls=[
                                    self.__add_input_field("Примечания", 1)
                                ]),
                                ft.Row(controls=[self.AddButton, self.SaveButton, self.DeleteButton])
                            ]))
