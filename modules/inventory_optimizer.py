import numpy as np

def optimizar_inventario(df=None):
    """
    NO depende del dataframe.
    Usa parámetros fijos del negocio (A, B, C).
    """

    # =========================
    # DATOS BASE REALES (TU INPUT)
    # =========================

    productos = {
        "A": {
            "demanda": 12000,
            "costo_pedir": 45000,
            "costo_mant": 3300,
            "lead_time": 5,
            "costo_unitario": 15000,
            "dias": 300
        },
        "B": {
            "demanda": 3500,
            "costo_pedir": 45000,
            "costo_mant": 9900,
            "lead_time": 5,
            "costo_unitario": 45000,
            "dias": 300
        },
        "C": {
            "demanda": 600,
            "costo_pedir": 45000,
            "costo_mant": 26400,
            "lead_time": 5,
            "costo_unitario": 120000,
            "dias": 300
        }
    }

    resultados = {}

    for k, p in productos.items():

        D = p["demanda"]
        S = p["costo_pedir"]
        H = p["costo_mant"]

        # =========================
        # EOQ REAL (WILSON)
        # Q* = sqrt( (2DS) / H )
        # =========================
        eoq = np.sqrt((2 * D * S) / H)

        # demanda diaria
        demanda_diaria = D / p["dias"]

        # stock de seguridad simple (lead time)
        stock_seguridad = demanda_diaria * p["lead_time"]

        # punto de reorden
        reorder_point = (demanda_diaria * p["lead_time"]) + stock_seguridad

        # pedido sugerido (simple lógico)
        suggested_order = max(0, reorder_point)

        resultados[k] = {
            "demanda_anual": D,
            "eoq": round(eoq, 2),
            "stock_seguridad": round(stock_seguridad, 2),
            "reorder_point": round(reorder_point, 2),
            "suggested_order": round(suggested_order, 2)
        }

    return resultados
