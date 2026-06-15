# modules/forecast.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

def generar_forecast(df):
    """
    Interfaz esperada por main.py.
    Devuelve un DataFrame con columnas: fecha, demanda, forecast, inventario
    """
    df = df.copy()
    if "fecha" in df.columns:
        df = df.sort_values("fecha").reset_index(drop=True)

    # Si existe demanda, usar regresión lineal simple como forecast
    if "demanda" in df.columns:
        df["t"] = np.arange(len(df))
        X = df[["t"]]
        y = df["demanda"]
        model = LinearRegression()
        try:
            model.fit(X, y)
            df["forecast"] = model.predict(X)
        except Exception:
            # fallback: media móvil de 7 días
            df["forecast"] = df["demanda"].rolling(window=7, min_periods=1).mean().shift(1).fillna(df["demanda"].mean())
    else:
        df["forecast"] = np.nan

    if "inventario" not in df.columns:
        df["inventario"] = 0

    # Mantener columnas en el orden esperado
    cols = [c for c in ["fecha", "demanda", "forecast", "inventario"] if c in df.columns]
    return df[cols]
