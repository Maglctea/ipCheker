import threading
from time import sleep

import flet as ft
from typing import Optional, Callable

from controller.ping import ping_host
from models.network import Network


class IPTableRow(ft.DataRow):
    def __init__(self, name: str, ip: str, notes: str,
                 on_select: Optional[Callable] = None,
                 on_long_press: Optional[Callable] = None,
                 ):
        super().__init__()
        self.id = None
        self.__name = ft.DataCell(ft.Text(value=name, font_family="default"))
        self.__ip = ft.DataCell(ft.Text(value=ip, font_family="default"))
        self.__notes = ft.DataCell(ft.Text(value=notes, font_family="default"))
        self.__ping = ft.DataCell(ft.Text(value="", font_family="default"))
        self.__status = ft.DataCell(ft.Text(value="Undefined", color="default", text_align=ft.TextAlign.CENTER))
        self.__on_select_changed = on_select
        self.__on_long_press = on_long_press
        self.__cells = [self.__name, self.__ip, self.__notes, self.__ping, self.__status]
        self.__running = False

    def did_mount(self):
        self.cells = self.__cells
        self.on_long_press = self.__on_long_press
        self.on_select_changed = self.__on_select_changed
        self.update()
        thread = threading.Thread(target=lambda: self.ip_status())
        thread.start()

    def will_unmount(self):
        self.__running = False

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
    def status(self) -> Optional[bool]:
        return True if self.__status.content.value == "Online" else False if self.__status.content.value == "Offline" else None

    @status.setter
    def status(self, status: Optional[bool]):
        if status:
            self.__status.content.value = "Online"
            self.__status.content.color = "green"
        elif not status:
            self.__status.content.value = "Offline"
            self.__status.content.color = "red"
        else:
            self.__status.content.value = "Undefined"
        self.update()

    def ip_status(self):
        self.__running = True
        try:
            while self.__running:
                result = ping_host(self.ip)
                self.ping = result['ping']
                self.status = result['status']
                # Задержку надо бы наверное?
        except Exception:
            return


class IPTable(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.Table = Table(columns=["Название", "IP-Адрес", "Примечания", "Пинг", "Статус"])
        self.InputContainer = InputContainer(self.add_row, self.__save_changes, self.delete_selected)
        self.selected = []

        self.Table.rows = [IPTableRow(name=row.name_network,
                                      ip=row.address_network,
                                      notes=row.description_network,
                                      on_select=self.__on_select,
                                      on_long_press=self.__on_change) for row in Network.get("*")
                           ]

    def __save_changes(self, e):
        e.control.disabled = True
        old_ip = e.control.data.ip
        row = e.control.data
        if row in self.Table.rows:
            previous_ip = row.ip

            row.name = self.InputContainer.NameInput.value
            row.ip = self.InputContainer.IpInput.value
            row.notes = self.InputContainer.NotesInput.value

            # Здесь нужно записать изменения в бд
            Network.update(old_ip, row.name, row.ip, row.notes)

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
            Network.delete(row.ip)
            self.Table.rows.remove(row)
        self.selected = []
        self.Table.update()

    def add_row(self, event=None):
        self.InputContainer.SaveButton.disabled = True
        self.InputContainer.SaveButton.data = None
        self.InputContainer.SaveButton.update()
        row = IPTableRow(name=self.InputContainer.NameInput.value,
                         ip=self.InputContainer.IpInput.value,
                         notes=self.InputContainer.NotesInput.value,
                         on_select=self.__on_select,
                         on_long_press=self.__on_change)
        try:
            Network.add(row.name, row.ip, row.notes)
            self.Table.rows.append(row)
            self.Table.update()
        except Exception as e:
            print(e)

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
    def __init__(self, on_add, on_save, on_delete):
        super().__init__()
        self.__on_add = on_add
        self.__on_save = on_save
        self.__on_delete = on_delete
        self.NameInput = InputRow("Название*", expand=3)
        self.IpInput = InputRow("IP-Адрес*", expand=1)
        self.NotesInput = InputRow("Примечания", expand=1)

    def build(self):
        self.AddButton = ft.ElevatedButton(text="Добавить", on_click=self.__on_add)
        self.SaveButton = ft.ElevatedButton(text="Сохранить", disabled=True, on_click=self.__on_save)
        self.DeleteButton = ft.ElevatedButton(text="Удалить", on_click=self.__on_delete)
        return ft.Container(border=ft.border.all(1, "#ebebeb"), border_radius=8, padding=15, expand=True,
                            content=ft.Column(controls=[
                                ft.Row(controls=[self.NameInput, self.IpInput]),
                                ft.Row(controls=[self.NotesInput]),
                                ft.Row(controls=[self.AddButton, self.SaveButton, self.DeleteButton])
                            ]))
