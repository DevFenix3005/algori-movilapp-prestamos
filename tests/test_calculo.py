import pytest

from algori_movilapp_prestamos.business.calculos import (
    pmt,
    amortization_schedule,
    amortization_series,
)


# -----------------------------
# Helpers
# -----------------------------
def nearly_eq(a, b, tol=1e-6):
    return abs(a - b) <= tol


# -----------------------------
# 1) PMT conocido (sanity check)
# -----------------------------
def test_pmt_conocido_200k_12pct_20y():
    # Caso clásico: 200,000 a 12% anual, 20 años, mensual
    meses = 20 * 12
    cuota, total = pmt(200_000.0, 12.0, meses)
    # Valor esperado con fórmula PMT estándar
    esperado = 2202.1722671392195
    assert cuota == pytest.approx(esperado, rel=1e-9, abs=1e-9)
    assert total == pytest.approx(esperado * meses, rel=1e-9, abs=1e-6)


# -----------------------------
# 2) Tasa 0% (distribución lineal)
# -----------------------------
@pytest.mark.parametrize(
    "monto, meses",
    [
        (12_000.0, 12),
        (60_000.0, 60),
        (1_000.0, 1),
    ],
)
def test_tasa_cero_cuota_lineal(monto, meses):
    cuota, total = pmt(monto, 0.0, meses)
    assert cuota == pytest.approx(monto / meses, rel=0, abs=1e-12)
    assert total == pytest.approx(monto, rel=0, abs=1e-12)


def test_tasa_cero_series_lineal_y_cierre_en_cero():
    monto = 12_000.0
    anios = 1
    periodos, balances, tot_capital, tot_interes, cuota = amortization_series(
        monto, 0.0, anios
    )
    meses = anios * 12
    assert len(periodos) == meses + 1
    assert len(balances) == meses + 1
    # Saldo inicial y final
    assert balances[0] == pytest.approx(monto, abs=1e-12)
    assert balances[-1] == pytest.approx(0.0, abs=1e-9)
    # Intereses deben ser ~0 con tasa 0
    assert tot_interes == pytest.approx(0.0, abs=1e-9)
    # Capital total pagado == monto
    assert tot_capital == pytest.approx(monto, abs=1e-6)
    # Cuota == monto/meses
    assert cuota == pytest.approx(monto / meses, abs=1e-12)


# -----------------------------
# 3) Tabla: suma capital/interés y cierre exacto en 0
# -----------------------------
@pytest.mark.parametrize(
    "monto, tasa, anios",
    [
        (100_000.0, 10.0, 1),
        (200_000.0, 12.0, 20),
        (50_000.0, 5.5, 5),
    ],
)
def test_tabla_totales_y_cierre(monto, tasa, anios):
    tabla = amortization_schedule(monto, tasa, anios)
    assert tabla, "La tabla no debe venir vacía"

    # La última fila debe ser 'TOTAL'
    assert tabla[-1].period == "TOTAL"

    # Filas de meses (todas menos la última)
    filas = tabla[:-1]
    # Verifica que el saldo vaya a 0 (o muy cercano)
    assert filas[-1].balance == pytest.approx(0.0, abs=1e-6)

    # Totales reportados por la tabla
    total_cuotas_rep = tabla[-1].payment
    total_interes_rep = tabla[-1].interest
    total_capital_rep = tabla[-1].principal

    # Totales calculados por suma de filas
    total_cuotas_calc = sum(f.payment for f in filas)
    total_interes_calc = sum(f.interest for f in filas)
    total_capital_calc = sum(f.principal for f in filas)

    # Deben coincidir (con redondeos de 2 decimales en filas)
    assert total_cuotas_rep == pytest.approx(total_cuotas_calc, abs=8e-2)
    assert total_interes_rep == pytest.approx(total_interes_calc, abs=8e-2)
    assert total_capital_rep == pytest.approx(total_capital_calc, abs=8e-2)

    # El capital total pagado debe ser ~ monto
    assert total_capital_rep == pytest.approx(monto, abs=1e-2)


# -----------------------------
# 4) Serie: longitudes, monotonía y consistencia con totales
# -----------------------------
def test_serie_longitudes_monotonia_y_consistencia():
    monto = 150_000.0
    tasa = 9.0
    anios = 10

    periodos, balances, tot_capital, tot_interes, cuota = amortization_series(
        monto, tasa, anios
    )

    n_meses = anios * 12
    # Longitudes
    assert len(periodos) == n_meses + 1
    assert len(balances) == n_meses + 1

    # Saldo inicial y final
    assert balances[0] == pytest.approx(monto, abs=1e-6)
    assert balances[-1] == pytest.approx(0.0, abs=1e-6)

    # Monotonía no creciente: s0 >= s1 >= ... >= 0
    assert all(
        balances[i] >= balances[i + 1] - 1e-6 for i in range(len(balances) - 1)
    ), "El saldo debe decrecer"

    # Totales deben ser positivos y coherentes
    assert tot_capital == pytest.approx(monto, abs=1e-2)
    assert tot_interes > 0.0
    assert cuota > 0.0


# -----------------------------
# 5) Bordes: entradas inválidas devuelven estructuras seguras
# -----------------------------
@pytest.mark.parametrize(
    "monto,tasa,meses",
    [
        (0.0, 10.0, 12),
        (-1000.0, 10.0, 12),
        (10_000.0, 10.0, 0),
        (10_000.0, 10.0, -1),
    ],
)
def test_bordes_calcular_cuota(monto, tasa, meses):
    cuota, total = pmt(monto, tasa, meses)
    assert cuota == 0.0
    assert total == 0.0


@pytest.mark.parametrize(
    "monto,tasa,anios",
    [
        (0.0, 10.0, 1),
        (-1.0, 10.0, 1),
        (10_000.0, 10.0, 0),
        (10_000.0, 10.0, -2),
    ],
)
def test_bordes_tabla_y_serie(monto, tasa, anios):
    tabla = amortization_schedule(monto, tasa, anios)
    assert tabla == []

    periodos, balances, tot_cap, tot_int, cuota = amortization_series(
        monto, tasa, anios
    )
    # Convención de retorno seguro
    assert len(periodos) == 1
    assert len(balances) == 1
    assert balances[0] == pytest.approx(max(monto, 0.0), abs=1e-12)
    assert tot_cap == 0.0
    assert tot_int == 0.0
    assert cuota == 0.0
