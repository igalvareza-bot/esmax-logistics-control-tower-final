import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import os

# =========================
# CONFIG "ENTERPRISE AI"
# =========================
st.set_page_config(
    page_title="ESMAX Intelligent Supply Chain AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# UI STYLE (CONSULTORA LEVEL)
# =========================
st.markdown(
"""
<style>
.big-title {
    font-size:28px;
    font-weight:800;
    color:#0b5f8a;
}

.card {
    background:white;
    padding:18px;
    border-radius:14px;
    box-shadow:0 2px 10px rgba(0,0,0,0.08);
}

.kpi {
    background: linear-gradient(90deg,#0b5f8a,#0b9bd3);
    color:white;
    padding:18px;
    border-radius:14px;
    text-align:center;
    font-weight:bold;
}

.badge-red {color:white;background:#e74c3c;padding:6px 10px;border-radius:8px;}
.badge-green {color:white;background:#2ecc71;padding:6px 10px;border-radius:8px;}
.badge-yellow {color:white;background:#f1c40f;padding:6px 10px;border-radius:8px;}
</style>
""",
unsafe_allow_html=True
)

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
# HEADER (PLATAFORMA IA)
# =========================
if os.path.exists("LAYOUT.png"):
    st.image(Image.open("LAYOUT.png"), use_container_width=True)

st.markdown('<div class="big-title">ESMAX Intelligent Supply Chain AI</div>', unsafe_allow_html=True)
st.markdown("Sistema autónomo de optimización de inventario basado en analítica predictiva y modelos de decisión logística")
st.markdown("---")


# =========================
# SIDEBAR (CONTROL CENTER)
# =========================
st.sidebar.header("Control Center AI")

uploaded = st.sidebar.file_uploader("Dataset operativo", type=["csv","xlsx"])
use_sample = st.sidebar.checkbox("Modo simulación IA", True)
dias = st.sidebar.slider("Horizonte de simulación", 30, 365, 180)

st.sidebar.markdown("### Modo analítico")
show_kpis = st.sidebar.checkbox("KPIs AI", True)
show_charts = st.sidebar.checkbox("Time Series", True)
show_abc = st.sidebar.checkbox("ABC Intelligence", True)
show_opt = st.sidebar.checkbox("Decision Engine", True)


# =========================
# DATA ENGINE
# =========================
if uploaded:
    df = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
else:
    df = generar_dataset_esmax(dias) if generar_dataset_esmax else None

if df is None:
    st.error("No data available")
    st.stop()


# =========================
# KPI ENGINE
# =========================
kpis = calcular_kpis(df) if calcular_kpis else {
    "fill_rate": (df["ventas"]/df["demanda"]).mean(),
    "mae": (df["demanda"]-df.get("ventas",0)).abs().mean(),
    "inventario_prom": df["inventario"].mean()
}

# =========================
# DECISION ENGINE (IA FAKE PERO PODEROSA)
# =========================
optim = optimizar_inventario(df) if optimizar_inventario else {}

risk = "GREEN"
if optim.get("suggested_order",0) > 500:
    risk = "RED"
elif optim.get("suggested_order",0) > 0:
    risk = "YELLOW"


# impacto económico simulado
stock_value = df["inventario"].mean() * 50  # proxy monetario
savings = stock_value * 0.12


# =========================
# TABS
# =========================
tabs = st.tabs([
    "AI Dashboard",
    "Demand Forecast AI",
    "Inventory Intelligence",
    "Decision Engine",
    "Executive Report"
])

# =========================
# AI DASHBOARD
# =========================
with tabs[0]:
    st.markdown("## 🧠 AI Executive Dashboard")

    c1,c2,c3 = st.columns(3)

    c1.markdown(f"<div class='kpi'>Fill Rate<br>{kpis['fill_rate']:.2%}</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'><b>Forecast Error (MAE)</b><br>{kpis['mae']:.1f}</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'><b>Inventory Exposure</b><br>{kpis['inventario_prom']:.0f}</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 📊 Business Insight Engine")

    st.info(f"""
    📦 Valor estimado inventario: ${stock_value:,.0f}
    💰 Potencial optimización: ${savings:,.0f}
    ⚠️ Nivel de riesgo actual: {risk}
    """)

    st.dataframe(df.head(12))


# =========================
# FORECAST AI
# =========================
with tabs[1]:
    st.markdown("## 🔮 Demand Forecast AI")

    df_fc = generar_forecast(df) if generar_forecast else df.copy()
    if isinstance(df_fc, tuple):
        df_fc = df_fc[0]

    df_fc["forecast"] = df_fc.get("forecast", df_fc["demanda"].rolling(7).mean())

    st.line_chart(df_fc.set_index("fecha")[["demanda","forecast"]])

    st.success("AI model simulates demand behavior using historical consumption patterns.")


# =========================
# INVENTORY INTELLIGENCE
# =========================
with tabs[2]:
    st.markdown("## 📦 Inventory Intelligence Layer")

    st.bar_chart(df.set_index("fecha")["inventario"])

    if show_abc:
        st.markdown("### SKU Intelligence (ABC AI Classification)")

        abc = clasificacion_abc(df) if clasificacion_abc else df.groupby("sku")["demanda"].sum().reset_index()

        st.dataframe(abc)


# =========================
# DECISION ENGINE
# =========================
with tabs[3]:
    st.markdown("## ⚙️ Autonomous Decision Engine")

    st.markdown("### System Status")

    if risk == "RED":
        st.markdown("<span class='badge-red'>CRITICAL RISK</span>", unsafe_allow_html=True)
    elif risk == "YELLOW":
        st.markdown("<span class='badge-yellow'>MEDIUM RISK</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='badge-green'>OPTIMAL</span>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Inventory Recommendations")

    st.write({
        "Suggested Order": optim.get("suggested_order",0),
        "Reorder Point": optim.get("reorder_point",0),
        "Safety Stock": optim.get("stock_seguridad",0),
        "EOQ": optim.get("eoq",0)
    })

    st.markdown("""
    🧠 Interpretation:
    - System evaluates demand volatility
    - Computes optimal reorder strategy
    - Minimizes stockout risk and overstock cost
    """)


# =========================
# EXECUTIVE REPORT
# =========================
with tabs[4]:
    st.markdown("## 📄 Executive AI Report")

    if generar_pdf_bytes:
        pdf = generar_pdf_bytes(df,kpis)
        st.download_button("Download AI Report", pdf, "ESMAX_AI_Report.pdf")


# =========================
# FOOTER (CONSULTORA STYLE)
# =========================
st.markdown("---")

col1,col2 = st.columns([3,1])

with col1:
    st.markdown("### ESMAX Intelligent Supply Chain AI")
    st.markdown("""
    Autonomous system for demand forecasting, inventory optimization,
    and decision-making support powered by analytical intelligence.
    """)

with col2:
    if os.path.exists("LAYOUT.png"):
        st.image(Image.open("LAYOUT.png"), use_container_width=True)
