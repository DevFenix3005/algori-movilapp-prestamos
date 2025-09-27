import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from calculos import calcular_cuota
from widgets.grafica import GraficaPrestamo


class SimuladorPrestamos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Préstamos")
        self.setGeometry(200, 200, 420, 400)

        # Widgets
        self.lbl_monto = QLabel("Monto del préstamo:")
        self.input_monto = QLineEdit()

        self.lbl_tasa = QLabel("Tasa de interés anual (%):")
        self.input_tasa = QLineEdit()

        self.lbl_plazo = QLabel("Plazo en años:")
        self.input_plazo = QLineEdit()

        self.btn_calcular = QPushButton("Calcular")
        self.btn_calcular.clicked.connect(self.calcular_prestamo)

        self.btn_graf_saldo = QPushButton("Mostrar gráfica: Evolución del saldo")
        self.btn_graf_saldo.clicked.connect(self.mostrar_grafica_saldo)

        self.btn_graf_comp = QPushButton("Mostrar gráfica: Capital vs Interés")
        self.btn_graf_comp.clicked.connect(self.mostrar_grafica_comp)

        self.lbl_resultado = QLabel("Resultado: ")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_monto)
        layout.addWidget(self.input_monto)
        layout.addWidget(self.lbl_tasa)
        layout.addWidget(self.input_tasa)
        layout.addWidget(self.lbl_plazo)
        layout.addWidget(self.input_plazo)
        layout.addWidget(self.btn_calcular)
        layout.addWidget(self.btn_graf_saldo)
        layout.addWidget(self.btn_graf_comp)
        layout.addWidget(self.lbl_resultado)

        self.setLayout(layout)

    def calcular_prestamo(self):
        try:
            monto = float(self.input_monto.text())
            tasa_anual = float(self.input_tasa.text())
            plazo_anios = int(self.input_plazo.text())

            cuota, total = calcular_cuota(monto, tasa_anual, plazo_anios)
            self.lbl_resultado.setText(f"Pago mensual: ${cuota:,.2f}\nTotal a pagar: ${total:,.2f}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Entrada inválida.\nDetalles: {e}")

    def mostrar_grafica_saldo(self):
        try:
            monto = float(self.input_monto.text())
            tasa_anual = float(self.input_tasa.text())
            plazo_anios = int(self.input_plazo.text())

            self.ventana_graf = GraficaPrestamo(monto, tasa_anual, plazo_anios, tipo='saldo')
            self.ventana_graf.show()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo generar la gráfica.\nDetalles: {e}")

    def mostrar_grafica_comp(self):
        try:
            monto = float(self.input_monto.text())
            tasa_anual = float(self.input_tasa.text())
            plazo_anios = int(self.input_plazo.text())

            self.ventana_graf = GraficaPrestamo(monto, tasa_anual, plazo_anios, tipo='comp')
            self.ventana_graf.show()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo generar la gráfica.\nDetalles: {e}")
            
def create_basic_window():
    # 1. Create a QApplication instance
    app = QApplication(sys.argv)

    # 2. Create a QMainWindow (or QWidget)
    main_window = SimuladorPrestamos()

    # 4. Show the window
    main_window.show()

    # 5. Start the application event loop
    sys.exit(app.exec_())

            
if __name__ == "__main__":
    create_basic_window()