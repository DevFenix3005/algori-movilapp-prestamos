from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText

from business.calculos import pmt, amortization_schedule
from ui.components.pmt_dialog import PmtDialog
from ui.screen.amortizacion_screen import AmortizacionScreen


class HomeScreen(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw, name="calculator")
        self.add_widget(
            MDBoxLayout(
                MDAnchorLayout(
                    MDBoxLayout(
                        MDTextField(
                            MDTextFieldHintText(text="Monto de tu prestamo"),
                            id="monto_input",
                        ),
                        MDTextField(
                            MDTextFieldHintText(text="Tasa de interes"), id="tasa_input"
                        ),
                        MDTextField(
                            MDTextFieldHintText(
                                text="Plazo (años)",
                            ),
                            id="plazo_input",
                        ),
                        orientation="vertical",
                        adaptive_height=True,
                        spacing=10,
                        padding=15,
                    ),
                    anchor_y="top",
                    padding=[0, 0, 0, 15],
                ),
                MDAnchorLayout(
                    MDBoxLayout(
                        MDButton(
                            MDButtonIcon(icon="plus"),
                            MDButtonText(text="Calcular"),
                            style="elevated",
                            size_hint_x=1,
                            theme_width="Custom",
                            on_press=self.calculo_prestamo_handler,
                        ),
                        MDButton(
                            MDButtonIcon(icon="list-box"),
                            MDButtonText(text="Amortizacion"),
                            style="elevated",
                            size_hint_x=1,
                            theme_width="Custom",
                            on_release=self.mostrar_amortizacion,
                        ),
                        orientation="vertical",
                        adaptive_height=True,
                        spacing=10,
                        padding=15,
                    ),
                    anchor_y="bottom",
                    padding=15,
                ),
                size_hint=(1, 1),
                orientation="vertical",
            )
        )

    def calculo_prestamo_handler(self, instance):
        monto_prestamo, tasa_interes, plazo = self.get_data()
        PmtDialog(
            self,
            monto_prestamo,
            tasa_interes,
            plazo,
            pmt(monto_prestamo, tasa_interes, plazo * 12),
        ).show_alert_dialog()

    def mostrar_amortizacion(self, instance):
        screen_manager: MDScreenManager = self.manager
        amortizacion_screen: AmortizacionScreen = screen_manager.get_screen(
            "amortizacion"
        )

        if amortizacion_screen:
            monto_prestamo, tasa_interes, plazo = self.get_data()
            amort_rows = amortization_schedule(monto_prestamo, tasa_interes, plazo)
            data = [
                {
                    "headline": f"Periodo: {row.period}",
                    "supporting": f"Pago: {row.payment:,.2f}  Interes: {row.interest:,.2f}  Total: {(row.payment + row.interest):,.2f}",
                    "tertiary": f"Capital:{row.principal:,.2f}  Saldo:{row.balance:,.2f}",
                }
                for row in amort_rows
            ]

        amortizacion_screen.set_items(data)

        self.manager.current = "amortizacion"

    def get_data(self):
        monto_prestamo = float(self.get_ids().monto_input.text)
        tasa_interes = float(self.get_ids().tasa_input.text)
        plazo = int(self.get_ids().plazo_input.text)
        return monto_prestamo, tasa_interes, plazo
