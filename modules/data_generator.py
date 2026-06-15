# modules/data_generator.py
import pandas as pd
import numpy as np

def generar_dataset_esmax(dias=180):
    np.random.seed(42)
    fechas = pd.date_range(start="2025-01-01", periods=dias, freq="D")

    demanda = np.clip(np.random.normal(150, 30, dias).astype(int), 50, None)
    ventas = np.clip(np.random.normal(145, 25, dias).astype(int), 40, None)
    sku = np.random.choice(["GAS-95", "GAS-97", "DIESEL", "KEROSENE"], dias)
    inventario = np.random.randint(800, 2500, dias)
    lead_time = np.random.randint(2, 8, dias)
    costo_unitario = np.random.randint(800, 1500, dias)

    # Construir DataFrame desde arrays del mismo tamaño
    df = pd.DataFrame({
        "fecha": fechas,
        "sku": sku,
        "demanda": demanda,
        "ventas": ventas,
        "inventario": inventario,
        "lead_time": lead_time,
        "costo_unitario": costo_unitario
    })

    df["fill_rate"] = df["ventas"] / df["demanda"]

    # Validación estricta antes de devolver
    lengths = {col: df[col].shape[0] for col in df.columns}
    if len(set(lengths.values())) != 1:
        raise ValueError(f"Inconsistent column lengths detected: {lengths}")

    return df
