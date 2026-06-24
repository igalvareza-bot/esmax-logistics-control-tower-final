import numpy as np

def optimizar_inventario(df):
    """
    EOQ REAL basado en parámetros de negocio (no datos simulados).
    """

    # =========================
    # PARAMETROS DE NEGOCIO
    # =========================
    costo_pedir = 45000
    demanda_anual = 12000
    costo_mantencion = 3300
    dias_trabajo = 300
    lead_time = 5

    # =========================
    # EOQ REAL
    # =========================
    eoq = np.sqrt((2 * demanda_anual * costo_pedir) / costo_mantencion)

    # demanda diaria real
    demanda_diaria = demanda_anual / dias_trabajo

    # punto de reorden real
    reorder_point = demanda_diaria * lead_time

    # stock de seguridad (puedes ajustarlo luego)
    stock_seguridad = reorder_point * 0.2

    # inventario objetivo
    inventario_objetivo = reorder_point + stock_seguridad

    # inventario actual (si existe el DF)
    inventario_actual = df["inventario"].mean() if "inventario" in df.columns else 0

    # pedido sugerido REAL
    suggested_order = max(0, inventario_objetivo - inventario_actual)

    return {
        "eoq": float(eoq),
        "reorder_point": float(reorder_point),
        "stock_seguridad": float(stock_seguridad),
        "suggested_order": float(suggested_order)
    }
