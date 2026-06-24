import numpy as np

def optimizar_inventario(df=None):
    """
    ABC EOQ + ROP compatible con main.py
    NO rompe UI
    """

    # =========================
    # DATOS FIJOS (TU TABLA)
    # =========================
    DIAS_TRABAJO = 300
    LEAD_TIME = 5
    COSTO_PEDIR = 45000

    A = {"demanda": 12000, "h": 3300}
    B = {"demanda": 3500, "h": 9900}
    C = {"demanda": 600, "h": 26400}

    clases = [A, B, C]

    # =========================
    # AGREGADOS (PARA UI SIMPLE)
    # =========================
    eoq_list = []
    rop_list = []
    ss_list = []

    inventario_simulado = 500  # solo referencia estable

    for c in clases:

        D = c["demanda"]
        H = c["h"]

        demanda_diaria = D / DIAS_TRABAJO

        # EOQ clásico
        eoq = np.sqrt((2 * D * COSTO_PEDIR) / H)

        # ROP
        reorder_point = demanda_diaria * LEAD_TIME

        # SS
        stock_seguridad = reorder_point * 0.2

        eoq_list.append(eoq)
        rop_list.append(reorder_point)
        ss_list.append(stock_seguridad)

    # =========================
    # PROMEDIOS (PARA DASHBOARD)
    # =========================
    eoq_avg = float(np.mean(eoq_list))
    rop_avg = float(np.mean(rop_list))
    ss_avg = float(np.mean(ss_list))

    # =========================
    # PEDIDO SUGERIDO (CLAVE)
    # =========================
    inventario_actual = inventario_simulado
    suggested_order = max(0, rop_avg - inventario_actual)

    # =========================
    # RIESGO
    # =========================
    if suggested_order > rop_avg * 0.5:
        riesgo = "ALTO"
    elif suggested_order > 0:
        riesgo = "MEDIO"
    else:
        riesgo = "BAJO"

    return {
        "eoq": eoq_avg,
        "reorder_point": rop_avg,
        "stock_seguridad": ss_avg,
        "suggested_order": suggested_order,
        "riesgo": riesgo
    }
