# main.py
"""
ESMAX Control Tower - UI completo y robusto
Reemplaza completamente el main.py actual por este archivo.
Características:
- Sidebar con opciones y filtros
- Cabecera con logo y layout (usa LAYOUT.png y logo_esmax.png si existen)
- KPIs destacados y tarjetas con colores ESMAX
- Pestañas/Secciones: Dashboard, Forecast, Inventario, Optimización, Reporte
- Gráficos interactivos (st.line_chart / st.bar_chart) y tablas
- Generación de PDF enriquecido (incluye logo si existe) usando modules/pdf_report.py
- Manejo de errores robusto para evitar que la app "se rompa" por un módulo faltante
- Compatibilidad con versiones recientes de Streamlit (sin opciones deprecadas)
"""

import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import io
import traceback
import os

# Importar módulos internos con manejo de errores
try:
    from modules.data_generator import generar_dataset_esmax
except Exception:
    generar_dataset_esmax = None

try:
    from modules.inventory import calcular_kpis, clasificacion_abc
except Exception:
    calcular_kpis = None
    clasificacion_abc = None

try:
    from modules.forecast import generar_forecast
except Exception:
    generar_forecast = None

try:
    from modules.inventory_optimizer import optimizar_inventario
except Exception:
    optimizar_inventario = None

try:
    from modules.pdf_report import generar_pdf_bytes
except Exception:
    generar_pdf_bytes = None

# Configuración de la página
st.set_page_config(page_title="ESMAX Control Tower", layout="wide", initial_sidebar_state="expanded")

# Evitar opción deprecada si existe
try:
    st.set_option("deprecation.showfileUploaderEncoding", False)
except Exception:
    pass

