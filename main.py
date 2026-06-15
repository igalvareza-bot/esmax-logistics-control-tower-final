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
# ESTILO LIMPIO EJECUTIVO
# =========================
st.markdown("""
<style>
.card {
    background:white;
    padding:16px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}

.kpi {
    background: linear-gradient(90deg,#0b5f8a,#0b9bd3);
    color:white;
    padding:18px;
    border-radius:12px;
    text-align:center;
    font-weight:bold;
}

.title {
    font-size:26px;
    font-weight:800;
    color:#0b5f8a;
}
</style>
""", unsafe_allow_html=True)


# =========================
# IMPORTS
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
# HEADER (SIN LAYOUT AQUÍ)
# =========================
st.markdown('<div class="title">ESMAX CONTROL TOWER</div>', unsafe_allow_html=True)
st.markdown("Plataforma de optimización de inventario y predicción de demanda")
st.markdown("---")


# =========================
# SIDEBAR
# =========================
st.sidebar.header("Panel de control")

uploaded = st.sidebar.file_uploader("Cargar datos", type=["csv","xlsx"])
use_sample = st.sidebar.checkbox("Usar datos simulados", True)
dias = st.sidebar.slider("Horizonte de análisis", 30, 365, 180)


# =========================
# DATA
# =========================
if uploaded:
    df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
else:
    df = generar_dataset_esmax(dias) if generar_dataset_esmax else None

if df is None:
    st.error("No hay datos disponibles")
    st.stop()


# =========================
# KPIs
# =========================
kpis = calcular_kpis(df) if calcular_kpis else {
    "fill_rate": (df["ventas"]/df["demanda"]).mean(),
    "mae": (df["demanda"] - df.get("ventas",0)).abs().mean(),
    "inventario_prom": df["inventario"].mean()
}


# =========================
# OPTIMIZACIÓN
# =========================
optim = optimizar_inventario(df) if optimizar_inventario else {}

riesgo = "BAJO"
if optim.get("suggested_order",0) > 500:
    riesgo = "ALTO"
elif optim.get("suggested_order",0) > 0:
    riesgo = "MEDIO"


# =========================
# TABS
# =========================
tabs = st.tabs([
    "Resumen",
    "Pronóstico",
    "Inventario",
    "Optimización",
    "Reporte"
])


# =========================
# RESUMEN
# =========================
with tabs[0]:
    st.markdown("### Resumen ejecutivo")

    c1,c2,c3 = st.columns(3)

    c1.markdown(f"<div class='kpi'>Nivel de servicio<br>{kpis['fill_rate']:.2%}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'><b>Error de pronóstico</b><br>{kpis['mae']:.1f}</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'><b>Inventario promedio</b><br>{kpis['inventario_prom']:.0f}</div>", unsafe_allow_html=True)

    st.markdown("### Datos")
    st.dataframe(df.head(15))


# =========================
# PRONÓSTICO
# =========================
with tabs[1]:
    st.markdown("### Pronóstico de demanda")

    df_fc = generar_forecast(df) if generar_forecast else df.copy()

    if isinstance(df_fc, tuple):
        df_fc = df_fc[0]

    df_fc["forecast"] = df_fc.get("forecast", df_fc["demanda"].rolling(7).mean())

    st.line_chart(df_fc.set_index("fecha")[["demanda","forecast"]])


# =========================
# INVENTARIO
# =========================
with tabs[2]:
    st.markdown("### Estado de inventario")

    st.bar_chart(df.set_index("fecha")["inventario"])

    if clasificacion_abc:
        st.markdown("### Clasificación de productos")
        st.dataframe(clasificacion_abc(df))
    else:
        st.dataframe(df.groupby("sku")["demanda"].sum().reset_index())


# =========================
# OPTIMIZACIÓN (SIN JSON)
# =========================
with tabs[3]:
    st.markdown("### Recomendación operativa")

    st.markdown(f"""
    - Nivel de riesgo: **{riesgo}**
    - Pedido sugerido: **{optim.get('suggested_order',0):.0f} unidades**
    - Punto de reorden: **{optim.get('reorder_point',0):.1f}**
    - Stock de seguridad: **{optim.get('stock_seguridad',0):.1f}**
    - EOQ: **{optim.get('eoq',0):.1f}**
    """)

    st.markdown("### Interpretación")

    if riesgo == "ALTO":
        st.error("Se recomienda reposición inmediata para evitar quiebre de stock.")
    elif riesgo == "MEDIO":
        st.warning("Se recomienda monitoreo activo del inventario.")
    else:
        st.success("Inventario en niveles adecuados.")


# =========================
# REPORTE
# =========================
with tabs[4]:
    st.markdown("### Reporte ejecutivo")

    if generar_pdf_bytes:
        pdf = generar_pdf_bytes(df, kpis)
        st.download_button("Descargar reporte PDF", pdf, "ESMAX_Report.pdf")


# =========================
# LAYOUT SOLO AL FINAL (GRANDE)
# =========================
st.markdown("---")

st.markdown("## ESMAX CONTROL TOWER")

col1, col2 = st.columns([3,2])

with col1:
    st.markdown("""
    Sistema de análisis avanzado para optimización de inventario,
    predicción de demanda y soporte a decisiones operacionales.
    """)

with col2:
    if os.path.exists("LAYOUT.png"):
        st.image(Image.open("LAYOUT.png"), use_container_width=True)
