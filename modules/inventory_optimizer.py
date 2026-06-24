import numpy as np

def optimizar_inventario(df=None):

    # =========================
    # DATOS FIJOS (TU MODELO)
    # =========================
    DIAS_TRABAJO = 300
    LEAD_TIME = 5
    COSTO_PEDIR = 45000

    CLASES = {
        "A": {"demanda": 12000, "h": 3300},
        "B": {"demanda": 3500, "h": 9900},
        "C": {"demanda": 600, "h": 26400}
    }

    resultado = {}

    # =========================
    # CALCULO POR CLASE (SIN MEZCLA)
    # =========================
    for k, v in CLASES.items():

        D = v["demanda"]
        H = v["h"]

        demanda_diaria = D / DIAS_TRABAJO

        eoq = np.sqrt((2 * D * COSTO_PEDIR) / H)
        reorder_point = demanda_diaria * LEAD_TIME
        stock_seguridad = reorder_point * 0.2

        resultado[k] = {
            "EOQ": round(eoq, 2),
            "Demanda anual": D,
            "Demanda diaria": round(demanda_diaria, 2),
            "Reorder Point": round(reorder_point, 2),
            "Stock seguridad": round(stock_seguridad, 2)
        }

    # =========================
    # PEDIDO GLOBAL (PARA MAIN)
    # =========================
    rop_total = sum(r["Reorder Point"] for r in resultado.values())
    ss_total = sum(r["Stock seguridad"] for r in resultado.values())

    inventario_simulado = 500
    suggested_order = max(0, rop_total - inventario_simulado)

    if suggested_order > rop_total * 0.5:
        riesgo = "ALTO"
    elif suggested_order > 0:
        riesgo = "MEDIO"
    else:
        riesgo = "BAJO"

    return {
        "A": resultado["A"],
        "B": resultado["B"],
        "C": resultado["C"],

        # 👇 compatibilidad con tu main.py (NO SE ROMPE)
        "eoq": None,
        "reorder_point": rop_total / 3,
        "stock_seguridad": ss_total / 3,
        "suggested_order": suggested_order,
        "riesgo": riesgo
    }
