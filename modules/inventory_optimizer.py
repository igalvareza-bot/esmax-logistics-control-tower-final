import numpy as np

def optimizar_inventario(df=None):
    """
    EOQ + ROP + SS basado en modelo ABC real
    Compatible 100% con main.py actual
    """

    # =========================
    # PARÁMETROS BASE (TU TABLA)
    # =========================
    DIAS_TRABAJO = 300
    LEAD_TIME = 5
    COSTO_PEDIR = 45000

    # =========================
    # DATOS ABC REALES
    # =========================
    clases = {
        "A": {"demanda": 12000, "h": 3300},
        "B": {"demanda": 3500, "h": 9900},
        "C": {"demanda": 600, "h": 26400}
    }

    # =========================
    # AGREGADOS GLOBAL (para UI única)
    # =========================
    demanda_total = 0
    eoq_total = 0
    reorder_total = 0
    ss_total = 0

    for c, d in clases.items():

        demanda_anual = d["demanda"]
        h = d["h"]

        demanda_diaria = demanda_anual / DIAS_TRABAJO

        # EOQ clásico
        eoq = np.sqrt((2 * demanda_anual * COSTO_PEDIR) / h)

        # Reorder Point
        reorder_point = demanda_diaria * LEAD_TIME

        # Stock de seguridad (20% buffer operativo)
        stock_seguridad = 0.2 * reorder_point

        # acumulación ponderada (para dashboard único)
        demanda_total += demanda_anual
        eoq_total += eoq
        reorder_total += reorder_point
        ss_total += stock_seguridad

    # =========================
    # INVENTARIO ACTUAL SIMULADO
    # =========================
    inventario_actual = demanda_total / DIAS_TRABAJO * 3

    # =========================
    # PEDIDO SUGERIDO
    # =========================
    suggested_order = max(0, reorder_total - inventario_actual)

    # =========================
    # RIESGO
    # =========================
    if suggested_order > reorder_total * 0.5:
        riesgo = "ALTO"
    elif suggested_order > 0:
        riesgo = "MEDIO"
    else:
        riesgo = "BAJO"

    return {
        "eoq": float(eoq_total / 3),
        "reorder_point": float(reorder_total / 3),
        "stock_seguridad": float(ss_total / 3),
        "suggested_order": float(suggested_order),
        "riesgo": riesgo
    }
