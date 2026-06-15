# sanity_check.py
from modules.data_generator import generar_dataset_esmax

df = generar_dataset_esmax(180)
print("Rows:", len(df))
print("Columns:", df.columns.tolist())
# Aserciones
assert "fecha" in df.columns
assert "demanda" in df.columns
assert "ventas" in df.columns
assert "inventario" in df.columns
# Todos los tamaños iguales
lengths = [df[col].shape[0] for col in df.columns]
assert len(set(lengths)) == 1, f"Inconsistent lengths: {dict(zip(df.columns, lengths))}"
print("Sanity check passed")
