import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import io
import traceback
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
# ESTILO EJECUTIVO
# =========================
st.markdown(
    """
    <style>
    .kpi {
        background: linear-gradient(90deg,#0b5f8a,#0b9bd3);
        color:white;
        padding:15px;
        border-radius:12px;
        text-align:center;
        font-weight:bold;
    }

    .card {
        background:white;
        padding:15px;
        border-radius:12px;
        box-shadow:0px 1px 6px rgba(0,0,0,0.08);
    }

    .title {
        font-size:24px;
        font-weight:700;
        color:#0b5f8a;
    }

    .subtitle {
        font-size:13px;
        color:#6c757d;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# IMPORTS SEGUROS
# =========================
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


# =========================
# HEADER (LAYOUT GRANDE ARRIBA)
# =========================
if os.path.exists("LAYOUT.png"):
    st.image(Image.open("LAYOUT.png"), use_container_width=True)

st.markdown("## 📊 ESMAX CONTROL TOWER")
st.markdown("Sistema de optimización de inventario, forecast y analítica operacional")
st.markdown("---")


# =========================
# SIDEBAR (NO SE ELIMINA NADA)
# =========================
st.sidebar.header("⚙️ Control Panel")

uploaded = st.sidebar.file_uploader("Subir CSV / Excel", type=["csv", "xlsx"])
use_sample = st.sidebar.checkbox("Usar datos simulados", True)
dias = st.sidebar.slider("Horizonte de simulación", 30, 365, 180, 30)

st.sidebar.markdown("### Visualización")
show_kpis = st.sidebar.checkbox("KPIs", True)
show_charts = st.sidebar.checkbox("Gráficos", True)
show_abc = st.sidebar.checkbox("ABC", True)
show_opt = st.sidebar.checkbox("Optimización", True)


# =========================
# DATA
# =========================
df = None

if uploaded:
    df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
else:
    if generar_dataset_esmax:
        df = generar_dataset_esmax(dias)

if df is None:
    st.error("No hay datos disponibles")
    st.stop()


# =========================
# KPIs
# =========================
if calcular_kpis:
    kpis = calcular_kpis(df)
else:
    kpis = {
        "fill_rate": (df["ventas"]/df["demanda"]).mean() if "ventas" in df else 0,
        "mae": (df["demanda"] - df.get("ventas",0)).abs().mean(),
        "inventario_prom": df["inventario"].mean()
    }


# =========================
# TABS
# =========================
tabs = st.tabs(["Dashboard","Forecast","Inventario","Optimización","Reporte"])


# =========================
# DASHBOARD
# =========================
with tabs[0]:
    st.markdown("### 📊 Dashboard Ejecutivo")

    c1,c2,c3 = st.columns(3)

    if show_kpis:
        c1.markdown(f"<div class='kpi'>Fill Rate<br>{kpis['fill_rate']:.2%}</div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='card'><b>MAE</b><br>{kpis['mae']:.1f}</div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='card'><b>Inventario Prom</b><br>{kpis['inventario_prom']:.0f}</div>", unsafe_allow_html=True)

    st.markdown("#### 📦 Vista de datos")
    st.dataframe(df.head(15), use_container_width=True)

    if show_charts and "fecha" in df.columns:
        st.markdown("#### 📈 Tendencias")
        st.line_chart(df.set_index("fecha")[["demanda","ventas","inventario"]])


# =========================
# FORECAST
# =========================
with tabs[1]:
    st.markdown("### 🔮 Forecast de Demanda")

    if generar_forecast:
        df_fc = generar_forecast(df)
        if isinstance(df_fc, tuple):
            df_fc = df_fc[0]
    else:
        df_fc = df.copy()
        df_fc["forecast"] = df_fc["demanda"].rolling(7).mean()

    st.line_chart(df_fc.set_index("fecha")[["demanda","forecast"]])

    st.info("Forecast basado en histórico de demanda para estimación de comportamiento futuro.")


# =========================
# INVENTARIO
# =========================
with tabs[2]:
    st.markdown("### 📦 Inventario")

    if "inventario" in df.columns:
        st.bar_chart(df.set_index("fecha")["inventario"])

    if show_abc:
        st.markdown("### 🧠 Clasificación ABC")

        if clasificacion_abc:
            abc = clasificacion_abc(df)
        else:
            abc = df.groupby("sku")["demanda"].sum().reset_index()

        st.dataframe(abc, use_container_width=True)


# =========================
# OPTIMIZACIÓN (MEJORADA)
# =========================
with tabs[3]:
    st.markdown("### ⚙️ Optimización de Inventario")

    optim = optimizar_inventario(df) if optimizar_inventario else {}

    c1,c2,c3 = st.columns(3)

    c1.metric("Demanda prom", f"{optim.get('demanda_prom',0):.1f}")
    c2.metric("Lead time", f"{optim.get('lead_time_prom',0):.1f}")
    c3.metric("Inventario prom", f"{optim.get('inventario_prom',0):.0f}")

    st.markdown("---")

    st.markdown("### 🧠 Recomendación Operacional")

    sugerido = optim.get("suggested_order",0)

    if sugerido > 0:
        st.error(f"🔴 Se recomienda ordenar: {sugerido} unidades")
        st.markdown("Existe riesgo de quiebre de stock si no se repone.")
    else:
        st.success("🟢 No se requiere compra")
        st.markdown("El inventario actual cubre la demanda proyectada.")

    st.markdown("---")

    st.markdown("### 📊 Parámetros logísticos")

    col1,col2,col3 = st.columns(3)

    col1.write(f"Stock seguridad: {optim.get('stock_seguridad',0):.1f}")
    col2.write(f"Reorder Point: {optim.get('reorder_point',0):.1f}")
    col3.write(f"EOQ: {optim.get('eoq',0):.1f}")


# =========================
# REPORTE
# =========================
with tabs[4]:
    st.markdown("### 📄 Reporte Ejecutivo")

    if generar_pdf_bytes:
        pdf = generar_pdf_bytes(df,kpis)
        st.download_button("Descargar PDF Ejecutivo", pdf, "ESMAX_Report.pdf")


# =========================
# LAYOUT FINAL (GRAN BLOQUE CORPORATIVO)
# =========================
st.markdown("---")

col1,col2 = st.columns([3,1])

with col1:
    st.markdown("### ESMAX Control Tower")
    st.markdown("""
    Plataforma de analítica avanzada para optimización de inventario,
    forecast de demanda y toma de decisiones operacionales.
    """)

with col2:
    if os.path.exists("LAYOUT.png"):
        st.image(Image.open("LAYOUT.png"), use_container_width=True)
