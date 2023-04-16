import flet as ft
from typing import Optional, Callable


class TopBar(ft.UserControl):
    def __init__(self,
                 page: ft.Page,
                 bgcolor: Optional[str] = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.__bgcolor = bgcolor
        self.Buttons = Buttons(self.page)

    def build(self):
        drag_area = ft.WindowDragArea(
            ft.Container(), expand=1)
        return ft.Container(content=ft.Row(controls=[drag_area, self.Buttons], expand=1), bgcolor=self.__bgcolor)


class TopBarIconButton(ft.IconButton):
    def __init__(self, icon: str, on_click: Callable = None):
        super().__init__(
            width=50,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)),
            icon=icon,
            on_click=on_click)


class Buttons(ft.UserControl):
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
