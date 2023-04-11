import flet as ft
from views.EthernetPage import EthernetPage
from views.TopBar import TopBar
from views.NavBar import NavBar, Nav


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.window_title_bar_hidden = True
        self.page.padding = 0
        self.page.spacing = 0
        self.page.window_center()
        self.page.theme_mode = ft.ThemeMode.DARK

        page.fonts = {
            "MontLight": "/fonts/mont_extralightdemo.ttf",
            "Mont": "/fonts/mont_heavydemo.ttf"
        }
        page.theme = ft.Theme(font_family="Mont")
        page.dark_theme = ft.Theme(font_family="Mont")

        self.TopBar = TopBar(self.page, height=40)
        self.NavBar = NavBar(self.page)
        self.page.add(
            ft.Stack(controls=[self.NavBar, self.TopBar], expand=1))
        self.page.update()

    def change_theme(self, theme: str):
        self.TopBar.Buttons.change_theme(theme)


if __name__ == "__main__":
    ft.app(App, assets_dir="../resources")
