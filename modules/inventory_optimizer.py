import numpy as np

def optimizar_inventario(df=None):
    """
    Modelo EOQ ABC fijo (industrial simplificado)
    Basado en datos entregados por usuario.
    """

    # =========================
    # PARÁMETROS FIJOS (TU TABLA)
    # =========================

    DIAS_TRABAJO = 300
    LEAD_TIME = 5
    COSTO_PEDIR = 45000

    clases = {
        "A": {
            "demanda": 12000,
            "costo_mantener": 3300,
            "costo_unitario": 15000
        },
        "B": {
            "demanda": 3500,
            "costo_mantener": 9900,
            "costo_unitario": 45000
        },
        "C": {
            "demanda": 600,
            "costo_mantener": 26400,
            "costo_unitario": 120000
        }
    }

    resultado = {}

    # =========================
    # CÁLCULO POR CLASE
    # =========================
    for clase, d in clases.items():

        demanda_anual = d["demanda"]
        h = d["costo_mantener"]

        # EOQ clásico
        q_opt = np.sqrt((2 * demanda_anual * COSTO_PEDIR) / h)

        # Reorder point (demanda diaria * lead time)
        demanda_diaria = demanda_anual / DIAS_TRABAJO
        reorder_point = demanda_diaria * LEAD_TIME

        # Stock de seguridad (simplificado empresarial)
        stock_seguridad = 0.2 * reorder_point

        # nivel objetivo
        nivel_objetivo = reorder_point + stock_seguridad

        resultado[clase] = {
            "EOQ": float(q_opt),
            "reorder_point": float(reorder_point),
            "stock_seguridad": float(stock_seguridad),
            "nivel_objetivo": float(nivel_objetivo),
            "demanda_anual": float(demanda_anual),
            "costo_mantener": float(h)
        }

    return resultado
