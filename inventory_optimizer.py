import numpy as np

def optimizar_inventario(df):
    """
    Modelo EOQ + Reposición basado en:
    - Parámetros reales del negocio (tabla ESMAX)
    - Datos operacionales (df)
    """

    # =========================
    # 📊 DATOS OPERACIONALES
    # =========================
    demanda_prom = float(df["demanda"].mean()) if "demanda" in df.columns else 0.0
    inventario_prom = float(df["inventario"].mean()) if "inventario" in df.columns else 0.0

    demanda_std = float(df["demanda"].std()) if "demanda" in df.columns else 0.0

    # =========================
    # 📦 PARÁMETROS FIJOS (TU TABLA REAL)
    # =========================
    S = 45000      # costo de pedir
    H = 3300       # costo de mantener inventario
    D = 12000      # demanda anual (FORZADA por negocio)
    dias = 300
    lead_time = 5

    # =========================
    # 📦 EOQ (Wilson)
    # =========================
    eoq = np.sqrt((2 * D * S) / H)

    # =========================
    # 📈 DEMANDA DIARIA
    # =========================
    demanda_diaria = D / dias

    # =========================
    # 🛡 STOCK DE SEGURIDAD
    # =========================
    z = 1.65  # nivel de servicio (~95%)
    stock_seguridad = z * demanda_std * np.sqrt(lead_time)

    # =========================
    # 🎯 PUNTO DE REORDEN
    # =========================
    reorder_point = (demanda_diaria * lead_time) + stock_seguridad

    # =========================
    # 📦 PEDIDO SUGERIDO
    # =========================
    suggested_order = max(0, round(reorder_point - inventario_prom))

    # =========================
    # 📊 MÉTRICAS EXTRA
    # =========================
    riesgo = "ALTO" if inventario_prom < reorder_point else "BAJO"

    return {
        "demanda_prom": demanda_prom,
        "inventario_prom": inventario_prom,
        "demanda_std": demanda_std,
        "stock_seguridad": stock_seguridad,
        "reorder_point": reorder_point,
        "eoq": eoq,
        "suggested_order": suggested_order,
        "riesgo_operativo": riesgo
    }
