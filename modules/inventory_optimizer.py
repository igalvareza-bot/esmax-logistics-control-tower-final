import numpy as np

def optimizar_inventario(df):
    """
    Modelo consistente EOQ + Reorder Point + Safety Stock
    TODO en misma lógica de negocio.
    """

    # =========================
    # 1. DATOS BASE (DE DF)
    # =========================
    demanda_diaria = df["demanda"].mean() if "demanda" in df.columns else 0
    std_demanda = df["demanda"].std() if "demanda" in df.columns else 0

    lead_time = df["lead_time"].mean() if "lead_time" in df.columns else 5
    inventario_actual = df["inventario"].mean() if "inventario" in df.columns else 0

    # =========================
    # 2. PARAMETROS ECONÓMICOS (FIJOS)
    # =========================
    costo_pedir = 45000
    costo_mantener = 3300
    dias_trabajo = 300

    # demanda anual coherente
    demanda_anual = demanda_diaria * dias_trabajo

    # =========================
    # 3. EOQ (ECONOMIC ORDER QUANTITY)
    # =========================
    eoq = np.sqrt((2 * demanda_anual * costo_pedir) / max(costo_mantener, 1))

    # =========================
    # 4. STOCK DE SEGURIDAD (Z=1.65)
    # =========================
    z = 1.65
    stock_seguridad = z * std_demanda * np.sqrt(lead_time)

    # =========================
    # 5. PUNTO DE REORDEN (ROP)
    # =========================
    reorder_point = (demanda_diaria * lead_time) + stock_seguridad

    # =========================
    # 6. NIVEL OBJETIVO
    # =========================
    inventario_objetivo = reorder_point

    # =========================
    # 7. PEDIDO SUGERIDO
    # =========================
    suggested_order = max(0, inventario_objetivo - inventario_actual)

    # =========================
    # 8. RIESGO OPERATIVO
    # =========================
    if suggested_order > reorder_point * 0.5:
        riesgo = "ALTO"
    elif suggested_order > 0:
        riesgo = "MEDIO"
    else:
        riesgo = "BAJO"

    return {
        "eoq": float(eoq),
        "reorder_point": float(reorder_point),
        "stock_seguridad": float(stock_seguridad),
        "suggested_order": float(suggested_order),
        "riesgo": riesgo
    }
