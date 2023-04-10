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
        self.page.theme_mode = ft.ThemeMode.DARK

        page.fonts = {
            "Mont": "/fonts/mont_heavydemo.ttf"
        }
        page.theme = ft.Theme(font_family="Mont")

        self.TopBar = TopBar(self.page, title="IPChecker", icon=ft.Image(src="icons/icons8-проводная-сеть-30.png"),
                             height=40)

        self.contentPage = ft.Container(content=ft.Text("Всем привет!"), expand=1)
        destinations = [
            Nav(Title="Интернет", icon=ft.Image(src="icons/icons8-signal-30.png", width=30, height=30),
                content=EthernetPage()),
            Nav(Title="Оргтехника", icon=ft.Image(src="icons/icons8-printer-maintenance-30.png", width=30, height=30),
                content=None),
            Nav(Title="Склад", icon=ft.Image(src="icons/icons8--30.png", width=30, height=30), content=None),
            Nav(Title="Настройки", icon=ft.Image(src="icons/icons8-settings-30.png", width=30, height=30),
                content=None),
            Nav(Title="Отчёты", icon=ft.Image(src="icons/icons8-pie-chart-report-30.png", width=30, height=30),
                content=None),
            Nav(Title="Панель SA", icon=ft.Image(src="icons/icons8-user-shield-30.png", width=30, height=30),
                content=None)
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
        self.page.add(
            ft.Stack(controls=[ft.Row(controls=[self.NavBar, self.contentPage], expand=1), self.TopBar], expand=1))
        # self.page.add(self.TopBar, ft.Row(controls=[self.NavBar, self.contentPage], expand=1))
        self.page.update()


if __name__ == "__main__":
    ft.app(App, assets_dir="../resources")
