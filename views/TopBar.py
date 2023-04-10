import flet as ft
from typing import Optional, Callable


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
        Title = ft.WindowDragArea(
            ft.Container(padding=10), expand=1)
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
