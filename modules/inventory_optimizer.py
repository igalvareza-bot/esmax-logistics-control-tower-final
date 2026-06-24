import numpy as np

def optimizar_inventario(df=None):
    """
    EOQ ABC basado EXCLUSIVAMENTE en los datos entregados por el usuario.
    Sin promedios, sin agregaciones, sin mezcla.
    """

    # =========================
    # PARÁMETROS FIJOS
    # =========================
    DIAS_TRABAJO = 300
    LEAD_TIME = 5
    COSTO_PEDIR = 45000

    # =========================
    # DATOS EXACTOS DEL USUARIO
    # =========================
    clases = {
        "A": {
            "demanda": 12000,
            "h": 3300
        },
        "B": {
            "demanda": 3500,
            "h": 9900
        },
        "C": {
            "demanda": 600,
            "h": 26400
        }
    }

    resultado = {}

    # =========================
    # CÁLCULO POR CLASE
    # =========================
    for clase, d in clases.items():

        D = d["demanda"]
        H = d["h"]

        # EOQ (CLÁSICO)
        eoq = np.sqrt((2 * D * COSTO_PEDIR) / H)

        # DEMANDA DIARIA REAL
        demanda_diaria = D / DIAS_TRABAJO

        # REORDER POINT (ROP)
        reorder_point = demanda_diaria * LEAD_TIME

        # STOCK SEGURIDAD (20% operativo)
        stock_seguridad = reorder_point * 0.2

        resultado[clase] = {
            "EOQ": round(eoq, 2),
            "Demanda anual": D,
            "Demanda diaria": round(demanda_diaria, 2),
            "Reorder Point": round(reorder_point, 2),
            "Stock seguridad": round(stock_seguridad, 2)
        }

    return resultado