# Estilos CSS mínimos para colores ESMAX (ajusta hex según tu branding)
st.markdown(
    """
    <style>
    .esmax-kpi {background: linear-gradient(90deg,#0b5f8a,#0b9bd3); color: white; padding: 12px; border-radius: 8px;}
    .esmax-card {background: #ffffff; padding: 12px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);}
    .esmax-title {color: #0b5f8a; font-weight:700;}
    .small-muted {color: #6c757d; font-size:12px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Cabecera con layout y logo
col_h1, col_h2 = st.columns([4, 1])
with col_h1:
    # Mostrar layout grande si existe
    try:
        if os.path.exists("LAYOUT.png"):
            st.image(Image.open("LAYOUT.png"), width="stretch")
        else:
            st.markdown("## ESMAX CONTROL TOWER", unsafe_allow_html=True)
    except Exception:
        st.markdown("## ESMAX CONTROL TOWER", unsafe_allow_html=True)

with col_h2:
    # Logo pequeño a la derecha si existe
    try:
        if os.path.exists("logo_esmax.png"):
            st.image(Image.open("logo_esmax.png"), width=120)
    except Exception:
        pass

st.markdown("---")

# Sidebar: controles y filtros
st.sidebar.header("Controles")
# Fuente de datos: si el usuario sube un CSV, lo usamos; si no, usamos el generador
uploaded = st.sidebar.file_uploader("Subir CSV (opcional)", type=["csv", "xlsx"])
use_sample = st.sidebar.checkbox("Usar datos simulados (sample)", value=True)
dias = st.sidebar.slider("Días a generar (si usa sample)", min_value=30, max_value=365, value=180, step=30)

# Opciones de visualización
st.sidebar.markdown("### Visualización")
show_kpis = st.sidebar.checkbox("Mostrar KPIs", value=True)
show_charts = st.sidebar.checkbox("Mostrar Gráficas", value=True)
show_abc = st.sidebar.checkbox("Mostrar clasificación ABC", value=True)
show_optim = st.sidebar.checkbox("Mostrar optimización", value=True)

# Cargar datos
df = None
load_error = None
try:
    if uploaded is not None:
        # Intentar leer CSV o Excel
        try:
            df = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
        except Exception:
            # Reintentar con pandas autodetect
            df = pd.read_csv(uploaded, encoding="latin1", errors="ignore")
    else:
        if use_sample and generar_dataset_esmax is not None:
            df = generar_dataset_esmax(dias)
        elif generar_dataset_esmax is None:
            load_error = "Módulo data_generator no disponible. No hay datos para mostrar."
        else:
            df = generar_dataset_esmax(dias)
except Exception as e:
    load_error = f"Error cargando datos: {e}\n{traceback.format_exc()}"

if df is None and load_error:
    st.error(load_error)
    st.stop()

# Normalizar columnas esperadas (intentar convertir nombres comunes)
expected_cols = ["fecha", "sku", "demanda", "ventas", "inventario", "lead_time", "costo_unitario"]
for c in expected_cols:
    if c not in df.columns:
        # intentar variantes en minúsculas
        for col in df.columns:
            if col.lower() == c:
                df.rename(columns={col: c}, inplace=True)
                break

# Asegurar tipos
if "fecha" in df.columns:
    try:
        df["fecha"] = pd.to_datetime(df["fecha"])
    except Exception:
        pass

# Pestañas principales
tabs = st.tabs(["Dashboard", "Forecast", "Inventario", "Optimización", "Reporte"])

# --- Dashboard tab ---
with tabs[0]:
    st.subheader("Resumen")
    if show_kpis:
        try:
            if calcular_kpis is not None:
                kpis = calcular_kpis(df)
            else:
                # fallback simple
                kpis = {
                    "fill_rate": float((df.get("ventas", 0) / df.get("demanda", 1)).mean()) if "ventas" in df.columns and "demanda" in df.columns else 0.0,
                    "mae": float((df["demanda"] - df.get("ventas", 0)).abs().mean()) if "demanda" in df.columns else 0.0,
                    "inventario_prom": float(df.get("inventario", pd.Series([0])).mean()) if "inventario" in df.columns else 0.0
                }
        except Exception:
            kpis = {"fill_rate": 0.0, "mae": 0.0, "inventario_prom": 0.0}

        # Mostrar KPIs con estilo
        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown(f"<div class='esmax-kpi'><div class='esmax-title'>Fill Rate</div><div style='font-size:20px'>{kpis.get('fill_rate',0):.2%}</div></div>", unsafe_allow_html=True)
        with k2:
            st.markdown(f"<div class='esmax-card'><div class='esmax-title'>MAE</div><div style='font-size:20px'>{kpis.get('mae',0):.1f}</div></div>", unsafe_allow_html=True)
        with k3:
            st.markdown(f"<div class='esmax-card'><div class='esmax-title'>Inventario Prom</div><div style='font-size:20px'>{kpis.get('inventario_prom',0):.0f}</div></div>", unsafe_allow_html=True)

    st.markdown("### Datos (muestra)")
    st.dataframe(df.head(10), use_container_width=True)

    if show_charts:
        st.markdown("### Gráficas rápidas")
        # Demanda y Ventas
        try:
            if "fecha" in df.columns and "demanda" in df.columns:
                chart_df = df.set_index("fecha")[["demanda"]].copy()
                if "ventas" in df.columns:
                    chart_df["ventas"] = df.set_index("fecha")["ventas"]
                st.line_chart(chart_df)
            else:
                st.line_chart(df[["demanda", "ventas"]].fillna(0))
        except Exception:
            st.info("No se pudieron generar las gráficas de demanda/ventas.")

# --- Forecast tab ---
with tabs[1]:
    st.subheader("Forecast")
    if generar_forecast is None:
        st.warning("Módulo de forecast no disponible. Mostraré un forecast simple de fallback.")
        # fallback: media móvil
        try:
            df_fc = df.copy()
            if "demanda" in df_fc.columns:
                df_fc = df_fc.sort_values("fecha").reset_index(drop=True)
                df_fc["forecast"] = df_fc["demanda"].rolling(window=7, min_periods=1).mean().shift(1).fillna(df_fc["demanda"].mean())
            else:
                df_fc["forecast"] = np.nan
        except Exception:
            df_fc = df.copy()
            df_fc["forecast"] = np.nan
    else:
        try:
            df_fc = generar_forecast(df)
            # generar_forecast puede devolver (df, model, error) o solo df
            if isinstance(df_fc, tuple) and len(df_fc) >= 1:
                df_fc = df_fc[0]
        except Exception:
            st.error("Error ejecutando generar_forecast. Usando fallback.")
            df_fc = df.copy()
            df_fc["forecast"] = df_fc.get("demanda", pd.Series([np.nan]*len(df_fc))).rolling(window=7, min_periods=1).mean().shift(1).fillna(df_fc.get("demanda", 0).mean())

    # Mostrar tabla y gráfico
    st.markdown("#### Tabla Forecast (primeras filas)")
    st.dataframe(df_fc.head(10), use_container_width=True)
    st.markdown("#### Demanda vs Forecast")
    try:
        if "fecha" in df_fc.columns:
            st.line_chart(df_fc.set_index("fecha")[["demanda", "forecast"]])
        else:
            st.line_chart(df_fc[["demanda", "forecast"]])
    except Exception:
        st.info("No se pudo graficar demanda vs forecast.")

# --- Inventario tab ---
with tabs[2]:
    st.subheader("Inventario y Clasificación")
    # Mostrar inventario
    try:
        if "fecha" in df.columns and "inventario" in df.columns:
            st.bar_chart(df.set_index("fecha")[["inventario"]])
        elif "inventario" in df.columns:
            st.bar_chart(df[["inventario"]])
        else:
            st.info("No hay columna 'inventario' para graficar.")
    except Exception:
        st.info("Error mostrando inventario.")

    # Clasificación ABC
    if show_abc:
        st.markdown("#### Clasificación ABC por SKU")
        try:
            if clasificacion_abc is not None:
                abc = clasificacion_abc(df)
            else:
                # fallback simple
                resumen = df.groupby("sku")["demanda"].sum().reset_index().sort_values("demanda", ascending=False)
                resumen["acumulado"] = resumen["demanda"].cumsum() / resumen["demanda"].sum()
                def cat(x):
                    if x <= 0.8:
                        return "A"
                    elif x <= 0.95:
                        return "B"
                    else:
                        return "C"
                resumen["ABC"] = resumen["acumulado"].apply(cat)
                abc = resumen
            st.dataframe(abc, use_container_width=True)
        except Exception:
            st.info("No se pudo generar clasificación ABC.")

# --- Optimización tab ---
with tabs[3]:
    st.subheader("Optimización de Inventario")
    try:
        if optimizar_inventario is not None:
            optim = optimizar_inventario(df)
        else:
            # fallback simple
            optim = {
                "demanda_prom": float(df["demanda"].mean()) if "demanda" in df.columns else 0.0,
                "lead_time_prom": float(df["lead_time"].mean()) if "lead_time" in df.columns else 1.0,
                "inventario_prom": float(df["inventario"].mean()) if "inventario" in df.columns else 0.0,
                "reorder_point": 0.0,
                "suggested_order": 0
            }
        st.json(optim)
    except Exception:
        st.error("Error calculando optimización.")
        st.code(traceback.format_exc(), language="python")

# --- Reporte tab ---
with tabs[4]:
    st.subheader("Reporte y Export")
    st.markdown("Genera un PDF con el resumen y KPIs. El PDF intentará incluir el logo si existe en la raíz del proyecto.")

    # Recalcular KPIs antes de exportar
    try:
        if calcular_kpis is not None:
            kpis = calcular_kpis(df)
        else:
            kpis = {
                "fill_rate": float((df.get("ventas", 0) / df.get("demanda", 1)).mean()) if "ventas" in df.columns and "demanda" in df.columns else 0.0,
                "mae": float((df["demanda"] - df.get("ventas", 0)).abs().mean()) if "demanda" in df.columns else 0.0,
                "inventario_prom": float(df.get("inventario", pd.Series([0])).mean()) if "inventario" in df.columns else 0.0
            }
    except Exception:
        kpis = {"fill_rate": 0.0, "mae": 0.0, "inventario_prom": 0.0}

    st.markdown("**KPIs actuales**")
    st.write(kpis)

    # Botón para descargar PDF
    try:
        if generar_pdf_bytes is not None:
            pdf_bytes = generar_pdf_bytes(df, kpis)
            if pdf_bytes:
                st.download_button("Descargar Reporte PDF", data=pdf_bytes, file_name="ESMAX_Control_Tower_Report.pdf", mime="application/pdf")
            else:
                st.warning("El generador de PDF devolvió bytes vacíos. Intentando generar PDF simple localmente.")
                raise Exception("PDF vacío")
        else:
            raise Exception("Módulo pdf_report no disponible")
    except Exception:
        # Generar PDF simple en memoria con reportlab si está instalado, incluyendo logo si existe
        try:
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.lib import colors

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer)
            styles = getSampleStyleSheet()
            content = []
            # Logo
            if os.path.exists("logo_esmax.png"):
                try:
                    rl_logo = RLImage("logo_esmax.png", width=120, height=40)
                    content.append(rl_logo)
                except Exception:
                    pass
            content.append(Paragraph("ESMAX CONTROL TOWER REPORT", styles["Title"]))
            content.append(Spacer(1, 8))
            content.append(Paragraph(f"Fill Rate: {kpis.get('fill_rate',0):.2%}", styles["Normal"]))
            content.append(Paragraph(f"MAE: {kpis.get('mae',0):.1f}", styles["Normal"]))
            content.append(Paragraph(f"Inventario Prom: {kpis.get('inventario_prom',0):.0f}", styles["Normal"]))
            content.append(Spacer(1, 12))

            # Tabla resumen (primeras 20 filas)
            head = list(df.columns)
            rows = [head]
            for _, r in df.head(20).iterrows():
                rows.append([str(r.get(c, "")) for c in head])
            table = Table(rows, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f2f2f2")),
                ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ]))
            content.append(table)
            doc.build(content)
            buffer.seek(0)
            st.download_button("Descargar Reporte PDF (fallback)", data=buffer.read(), file_name="ESMAX_Control_Tower_Report.pdf", mime="application/pdf")
        except Exception:
            st.error("No se pudo generar el PDF. Instala reportlab o revisa modules/pdf_report.py")
            st.code(traceback.format_exc(), language="python")

# Footer
st.markdown("---")
st.caption("Si necesitas que el layout, colores o secciones sean exactamente como el entregable oficial ESMAX, sube los assets (logo_esmax.png, LAYOUT.png) y describe las secciones faltantes. Puedo adaptar el diseño al detalle.")
