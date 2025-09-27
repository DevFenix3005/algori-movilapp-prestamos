
def calcular_cuota(monto: float, tasa_anual: float, plazo_anios: int):
    meses = plazo_anios * 12
    tasa_mensual = tasa_anual / 100 / 12
    if meses == 0:
        return 0.0, 0.0
    if tasa_mensual == 0:
        cuota = monto / meses
    else:
        cuota = monto * (tasa_mensual * (1 + tasa_mensual) * meses) / ((1 + tasa_mensual) * meses - 1)
    total = cuota * meses
    return cuota, total


def generar_tabla_amortizacion(monto: float, tasa_anual: float, plazo_anios: int):
    """
    Devuelve una lista con la tabla de amortización redondeada.
    Cada fila: [mes, cuota, interés, capital, saldo]
    y una fila final con totales (la usamos para mostrar en QTableWidget).
    """
    meses = plazo_anios * 12
    tasa_mensual = tasa_anual / 100 / 12

    if meses == 0:
        return []

    if tasa_mensual == 0:
        cuota = monto / meses
    else:
        cuota = monto * (tasa_mensual * (1 + tasa_mensual) * meses) / ((1 + tasa_mensual) * meses - 1)

    saldo = monto
    tabla = []
    total_interes = 0.0
    total_capital = 0.0

    for mes in range(1, meses + 1):
        interes = saldo * tasa_mensual
        capital = cuota - interes
        saldo -= capital
        total_interes += interes
        total_capital += capital

        tabla.append([
            mes,
            round(cuota, 2),
            round(interes, 2),
            round(capital, 2),
            round(saldo if saldo > 0 else 0, 2)
        ])

    # Totales al final
    tabla.append([
        "TOTAL",
        round(cuota * meses, 2),
        round(total_interes, 2),
        round(total_capital, 2),
        0
    ])

    return tabla


def generar_serie_amortizacion(monto: float, tasa_anual: float, plazo_anios: int):
    """
    Devuelve series (sin redondeo) útiles para graficar:
    - meses: [0,1,...,N]
    - balances: [saldo_inicial, saldo_mes1, ..., saldo_mesN]
    - total_capital, total_interes, cuota_mensual
    """
    meses = plazo_anios * 12
    tasa_mensual = tasa_anual / 100 / 12

    if meses == 0:
        return [0], [monto], 0.0, 0.0, 0.0

    if tasa_mensual == 0:
        cuota = monto / meses
    else:
        cuota = monto * (tasa_mensual * (1 + tasa_mensual) * meses) / ((1 + tasa_mensual) * meses - 1)

    saldo = monto
    balances = [saldo]  # mes 0 = saldo inicial
    total_interes = 0.0
    total_capital = 0.0

    for mes in range(1, meses + 1):
        interes = saldo * tasa_mensual
        capital = cuota - interes
        saldo -= capital
        total_interes += interes
        total_capital += capital
        balances.append(max(saldo, 0.0))

    meses_lista = list(range(0, meses + 1))
    return meses_lista, balances, total_capital, total_interes, cuota