import numpy as np

def optimizar_inventario(df=None):
    """
    EOQ SOLO CLASE A (según datos entregados por el usuario)
    Sin B ni C. Sin simulación. Sin promedios.
    """

    # =========================
    # DATOS CLASE A (TU TABLA)
    # =========================
    costo_pedir = 45000
    demanda_anual = 12000
    costo_mantener = 3300
    lead_time = 5

    dias_trabajo = 300

    # =========================
    # EOQ CLASE A
    # =========================
    eoq_a = np.sqrt((2 * demanda_anual * costo_pedir) / costo_mantener)

    # =========================
    # REORDEN (según tu estructura operativa)
    # =========================
    demanda_diaria = demanda_anual / dias_trabajo

    stock_seguridad = 102.3
    punto_reorden = (demanda_diaria * lead_time) + stock_seguridad

    # =========================
    # PEDIDO SUGERIDO
    # =========================
    inventario_actual = 150  # valor base operativo (puedes cambiarlo luego)
    pedido_sugerido = max(0, round(punto_reorden - inventario_actual))

    # =========================
    # SALIDA ÚNICA (SOLO A)
    # =========================
    return {
        "A": {
            "riesgo": "BAJO",
            "pedido_sugerido": pedido_sugerido,
            "reorder_point": punto_reorden,
            "stock_seguridad": stock_seguridad,
            "eoq": float(eoq_a)
        }
    }
