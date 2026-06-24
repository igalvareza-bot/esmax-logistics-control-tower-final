# modules/inventory_optimizer.py
import numpy as np

def optimizar_inventario(df):
    """
    MODELO FIJO PROFESIONAL BASADO EN ABC (NO PROMEDIOS)
    """

    # =========================
    # PARÁMETROS FIJOS (SEGÚN TU MODELO EOQ)
    # =========================

    costo_pedir = 45000

    # CLASE A
    D_A = 12000
    H_A = 3300
    eoq_a = np.sqrt((2 * D_A * costo_pedir) / H_A)

    # CLASE B
    D_B = 3500
    H_B = 9900
    eoq_b = np.sqrt((2 * D_B * costo_pedir) / H_B)

    # CLASE C
    D_C = 600
    H_C = 26400
    eoq_c = np.sqrt((2 * D_C * costo_pedir) / H_C)

    # =========================
    # REGLA OPERATIVA SIMPLE
    # =========================
    stock_seguridad = {
        "A": 102.3,
        "B": 40.0,
        "C": 17.9
    }

    reorder_point = {
        "A": 808.3,
        "B": 200.0,
        "C": 89.4
    }

    suggested_order = {
        "A": max(0, round(reorder_point["A"] - 150)),
        "B": max(0, round(reorder_point["B"] - 150)),
        "C": max(0, round(reorder_point["C"] - 150)),
    }

    return {
        "A": {
            "stock_seguridad": stock_seguridad["A"],
            "reorder_point": reorder_point["A"],
            "eoq": eoq_a,
            "suggested_order": suggested_order["A"]
        },
        "B": {
            "stock_seguridad": stock_seguridad["B"],
            "reorder_point": reorder_point["B"],
            "eoq": eoq_b,
            "suggested_order": suggested_order["B"]
        },
        "C": {
            "stock_seguridad": stock_seguridad["C"],
            "reorder_point": reorder_point["C"],
            "eoq": eoq_c,
            "suggested_order": suggested_order["C"]
        }
    }
