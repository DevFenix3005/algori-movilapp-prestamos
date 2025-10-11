from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
)


class PmtDialog:
    def __init__(self, parent, monto_prestamo, tasa_interes, plazo, cuota):
        self.parent = parent
        self.monto_prestamo = monto_prestamo
        self.tasa_interes = tasa_interes
        self.plazo = plazo
        self.cuota = cuota

    def show_alert_dialog(self):
        MDDialog(
            # ----------------------------Icon-----------------------------
            MDDialogIcon(
                icon="cash",
            ),
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="Calculo del prestamo",
            ),
            # -----------------------Supporting text-----------------------
            MDDialogSupportingText(
                text=f"Monto a prestar: {self.monto_prestamo:,.2f}"
                f"\nTasa de interes: {self.tasa_interes:,.2f} %"
                f"\nPlazo del prestamo: {self.plazo * 12} meses"
                f"\nPago mensual de este prestamo:{(self.cuota[0]):,.2f}"
                f"\nPago total de este prestamo sera de:{(self.cuota[1]):,.2f}"
            ),
            # -------------------------------------------------------------
        ).open()
