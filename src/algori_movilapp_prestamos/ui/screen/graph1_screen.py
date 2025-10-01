from kivy.properties import NumericProperty
from kivy.metrics import dp
from kivy.core.image import Image as CoreImage
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from business.calculos import amortization_series

import matplotlib.pyplot as plt
import io


class Graph1Screen(MDScreen):
    principal = NumericProperty()
    rate = NumericProperty()
    years = NumericProperty()

    def __init__(self, **kw):
        super().__init__(**kw, name="chart-line")
        style = "Label"
        role = "large"
        self.add_widget(
            MDCard(
                MDBoxLayout(
                    FitImage(
                        id="graph_container",
                        size_hint_y=1,
                        fit_mode="contain",
                    ),
                    MDLabel(
                        id="label_interes",
                        halign="center",
                        font_style=style,
                        role=role,
                        size_hint=(1, 0.1),
                    ),
                    MDLabel(
                        id="label_total",
                        halign="center",
                        font_style=style,
                        role=role,
                        size_hint=(1, 0.1),
                    ),
                    MDLabel(
                        id="label_pagos",
                        halign="center",
                        font_style=style,
                        role=role,
                        size_hint=(1, 0.1),
                    ),
                    padding=dp(10),
                    spacing=dp(10),
                    orientation="vertical",
                )
            )
        )

    def on_pre_enter(self, *args):
        self.__generate_graph()

    def __generate_graph(self):
        periods, balances, total, interes, pagos = amortization_series(
            self.principal, self.rate, self.years
        )
        # Crear gráfica matplotlib
        fig, ax = plt.subplots(figsize=(6, 4), dpi=150)
        ax.plot(periods, balances)
        ax.set_xlabel("Periodo")
        ax.set_ylabel("Saldo")
        ax.grid(True)

        # Guardar en memoria
        buf = io.BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        image: FitImage = self.get_ids().graph_container
        image.texture = CoreImage(buf, ext="png").texture
        label_interes: MDLabel = self.get_ids().label_interes
        label_interes.text = f"Iteres del prestamo: {interes:0.2f}"
        label_total: MDLabel = self.get_ids().label_total
        label_total.text = f"Total a pagar: {(total + interes):0.2f}"
        label_pagos: MDLabel = self.get_ids().label_pagos
        label_pagos.text = f"Pagos por periodo: {pagos:0.2f}"
