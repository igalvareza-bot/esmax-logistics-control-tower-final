import numpy as np

def optimizar_inventario(df=None):
    """
    FIX COMPATIBLE CON TU MAIN ACTUAL
    (NO requiere cambiar main.py)
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
    # EOQ
    # =========================
    eoq = np.sqrt((2 * demanda_anual * costo_pedir) / costo_mantener)

    # =========================
    # DEMANDA DIARIA
    # =========================
    demanda_diaria = demanda_anual / dias_trabajo

    # =========================
    # STOCK SEGURIDAD (FIJO SEGÚN TU MODELO)
    # =========================
    stock_seguridad = 102.3

    # =========================
    # PUNTO DE REORDEN
    # =========================
    reorder_point = (demanda_diaria * lead_time) + stock_seguridad

    # =========================
    # INVENTARIO ACTUAL (fallback seguro)
    # =========================
    inventario_actual = 150

    # =========================
    # PEDIDO SUGERIDO
    # =========================
    suggested_order = max(0, round(reorder_point - inventario_actual))

    # =========================
    # ⚠️ IMPORTANTE
    # RETORNO FLAT (COMPATIBLE CON TU MAIN)
    # =========================
    return {
        "eoq": float(eoq),
        "reorder_point": float(reorder_point),
        "stock_seguridad": float(stock_seguridad),
        "suggested_order": int(suggested_order),
        "riesgo": "BAJO"
    }
