import flet as ft
from typing import Optional, Callable


class IPTableRow(ft.DataRow):
    def __init__(self, name: str, ip: str, notes: str,
                 on_select: Optional[Callable] = None,
                 on_long_press: Optional[Callable] = None):
        super().__init__(on_select_changed=on_select, on_long_press=on_long_press)
        self.__name = ft.DataCell(ft.Text(value=name, font_family="default"))
        self.__ip = ft.DataCell(ft.Text(value=ip, font_family="default"))
        self.__notes = ft.DataCell(ft.Text(value=notes, font_family="default"))
        self.__ping = ft.DataCell(ft.Text(value="", font_family="default"))
        self.__status = ft.DataCell(ft.Text(value="Offline", color="red"))

        self.cells = [self.__name, self.__ip, self.__notes, self.__ping, self.__status]

    @property
    def name(self):
        return self.__name.content.value

    @name.setter
    def name(self, name):
        self.__name.content.value = name
        self.update()

    @property
    def ip(self):
        return self.__ip.content.value

    @ip.setter
    def ip(self, name):
        self.__ip.content.value = name
        self.update()

    @property
    def notes(self):
        return self.__notes.content.value

    @notes.setter
    def notes(self, name):
        self.__notes.content.value = name
        self.update()

    @property
    def ping(self):
        return self.__ping.content.value

    @ping.setter
    def ping(self, name):
        self.__ping.content.value = name
        self.update()

    @property
    def status(self) -> bool:
        return True if self.__status.content.value == "Online" else False

    @status.setter
    def status(self, status: bool):
        if status:
            self.__status.content.value = "Online"
            self.__status.content.color = "green"
        else:
            self.__status.content.value = "Offline"
            self.__status.content.color = "red"
        self.update()


class IPTable(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.Table = Table(columns=["Название", "IP-Адрес", "Примечания", "Пинг", "Статус"])
        self.InputContainer = InputContainer()
        self.selected = []

        self.InputContainer.AddButton.on_click = self.add_row
        self.InputContainer.DeleteButton.on_click = self.delete_selected
        self.InputContainer.SaveButton.on_click = self.__save_changes

    def __save_changes(self, e):
        e.control.disabled = True
        row = e.control.data
        if row in self.Table.rows:
            row.name = self.InputContainer.NameInput.value
            row.ip = self.InputContainer.IpInput.value
            row.notes = self.InputContainer.NotesInput.value
        e.control.data = None
        e.control.update()

    def __on_change(self, e):
        self.InputContainer.NameInput.value = e.control.name
        self.InputContainer.IpInput.value = e.control.ip
        self.InputContainer.NotesInput.value = e.control.notes
        self.InputContainer.SaveButton.disabled = False
        self.InputContainer.SaveButton.data = e.control
        self.InputContainer.update()

    def __on_select(self, e):
        e.control.selected = not e.control.selected
        if e.control.selected:
            self.selected.append(e.control)
        else:
            self.selected.remove(e.control)
        e.control.update()

    def delete_selected(self, e):
        for row in self.selected:
            self.Table.rows.remove(row)
        self.selected = []
        self.Table.update()

    def add_row(self, e):
        self.InputContainer.SaveButton.disabled = True
        self.InputContainer.SaveButton.data = None
        self.InputContainer.SaveButton.update()
        row = IPTableRow(name=self.InputContainer.NameInput.value,
                         ip=self.InputContainer.IpInput.value,
                         notes=self.InputContainer.NotesInput.value,
                         on_select=self.__on_select,
                         on_long_press=self.__on_change)
        self.Table.rows.append(row)
        self.Table.update()

    def build(self):
        return ft.Container(content=ft.Column(controls=[
            self.InputContainer,
            ft.Row(controls=[ft.Container(self.Table, expand=1)])]
        ), padding=15, expand=1)


class Table(ft.DataTable):
    def __init__(self, columns: list[str]):
        super().__init__(
            columns=[ft.DataColumn(label=ft.Text(value=value)) for value in columns],
            show_checkbox_column=True,
            divider_thickness=1,
            rows=[],
            expand=1)


class InputRow(ft.UserControl):
    def __init__(self, label, expand):
        super().__init__()
        self.expand = expand
        self.label = label
        self.__TextField = ft.TextField(
            border_color="transparent",
            height=30,
            text_size=15,
            content_padding=0,
            cursor_color="black",
            cursor_width=1,
            cursor_height=18,
            color="black",
            text_style=ft.TextStyle(font_family="default")
        )

    @property
    def value(self):
        return self.__TextField.value

    @value.setter
    def value(self, value):
        self.__TextField.value = value
        self.__TextField.update()

    def build(self):
        return ft.Container(content=ft.Column(
            spacing=1,
            controls=[
                ft.Text(value=self.label, size=13, color="black", weight=ft.FontWeight.BOLD),
                self.__TextField
            ]
        ),
            expand=self.expand,
            height=60,
            bgcolor="#ebebeb",
            border_radius=6,
            padding=8
        )


class InputContainer(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.AddButton = ft.ElevatedButton(text="Добавить")
        self.SaveButton = ft.ElevatedButton(text="Сохранить", disabled=True)
        self.DeleteButton = ft.ElevatedButton(text="Удалить")

        self.NameInput = InputRow("Название", expand=3)
        self.IpInput = InputRow("IP-Адрес", expand=1)
        self.NotesInput = InputRow("Примечания", expand=1)

    def build(self):
        return ft.Container(border=ft.border.all(1, "#ebebeb"), border_radius=8, padding=15, expand=True,
                            content=ft.Column(controls=[
                                ft.Row(controls=[self.NameInput, self.IpInput]),
                                ft.Row(controls=[self.NotesInput]),
                                ft.Row(controls=[self.AddButton, self.SaveButton, self.DeleteButton])
                            ]))
