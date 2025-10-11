from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.appbar import (
    MDTopAppBar,
    MDTopAppBarTitle,
)
from kivymd.uix.navigationbar import (
    MDNavigationBar,
    MDNavigationItem,
    MDNavigationItemLabel,
    MDNavigationItemIcon,
)
from kivymd.uix.screenmanager import MDScreenManager
from ui.screen import HomeScreen, Graph1Screen, Graph2Screen, AmortizacionScreen


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(MDNavigationItemIcon(icon=self.icon))
        self.add_widget(MDNavigationItemLabel(text=self.text))


class MyPrestamoApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"

        return MDBoxLayout(
            MDTopAppBar(
                MDTopAppBarTitle(text="Simulador de prestamos", halign="center"),
            ),
            MDScreenManager(
                HomeScreen(),
                Graph1Screen(),
                Graph2Screen(),
                AmortizacionScreen(),
                size_hint=(1, 0.5),
                id="screen_manager",
            ),
            MDNavigationBar(
                BaseMDNavigationItem(
                    icon="calculator",
                    text="Calculo",
                    active=True,
                ),
                BaseMDNavigationItem(
                    icon="chart-line",
                    text="Amortizacion",
                ),
                BaseMDNavigationItem(
                    icon="chart-bar",
                    text="Vs",
                ),
                on_switch_tabs=self.on_switch_tabs,
            ),
            orientation="vertical",
            md_bg_color=self.theme_cls.backgroundColor,
        )

    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        manager: MDScreenManager = self.root.get_ids().screen_manager
        if item_icon == "chart-line":
            home: HomeScreen = manager.get_screen("calculator")
            chart_line: Graph1Screen = manager.get_screen(item_icon)

            monto_prestamo, tasa_interes, plazo = home.get_data()
            chart_line.principal = monto_prestamo
            chart_line.rate = tasa_interes
            chart_line.years = plazo

        self.root.get_ids().screen_manager.current = item_icon
