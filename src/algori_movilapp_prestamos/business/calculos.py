from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Union

Number = Union[float, int]


# ------------------------------------------------------------
# 1) PMT - cuota fija de una anualidad (método francés)
# ------------------------------------------------------------
def pmt(
    principal: Number,
    annual_rate_pct: Number,
    n_periods: int,
    *,
    payments_per_year: int = 12,
) -> Tuple[float, float]:
    """
    Calcula la cuota periódica fija (PMT) para un préstamo/amortización nivelada.
    Usa fórmula: P * [i (1+i)^n] / [(1+i)^n - 1], con i = tasa por periodo.
    Si la tasa es 0, PMT = principal / n_periods.
    Retorna float; si use_decimal=True, internamente usa Decimal y redondea a 2 decimales.
    """
    if n_periods <= 0 or principal <= 0:
        return 0.0, 0.0

    # modo float
    monto = float(principal)
    i = float(annual_rate_pct) / 100.0 / float(payments_per_year)
    if i == 0.0:
        cuota = monto / n_periods
    else:
        factor = (1.0 + i) ** n_periods
        cuota = monto * (i * factor) / (factor - 1.0)
    return cuota, cuota * n_periods


# ------------------------------------------------------------
# 2) Tabla de amortización
# ------------------------------------------------------------
@dataclass
class AmortRow:
    period: int
    payment: float
    interest: float
    principal: float
    balance: float


def amortization_schedule(
    principal: Number,
    annual_rate_pct: Number,
    years: Number,
    *,
    payments_per_year: int = 12,
) -> List[AmortRow]:
    """
    Genera una tabla de amortización método francés.
    Ajusta el último pago para cerrar el saldo en 0.
    """
    # Validaciones
    total_periods = int(round(float(years) * payments_per_year))
    if total_periods <= 0 or principal <= 0:
        return []

    # modo float
    i = float(annual_rate_pct) / 100.0 / float(payments_per_year)
    cuota, cuaota_total = pmt(
        principal, annual_rate_pct, total_periods, payments_per_year=payments_per_year
    )
    saldo = float(principal)
    rows: List[AmortRow] = []
    total_interes = 0.0
    total_capital = 0.0

    for t in range(1, total_periods + 1):
        interes = saldo * i if i != 0.0 else 0.0
        capital = cuota - interes

        if t == total_periods:
            capital = saldo
            interes = cuota - capital if i != 0.0 else 0.0
            pago_efectivo = capital + interes
        else:
            pago_efectivo = cuota

        saldo -= capital
        total_interes += interes
        total_capital += capital

        if saldo < 0.0:
            saldo = 0.0

        rows.append(
            AmortRow(
                period=t,
                payment=round(pago_efectivo, 2),
                interest=round(interes, 2),
                principal=round(capital, 2),
                balance=round(saldo, 2),
            )
        )
    rows.append(
        AmortRow(
            period="TOTAL",
            payment=round(sum(f.payment for f in rows), 2),
            interest=round(total_interes, 2),
            principal=round(total_capital, 2),
            balance=0,
        )
    )
    return rows


# ------------------------------------------------------------
# 3) Serie para gráficas (saldo vs tiempo) + totales
# ------------------------------------------------------------
def amortization_series(
    principal: Number,
    annual_rate_pct: Number,
    years: Number,
    *,
    payments_per_year: int = 12,
) -> Tuple[List[int], List[float], float, float, float]:
    """
    Devuelve:
      - periods: [0, 1, ..., n]
      - balances: [saldo_inicial, ..., saldo_final=0]
      - total_principal, total_interest
      - payment (cuota fija teórica)
    La serie usa la misma lógica de schedule (ajuste en el último periodo),
    pero no devuelve la lista de pagos por mes.
    """
    principal = float(principal) if principal > 0 else 0.0

    rows = amortization_schedule(
        principal,
        annual_rate_pct,
        years,
        payments_per_year=payments_per_year,
    )
    if not rows:
        return [0], [principal], 0.0, 0.0, 0.0

    total_row = rows.pop()
    periods = [0] + [r.period for r in rows]
    balances = [principal] + [r.balance for r in rows]
    total_principal = total_row.principal
    total_interest = total_row.interest

    n_periods = len(rows)
    pay = (
        rows[0].payment if n_periods > 0 else 0.0
    )  # cuota fija teórica (el último puede variar centavos)

    return (
        periods,
        balances,
        round(total_principal, 2),
        round(total_interest, 2),
        round(pay, 2),
    )
