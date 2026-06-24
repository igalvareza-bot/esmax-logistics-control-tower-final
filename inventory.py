import numpy as np
import pandas as pd

def calcular_kpis(df):
    """
    Devuelve dict con keys:
    - fill_rate
    - desviacion_demanda (antes MAE)
    - inventario_prom
    """
    res = {
        "fill_rate": 0.0,
        "desviacion_demanda": 0.0,
        "inventario_prom": 0.0
    }

    if "demanda" in df.columns and "ventas" in df.columns:
        mask = df["demanda"] > 0

        if mask.any():
            fr = (df.loc[mask, "ventas"] / df.loc[mask, "demanda"]).mean()
        else:
            fr = 0.0

        res["fill_rate"] = float(fr)

        # 🔥 RENOMBRADO (antes MAE)
        res["desviacion_demanda"] = float(
            (df["demanda"] - df["ventas"]).abs().mean()
        )

    elif "demanda" in df.columns:
        res["desviacion_demanda"] = float(df["demanda"].abs().mean())
        res["fill_rate"] = 0.0

    if "inventario" in df.columns:
        res["inventario_prom"] = float(df["inventario"].mean())
    else:
        res["inventario_prom"] = 0.0

    return res


# =========================
# ABC CLASIFICACIÓN
# =========================
def clasificacion_abc(df):
    resumen = df.groupby("sku")["demanda"].sum().reset_index()
    resumen = resumen.sort_values(by="demanda", ascending=False)

    resumen["acumulado"] = resumen["demanda"].cumsum() / resumen["demanda"].sum()

    def categoria(x):
        if x <= 0.8:
            return "A"
        elif x <= 0.95:
            return "B"
        else:
            return "C"

    resumen["ABC"] = resumen["acumulado"].apply(categoria)

    return resumen
