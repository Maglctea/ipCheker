import flet as ft
from typing import Optional, Callable


class TopBar(ft.UserControl):
    def __init__(self,
                 page: ft.Page,
                 bgcolor: Optional[str] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__page = page
        self.__bgcolor = bgcolor
        self.Buttons = ButtonsRow(self.__page)
        self.Buttons.height = kwargs["height"]

    def build(self):
        drag_area = ft.WindowDragArea(
            ft.Container(), expand=1)
        return ft.Container(content=ft.Row(controls=[drag_area, self.Buttons], expand=1), bgcolor=self.__bgcolor)


class TopBarIconButton(ft.UserControl):
    def __init__(self, icon: Optional[str] = None, on_click: Optional[Callable] = None):
        super().__init__()
        self.__btn = None
        self.__style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))
        self.__icon = icon
        self.__on_click = on_click

    @property
    def icon(self):
        return self.__icon

    @icon.setter
    def icon(self, icon):
        self.__icon = icon
        self.__btn.icon = self.__icon
        self.update()

    def update(self):
        self.__btn.update()

    @property
    def on_click(self):
        return self.__on_click

    @on_click.setter
    def on_click(self, on_click: Optional[Callable]):
        self.__on_click = on_click
        self.__btn.on_click = self.__on_click
        self.__btn.update()

    def build(self):
        self.__btn = ft.IconButton(self.__icon, on_click=self.__on_click, style=self.__style, width=50, expand=1)
        return self.__btn


class ButtonsRow(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.minimizeBtn = TopBarIconButton(icon=ft.icons.MINIMIZE, on_click=lambda e: self.__minimize())
        self.closeBtn = TopBarIconButton(icon=ft.icons.CLOSE, on_click=lambda e: self.page.window_close())
        self.updateBtn = TopBarIconButton(icon=ft.icons.UPDATE)
        self.themeBtn = TopBarIconButton(
            icon=ft.icons.DARK_MODE if self.page.theme_mode.value == 'light' else ft.icons.LIGHT_MODE,
            on_click=lambda e: self.change_theme('dark' if self.page.theme_mode.value == 'light' else 'light'))

    def change_theme(self, theme):
        if theme == ft.ThemeMode.LIGHT.value:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.themeBtn.icon = ft.icons.DARK_MODE
        elif theme == ft.ThemeMode.DARK.value:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.themeBtn.icon = ft.icons.LIGHT_MODE
        self.themeBtn.update()
        self.page.update()

    def __minimize(self):
        self.page.window_minimized = True
        self.page.update()

    def build(self):
        return ft.Row(controls=[self.themeBtn, self.updateBtn, self.minimizeBtn, self.closeBtn],
                      alignment=ft.MainAxisAlignment.END, spacing=0)
