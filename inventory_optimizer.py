# modules/inventory_optimizer.py
import numpy as np

def optimizar_inventario(df):
    """
    Interfaz simple esperada por main.py.
    Retorna dict con recomendaciones básicas.
    """
    demanda_prom = float(df["demanda"].mean()) if "demanda" in df.columns else 0.0
    lead_time_prom = float(df["lead_time"].mean()) if "lead_time" in df.columns else 1.0
    inventario_prom = float(df["inventario"].mean()) if "inventario" in df.columns else 0.0

    stock_seguridad = 1.65 * df["demanda"].std() * np.sqrt(lead_time_prom) if "demanda" in df.columns else 0.0
    reorder_point = (demanda_prom * lead_time_prom) + stock_seguridad
    eoq = np.sqrt((2 * max(1, demanda_prom) * 5000) / max(0.1, 2))  # parámetros supuestos

    suggested_order = max(0, round(reorder_point - inventario_prom))

    return {
        "demanda_prom": demanda_prom,
        "lead_time_prom": lead_time_prom,
        "inventario_prom": inventario_prom,
        "stock_seguridad": stock_seguridad,
        "reorder_point": reorder_point,
        "eoq": eoq,
        "suggested_order": suggested_order
    }
