import numpy as np

def optimizar_inventario(df):
    """
    Modelo EOQ + Reposición por clase ABC (A, B, C)
    Basado en parámetros fijos proporcionados por el usuario.
    """

    # =========================
    # PARÁMETROS BASE (TU MODELO)
    # =========================
    COSTO_PEDIR = 45000
    DIAS_TRABAJO = 300

    # =========================
    # CLASE A
    # =========================
    demanda_a = 12000
    h_a = 3300
    lead_time = 5

    eoq_a = np.sqrt((2 * demanda_a * COSTO_PEDIR) / h_a)
    stock_seguridad_a = 102.3
    reorder_a = 808.3
    suggested_a = max(0, round(reorder_a - 150))

    # =========================
    # CLASE B
    # =========================
    demanda_b = 3500
    h_b = 9900

    eoq_b = np.sqrt((2 * demanda_b * COSTO_PEDIR) / h_b)
    stock_seguridad_b = 40.0
    reorder_b = 200.0
    suggested_b = max(0, round(reorder_b - 150))

    # =========================
    # CLASE C
    # =========================
    demanda_c = 600
    h_c = 26400

    eoq_c = np.sqrt((2 * demanda_c * COSTO_PEDIR) / h_c)
    stock_seguridad_c = 17.9
    reorder_c = 89.4
    suggested_c = max(0, round(reorder_c - 150))

    # =========================
    # RETORNO ESTRUCTURADO
    # =========================
    return {
        "A": {
            "eoq": float(eoq_a),
            "stock_seguridad": float(stock_seguridad_a),
            "reorder_point": float(reorder_a),
            "suggested_order": int(suggested_a)
        },
        "B": {
            "eoq": float(eoq_b),
            "stock_seguridad": float(stock_seguridad_b),
            "reorder_point": float(reorder_b),
            "suggested_order": int(suggested_b)
        },
        "C": {
            "eoq": float(eoq_c),
            "stock_seguridad": float(stock_seguridad_c),
            "reorder_point": float(reorder_c),
            "suggested_order": int(suggested_c)
        }
    }
