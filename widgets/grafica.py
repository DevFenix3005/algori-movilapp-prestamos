from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from calculos import generar_serie_amortizacion


class GraficaPrestamo(QWidget):
    """
    Ventana que muestra una gráfica para el préstamo.
    tipo = 'saldo'  -> evolución del saldo (línea)
    tipo = 'comp'   -> comparación total: capital vs interés (barras)
    """
    def __init__(self, monto, tasa, plazo, tipo='saldo', parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gráfica del préstamo")
        self.setGeometry(300, 200, 800, 520)

        self.monto = monto
        self.tasa = tasa
        self.plazo = plazo
        self.tipo = tipo

        layout = QVBoxLayout()
        self.fig = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # toolbar opcional para zoom/guardado
        try:
            toolbar = NavigationToolbar(self.canvas, self)
            layout.addWidget(toolbar)
        except Exception:
            pass  # si falla, no es crítico

        self.setLayout(layout)
        self.ax = self.fig.add_subplot(111)

        if self.tipo == 'saldo':
            self.plot_balance_evolution()
        else:
            self.plot_capital_vs_interest()

    def plot_balance_evolution(self):
        meses, balances, total_capital, total_interes, cuota = generar_serie_amortizacion(
            self.monto, self.tasa, self.plazo
        )
        self.ax.clear()
        self.ax.plot(meses, balances, marker='o')
        self.ax.set_title("Evolución del saldo (mes a mes)")
        self.ax.set_xlabel("Mes")
        self.ax.set_ylabel("Saldo pendiente")
        self.ax.grid(True)
        self.canvas.draw()

    def plot_capital_vs_interest(self):
        meses, balances, total_capital, total_interes, cuota = generar_serie_amortizacion(
            self.monto, self.tasa, self.plazo
        )
        self.ax.clear()
        etiquetas = ["Capital (total)", "Interés (total)"]
        valores = [total_capital, total_interes]
        self.ax.bar(etiquetas, valores)
        self.ax.set_title("Capital vs Interés (totales)")
        self.ax.set_ylabel("Monto")
        self.canvas.draw()