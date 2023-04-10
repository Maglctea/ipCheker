import flet as ft


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
            ft.DataColumn(label=ft.Text(value="Примечания")),
            ft.DataColumn(label=ft.Text(value="Пинг")),
            ft.DataColumn(label=ft.Text(value="Статус")),
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
