import numpy as np

def optimizar_inventario(df=None):

    # =========================
    # PARÁMETROS DEL MODELO
    # =========================
    DIAS_TRABAJO = 300
    LEAD_TIME = 5
    COSTO_PEDIR = 45000

    # =========================
    # DATOS EXACTOS ENTREGADOS
    # =========================
    CLASES = {
        "A": {"demanda": 12000, "h": 3300},
        "B": {"demanda": 3500, "h": 9900},
        "C": {"demanda": 600, "h": 26400}
    }

    resultado = {}

    # =========================
    # CÁLCULO POR CLASE (SIN MEZCLA)
    # =========================
    for k, v in CLASES.items():

        D = v["demanda"]
        H = v["h"]

        demanda_diaria = D / DIAS_TRABAJO

        # EOQ CLÁSICO
        eoq = np.sqrt((2 * D * COSTO_PEDIR) / H)

        # REORDER POINT
        reorder_point = demanda_diaria * LEAD_TIME

        # STOCK SEGURIDAD
        stock_seguridad = reorder_point * 0.2

        resultado[k] = {
            "EOQ": float(round(eoq, 2)),
            "Demanda anual": float(D),
            "Demanda diaria": float(round(demanda_diaria, 2)),
            "Reorder Point": float(round(reorder_point, 2)),
            "Stock seguridad": float(round(stock_seguridad, 2))
        }

    # =========================
    # AGREGADOS PARA MAIN (COMPATIBILIDAD TOTAL)
    # =========================
    rop_total = sum(r["Reorder Point"] for r in resultado.values())
    ss_total = sum(r["Stock seguridad"] for r in resultado.values())

    inventario_simulado = 500

    suggested_order = max(0, rop_total - inventario_simulado)

    # =========================
    # RIESGO OPERATIVO
    # =========================
    if suggested_order > rop_total * 0.5:
        riesgo = "ALTO"
    elif suggested_order > 0:
        riesgo = "MEDIO"
    else:
        riesgo = "BAJO"

    # =========================
    # RETURN COMPATIBLE CON TU MAIN.PY
    # =========================
    return {
        # 🔵 CLASES SEPARADAS (LO QUE PEDISTE)
        "A": resultado["A"],
        "B": resultado["B"],
        "C": resultado["C"],

        # 🟢 CAMPOS QUE TU MAIN USA (NO SE ROMPE)
        "eoq": float((resultado["A"]["EOQ"] + resultado["B"]["EOQ"] + resultado["C"]["EOQ"]) / 3),
        "reorder_point": float(rop_total / 3),
        "stock_seguridad": float(ss_total / 3),
        "suggested_order": float(suggested_order),
        "riesgo": riesgo
    }
