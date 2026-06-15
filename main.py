# main.py
import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import io
import traceback
import os

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(
    page_title="ESMAX Control Tower",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# ESTILOS EJECUTIVOS
# ----------------------------
st.markdown(
    """
    <style>
    .kpi-card {
        background: linear-gradient(90deg,#0b5f8a,#0b9bd3);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
    .metric-box {
        background: white;
        padding: 12px;
        border-radius: 10px;
        box-shadow: 0 1px 5px rgba(0,0,0,0.1);
    }
    .title {
        color:#0b5f8a;
        font-size:22px;
        font-weight:700;
    }
    .sub {
        color:#6c757d;
        font-size:13px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# IMPORTS SEGUROS
# ----------------------------
try:
    from modules.data_generator import generar_dataset_esmax
except:
    generar_dataset_esmax = None

try:
    from modules.inventory import calcular_kpis, clasificacion_abc
except:
    calcular_kpis = None
    clasificacion_abc = None

try:
    from modules.forecast import generar_forecast
except:
    generar_forecast = None

try:
    from modules.inventory_optimizer import optimizar_inventario
except:
    optimizar_inventario = None

try:
    from modules.pdf_report import generar_pdf_bytes
except:
    generar_pdf_bytes = None

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.header("Control Operacional")

uploaded = st.sidebar.file_uploader("Subir CSV", type=["csv","xlsx"])
use_sample = st.sidebar.checkbox("Usar dataset simulado", True)
dias = st.sidebar.slider("Horizonte de simulación", 30, 365, 180, 30)

# ----------------------------
# DATA
# ----------------------------
df = None

if uploaded:
    df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
else:
    if generar_dataset_esmax:
        df = generar_dataset_esmax(dias)

if df is None:
    st.error("No hay datos disponibles")
    st.stop()

# ----------------------------
# KPIs
# ----------------------------
if calcular_kpis:
    kpis = calcular_kpis(df)
else:
    kpis = {
        "fill_rate": (df["ventas"]/df["demanda"]).mean() if "ventas" in df else 0,
        "mae": (df["demanda"] - df.get("ventas",0)).abs().mean(),
        "inventario_prom": df["inventario"].mean()
    }

# ----------------------------
# TABS
# ----------------------------
tabs = st.tabs(["Dashboard","Forecast","Inventario","Optimización","Reporte"])

# =========================
# DASHBOARD
# =========================
with tabs[0]:
    st.markdown("## 📊 Dashboard Ejecutivo")

    c1,c2,c3 = st.columns(3)

    c1.markdown(f"<div class='kpi-card'>Fill Rate<br>{kpis['fill_rate']:.2%}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-box'><b>MAE</b><br>{kpis['mae']:.1f}</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-box'><b>Inventario Prom</b><br>{kpis['inventario_prom']:.0f}</div>", unsafe_allow_html=True)

    st.dataframe(df.head(10), use_container_width=True)

# =========================
# FORECAST
# =========================
with tabs[1]:
    st.markdown("## 🔮 Forecast de Demanda")

    if generar_forecast:
        df_fc = generar_forecast(df)
        if isinstance(df_fc, tuple):
            df_fc = df_fc[0]
    else:
        df_fc = df.copy()
        df_fc["forecast"] = df_fc["demanda"].rolling(7).mean()

    st.line_chart(df_fc.set_index("fecha")[["demanda","forecast"]])

    st.info("El forecast estima la demanda futura usando comportamiento histórico.")

# =========================
# INVENTARIO
# =========================
with tabs[2]:
    st.markdown("## 📦 Control de Inventario")

    st.bar_chart(df.set_index("fecha")["inventario"])

    if clasificacion_abc:
        abc = clasificacion_abc(df)
    else:
        abc = df.groupby("sku")["demanda"].sum().reset_index()

    st.dataframe(abc)

# =========================
# OPTIMIZACIÓN (EJECUTIVA)
# =========================
with tabs[3]:
    st.markdown("## ⚙️ Optimización de Inventario")

    optim = optimizar_inventario(df) if optimizar_inventario else {}

    # KPIs
    col1,col2,col3 = st.columns(3)

    col1.metric("Demanda prom", f"{optim.get('demanda_prom',0):.1f}")
    col2.metric("Lead time", f"{optim.get('lead_time_prom',0):.1f}")
    col3.metric("Inventario", f"{optim.get('inventario_prom',0):.0f}")

    st.divider()

    # decisiones
    st.markdown("### 🧠 Decisión Operacional")

    if optim.get("suggested_order",0) > 0:
        st.error(f"🔴 Orden sugerida: {optim['suggested_order']} unidades")
        st.markdown("Existe riesgo de quiebre de stock.")
    else:
        st.success("🟢 No se requiere compra")
        st.markdown("El inventario actual cubre la demanda proyectada.")

    st.divider()

    st.markdown("### 📊 Parámetros de optimización")
    st.write({
        "Stock seguridad": optim.get("stock_seguridad"),
        "ROP": optim.get("reorder_point"),
        "EOQ": optim.get("eoq")
    })

# =========================
# REPORTE
# =========================
with tabs[4]:
    st.markdown("## 📄 Reporte Ejecutivo")

    if generar_pdf_bytes:
        pdf = generar_pdf_bytes(df,kpis)
        st.download_button("Descargar PDF", pdf, "ESMAX_Report.pdf")

# =========================
# LAYOUT AL FINAL (COMO PEDISTE)
# =========================
st.markdown("---")

col1,col2 = st.columns([3,1])

with col1:
    st.markdown("### ESMAX Control Tower")
    st.markdown("Sistema de optimización de inventario y forecast")

with col2:
    if os.path.exists("LAYOUT.png"):
        st.image(Image.open("LAYOUT.png"), width=250)
