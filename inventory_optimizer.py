import numpy as np

def optimizar_inventario(df):

    demanda_prom = float(df["demanda"].mean())
    inventario_prom = float(df["inventario"].mean())
    lead_time = 5

    # Parámetros reales
    S = 45000   # costo pedir
    H = 3300    # costo mantener
    dias = 300

    D_anual = demanda_prom * dias

    # EOQ
    eoq = np.sqrt((2 * D_anual * S) / H)

    # Demanda diaria
    demanda_diaria = demanda_prom

    # Stock de seguridad
    stock_seguridad = 1.65 * df["demanda"].std() * np.sqrt(lead_time)

    # Punto de reorden
    reorder_point = (demanda_diaria * lead_time) + stock_seguridad

    # Pedido sugerido
    suggested_order = max(0, round(reorder_point - inventario_prom))

    return {
        "demanda_prom": demanda_prom,
        "stock_seguridad": stock_seguridad,
        "reorder_point": reorder_point,
        "eoq": eoq,
        "suggested_order": suggested_order
    }
