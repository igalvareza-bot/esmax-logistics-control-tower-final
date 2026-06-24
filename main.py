import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import os

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="ESMAX Control Tower",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# ESTILO
# =========================
st.markdown("""
<style>
.kpi {
    background: linear-gradient(90deg,#0b5f8a,#0b9bd3);
    color:white;
    padding:14px;
    border-radius:12px;
    text-align:center;
    font-weight:bold;
}

.card {
    background:white;
    padding:12px;
    border-radius:12px;
    box-shadow:0px 1px 6px rgba(0,0,0,0.08);
}

.title {
    font-size:28px;
    font-weight:800;
    color:#0b5f8a;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# =========================
# IMPORT MÓDULOS
# =========================
from modules.data_generator import generar_dataset_esmax
from modules.inventory import calcular_kpis, clasificacion_abc
from modules.forecast import generar_forecast
from modules.inventory_optimizer import optimizar_inventario
from modules.pdf_report import generar_pdf_bytes

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Panel de Control")

uploaded = st.sidebar.file_uploader("Subir datos", type=["csv","xlsx"])
dias = st.sidebar.slider("Horizonte", 30, 365, 180)

show_opt = st.sidebar.checkbox("Optimización", True)

# =========================
# DATA (SIEMPRE RELOAD)
# =========================
if uploaded:
    df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
else:
    df = generar_dataset_esmax(dias)

# 🔴 IMPORTANTE: evita cache viejo
df = df.copy()

# =========================
# KPIs
# =========================
kpis = calcular_kpis(df) if calcular_kpis else {
    "fill_rate": (df["ventas"]/df["demanda"]).mean(),
    "mae": (df["demanda"] - df["ventas"]).abs().mean(),
    "inventario_prom": df["inventario"].mean()
}

# =========================
# OPTIMIZACIÓN (FUENTE ÚNICA)
# =========================
optim = optimizar_inventario(df)

# 🔴 DEBUG (desactivar después)
st.caption("DEBUG OPTIMIZER:")
st.write(optim)

riesgo = optim.get("riesgo_operativo", "BAJO")

# =========================
# HEADER
# =========================
st.markdown('<div class="title">ESMAX CONTROL TOWER</div>', unsafe_allow_html=True)
st.markdown("---")

# =========================
# TABS
# =========================
tabs = st.tabs([
    "Dashboard",
    "Forecast",
    "Inventario",
    "Optimización",
    "Reporte"
])

# =========================
# DASHBOARD
# =========================
with tabs[0]:
    st.markdown("### Indicadores")

    c1,c2,c3 = st.columns(3)

    c1.markdown(f"<div class='kpi'>Fill Rate<br>{kpis['fill_rate']:.2%}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'><b>MAE</b><br>{kpis['mae']:.1f}</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'><b>Inventario</b><br>{kpis['inventario_prom']:.0f}</div>", unsafe_allow_html=True)

    st.dataframe(df.head(20))

# =========================
# FORECAST
# =========================
with tabs[1]:
    df_fc = generar_forecast(df) if generar_forecast else df.copy()

    if isinstance(df_fc, tuple):
        df_fc = df_fc[0]

    df_fc["forecast"] = df_fc.get("forecast", df_fc["demanda"].rolling(7).mean())

    st.line_chart(df_fc.set_index("fecha")[["demanda","forecast"]])

# =========================
# INVENTARIO
# =========================
with tabs[2]:
    st.bar_chart(df.set_index("fecha")["inventario"])

    st.dataframe(
        clasificacion_abc(df) if clasificacion_abc else df.groupby("sku")["demanda"].sum()
    )

# =========================
# OPTIMIZACIÓN (SOLO RESULTADOS)
# =========================
with tabs[3]:
    st.markdown("### Decisión de reposición")

    st.markdown(f"""
- Riesgo operativo: **{riesgo}**
- Pedido sugerido: **{optim.get('suggested_order',0):.0f}**
- Punto de reorden: **{optim.get('reorder_point',0):.1f}**
- Stock de seguridad: **{optim.get('stock_seguridad',0):.1f}**
- EOQ: **{optim.get('eoq',0):.1f}**
""")

    if riesgo == "ALTO":
        st.error("Acción inmediata requerida")
    elif riesgo == "MEDIO":
        st.warning("Monitorear niveles")
    else:
        st.success("Sistema estable")

# =========================
# REPORTE
# =========================
with tabs[4]:
    pdf = generar_pdf_bytes(df, kpis)
    st.download_button("Descargar PDF", pdf, "ESMAX_Report.pdf")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("## ESMAX CONTROL TOWER")

st.markdown("""
Plataforma de analítica avanzada para optimización de inventario y soporte a decisiones.
""")

if os.path.exists("LAYOUT.png"):
    st.image(Image.open("LAYOUT.png"), use_container_width=True)
