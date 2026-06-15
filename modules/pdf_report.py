# modules/pdf_report.py

import io
import os

from reportlab.platypus import (
SimpleDocTemplate,
Paragraph,
Spacer,
Table,
TableStyle,
Image as RLImage,
PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER

def generar_pdf_bytes(df, kpis):

```
buffer = io.BytesIO()

doc = SimpleDocTemplate(
    buffer,
    pagesize=A4,
    rightMargin=30,
    leftMargin=30,
    topMargin=30,
    bottomMargin=30
)

styles = getSampleStyleSheet()

titulo_style = ParagraphStyle(
    "TituloESMAX",
    parent=styles["Title"],
    alignment=TA_CENTER,
    textColor=colors.HexColor("#003366")
)

subtitulo_style = ParagraphStyle(
    "Subtitulo",
    parent=styles["Heading2"],
    alignment=TA_CENTER,
    textColor=colors.HexColor("#005A9C")
)

caja_style = ParagraphStyle(
    "Caja",
    parent=styles["BodyText"],
    leading=18
)

content = []

# ==========================================================
# PORTADA
# ==========================================================

if os.path.exists("LAYOUT.png"):
    try:
        banner = RLImage(
            "LAYOUT.png",
            width=520,
            height=120
        )
        content.append(banner)
        content.append(Spacer(1, 10))
    except Exception:
        pass

logos = []

if os.path.exists("logo_esmax.png"):
    try:
        logos.append(
            RLImage(
                "logo_esmax.png",
                width=120,
                height=40
            )
        )
    except Exception:
        pass

if os.path.exists("python_logo.png"):
    try:
        logos.append(
            RLImage(
                "python_logo.png",
                width=60,
                height=60
            )
        )
    except Exception:
        pass

if logos:
    tabla_logos = Table([logos])
    content.append(tabla_logos)

content.append(Spacer(1, 20))

content.append(
    Paragraph(
        "ESMAX CONTROL TOWER",
        titulo_style
    )
)

content.append(
    Paragraph(
        "Sistema Inteligente de Gestión y Optimización de Inventarios",
        subtitulo_style
    )
)

content.append(Spacer(1, 15))

content.append(
    Paragraph(
        """
        <b>Elaborado por:</b><br/>
        Ignacio Álvarez<br/>
        Benjamín Tello<br/>
        Renato Soto
        """,
        styles["Normal"]
    )
)

content.append(Spacer(1, 20))

# ==========================================================
# RESUMEN EJECUTIVO
# ==========================================================

resumen = Table([[
    Paragraph(
        """
        <b>Resumen Ejecutivo</b><br/><br/>
        ESMAX Control Tower es una plataforma desarrollada en Python
        que permite monitorear indicadores operacionales,
        analizar inventarios, proyectar demanda futura y generar
        recomendaciones de abastecimiento para apoyar la toma
        de decisiones basada en datos.
        """,
        caja_style
    )
]])

resumen.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F4FD")),
    ("BOX", (0, 0), (-1, -1), 2, colors.HexColor("#005A9C")),
    ("PADDING", (0, 0), (-1, -1), 12)
]))

content.append(resumen)

content.append(Spacer(1, 20))

# ==========================================================
# KPIs
# ==========================================================

fill_rate = kpis.get("fill_rate", 0)
mae = kpis.get("mae", 0)
inventario = kpis.get("inventario_prom", 0)

kpi_table = Table(
    [[
        f"FILL RATE\n{fill_rate:.2%}",
        f"MAE\n{mae:.2f}",
        f"INVENTARIO\n{inventario:.0f}"
    ]],
    colWidths=[160, 160, 160]
)

kpi_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#28A745")),
    ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#FD7E14")),
    ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#007BFF")),
    ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("BOX", (0, 0), (-1, -1), 1, colors.black)
]))

content.append(kpi_table)

content.append(Spacer(1, 15))

content.append(
    Paragraph(
        """
        <b>Fill Rate:</b> porcentaje de la demanda satisfecha.<br/>
        <b>MAE:</b> error promedio entre demanda real y forecast.<br/>
        <b>Inventario Promedio:</b> stock promedio disponible.
        """,
        styles["Normal"]
    )
)

content.append(Spacer(1, 15))

# ==========================================================
# FLUJO DEL SISTEMA
# ==========================================================

flujo = Table([[
    "DATOS",
    "→",
    "KPIs",
    "→",
    "FORECAST",
    "→",
    "OPTIMIZACIÓN",
    "→",
    "REPORTE"
]])

flujo.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#D9EDF7")),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
    ("GRID", (0, 0), (-1, -1), 1, colors.grey)
]))

content.append(
    Paragraph(
        "<b>Arquitectura del Sistema</b>",
        styles["Heading2"]
    )
)

content.append(flujo)

content.append(Spacer(1, 20))

# ==========================================================
# EXPLICACIÓN DE DATOS
# ==========================================================

campos = [
    ["Campo", "Descripción"],
    ["fecha", "Fecha del registro"],
    ["sku", "Identificador del producto"],
    ["demanda", "Demanda estimada"],
    ["ventas", "Ventas reales"],
    ["inventario", "Stock disponible"],
    ["lead_time", "Tiempo de reposición"],
    ["costo_unitario", "Costo por unidad"]
]

tabla_campos = Table(campos, colWidths=[120, 320])

tabla_campos.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")
]))

content.append(
    Paragraph(
        "<b>Descripción del Dataset</b>",
        styles["Heading2"]
    )
)

content.append(tabla_campos)

content.append(Spacer(1, 20))

# ==========================================================
# FÓRMULAS
# ==========================================================

content.append(
    Paragraph(
        "<b>Fórmulas Utilizadas</b>",
        styles["Heading2"]
    )
)

content.append(
    Paragraph(
        """
        Fill Rate = Ventas / Demanda<br/><br/>
        ROP = Demanda Promedio × Lead Time + Stock de Seguridad<br/><br/>
        EOQ = √((2 × D × S) / H)
        """,
        styles["Normal"]
    )
)

content.append(Spacer(1, 20))

# ==========================================================
# IMPACTO ECONÓMICO
# ==========================================================

ahorro_estimado = inventario * 0.12

ahorro_box = Table([[
    Paragraph(
        f"""
        <b>Impacto Económico Estimado</b><br/><br/>
        Basado en la optimización de inventario,
        el sistema puede generar una reducción potencial
        cercana al 12% de los costos asociados al exceso
        de stock.<br/><br/>

        Ahorro estimado: <b>${ahorro_estimado:,.0f}</b>
        """,
        styles["Normal"]
    )
]])

ahorro_box.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EAF7EA")),
    ("BOX", (0, 0), (-1, -1), 2, colors.green),
    ("PADDING", (0, 0), (-1, -1), 12)
]))

content.append(ahorro_box)

content.append(Spacer(1, 20))

# ==========================================================
# TECNOLOGÍAS
# ==========================================================

content.append(
    Paragraph(
        "<b>Tecnologías Utilizadas</b>",
        styles["Heading2"]
    )
)

content.append(
    Paragraph(
        """
        • Python<br/>
        • Streamlit<br/>
        • Pandas<br/>
        • NumPy<br/>
        • Scikit-Learn<br/>
        • ReportLab
        """,
        styles["Normal"]
    )
)

content.append(PageBreak())

# ==========================================================
# TABLA DE DATOS
# ==========================================================

content.append(
    Paragraph(
        "Muestra de Datos",
        styles["Heading1"]
    )
)

try:

    head = list(df.columns)

    rows = [head]

    for _, r in df.head(20).iterrows():
        rows.append(
            [str(r.get(c, "")) for c in head]
        )

    table = Table(rows)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.whitesmoke, colors.HexColor("#F5F9FF")])
    ]))

    content.append(table)

except Exception:
    content.append(
        Paragraph(
            "No se pudo generar la tabla.",
            styles["Normal"]
        )
    )

content.append(Spacer(1, 20))

# ==========================================================
# CONCLUSIONES
# ==========================================================

content.append(
    Paragraph(
        "<b>Conclusiones</b>",
        styles["Heading1"]
    )
)

content.append(
    Paragraph(
        """
        • Centralización de la información operativa.<br/>
        • Mayor visibilidad del inventario.<br/>
        • Apoyo a la toma de decisiones basada en datos.<br/>
        • Proyección de demanda para anticipar quiebres de stock.<br/>
        • Recomendaciones automáticas de abastecimiento.<br/>
        • Generación automática de reportes ejecutivos.
        """,
        styles["Normal"]
    )
)

content.append(Spacer(1, 20))

content.append(
    Paragraph(
        """
        <hr/>
        ESMAX Control Tower © 2026<br/>
        Proyecto desarrollado por Ignacio Álvarez,
        Benjamín Tello y Renato Soto.
        """,
        styles["Normal"]
    )
)

doc.build(content)

buffer.seek(0)

return buffer.read()
