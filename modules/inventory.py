import numpy as np
import pandas as pd

def calcular_kpis(df):
    """
    KPIs logísticos + compatibilidad con main.py
    """

    res = {
        "fill_rate": 0.0,
        "mae": 0.0,                     # 👈 MANTENER PARA NO ROMPER MAIN
        "desviacion_demanda": 0.0,     # 👈 NUEVO NOMBRE LOGÍSTICO
        "inventario_prom": 0.0
    }

    # =========================
    # Fill rate + desviación
    # =========================
    if "demanda" in df.columns and "ventas" in df.columns:
        mask = df["demanda"] > 0

        if mask.any():
            fr = (df.loc[mask, "ventas"] / df.loc[mask, "demanda"]).mean()
        else:
            fr = 0.0

        res["fill_rate"] = float(fr)

        error = (df["demanda"] - df["ventas"]).abs().mean()

        res["mae"] = float(error)  # 👈 MAIN FUNCIONA
        res["desviacion_demanda"] = float(error)  # 👈 LOGÍSTICO

    elif "demanda" in df.columns:
        error = float(df["demanda"].abs().mean())

        res["mae"] = error
        res["desviacion_demanda"] = error
        res["fill_rate"] = 0.0

    # =========================
    # Inventario promedio
    # =========================
    if "inventario" in df.columns:
        res["inventario_prom"] = float(df["inventario"].mean())

    return res
