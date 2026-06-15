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

    print(">>> PDF REPORT ACTIVO (VERSION NUEVA 2026) <<<")

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

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#003366")
    )

    subtitle_style = ParagraphStyle(
        "SubtitleCustom",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#005A9C")
    )

    normal = styles["Normal"]

    content = []

    # =====================================================
    # MARCA DE VERSION (VISIBLE EN PDF)
    # =====================================================
    content.append(
        Paragraph(
            "<b>VERSION ACTIVA: PDF REPORT NUEVO - ESMAX 2026</b>",
            title_style
        )
    )
    content.append(Spacer(1, 10))

    # =====================================================
    # LAYOUT BANNER
    # =====================================================
    if os.path.exists("LAYOUT.png"):
        try:
            content.append(
                RLImage("LAYOUT.png", width=520, height=120)
            )
            content.append(Spacer(1, 10))
        except:
            pass

    # =====================================================
    # LOGOS
    # =====================================================
    logo_row = []

    if os.path.exists("logo_esmax.png"):
        try:
            logo_row.append(
                RLImage("logo_esmax.png", width=120, height=40)
            )
        except:
            pass

    if os.path.exists("python_logo.png"):
        try:
            logo_row.append(
                RLImage("python_logo.png", width=60, height=60)
            )
        except:
            pass

    if logo_row:
        content.append(Table([logo_row]))
        content.append(Spacer(1, 15))

    # =====================================================
    # TITULO
    # =====================================================
    content.append(Paragraph("ESMAX CONTROL TOWER", title_style))
    content.append(Paragraph("Sistema Inteligente de Inventario y Forecast", subtitle_style))
    content.append(Spacer(1, 15))

    # =====================================================
    # AUTORES
    # =====================================================
    content.append(
        Paragraph(
            """
            <b>Elaborado por:</b><br/>
            Ignacio Álvarez<br/>
            Benjamín Tello<br/>
            Renato Soto
            """,
            normal
        )
    )

    content.append(Spacer(1, 15))

    # =====================================================
    # KPIs
    # =====================================================
    fill_rate = kpis.get("fill_rate", 0)
    mae = kpis.get("mae", 0)
    inv = kpis.get("inventario_prom", 0)

    kpi_table = Table([[
        f"FILL RATE\n{fill_rate:.2%}",
        f"MAE\n{mae:.2f}",
        f"INVENTARIO\n{inv:.0f}"
    ]], colWidths=[160, 160, 160])

    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.green),
        ("BACKGROUND", (1, 0), (1, 0), colors.orange),
        ("BACKGROUND", (2, 0), (2, 0), colors.blue),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    content.append(kpi_table)
    content.append(Spacer(1, 15))

    # =====================================================
    # RESUMEN
    # =====================================================
    content.append(
        Paragraph(
            """
            <b>Resumen Ejecutivo</b><br/><br/>
            Plataforma desarrollada en Python para análisis de inventario,
            forecast de demanda y optimización de reposición mediante KPIs
            y modelos analíticos.
            """,
            normal
        )
    )

    content.append(Spacer(1, 15))

    # =====================================================
    # FLUJO
    # =====================================================
    content.append(
        Paragraph("<b>Flujo del Sistema</b>", title_style)
    )

    flujo = Table([[
        "DATOS", "→", "KPIs", "→", "FORECAST", "→", "OPTIMIZACIÓN", "→", "REPORTE"
    ]])

    flujo.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F4FD")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
    ]))

    content.append(flujo)
    content.append(Spacer(1, 15))

    # =====================================================
    # DATOS
    # =====================================================
    content.append(Paragraph("<b>Descripción de Datos</b>", title_style))

    cols = [
        ["Campo", "Descripción"],
        ["fecha", "Fecha del registro"],
        ["sku", "Producto"],
        ["demanda", "Demanda estimada"],
        ["ventas", "Ventas reales"],
        ["inventario", "Stock disponible"],
        ["lead_time", "Tiempo reposición"],
        ["costo_unitario", "Costo unidad"]
    ]

    table = Table(cols, colWidths=[120, 350])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    content.append(table)
    content.append(Spacer(1, 15))

    # =====================================================
    # IMPACTO ECONOMICO
    # =====================================================
    ahorro = inv * 0.12

    content.append(
        Paragraph(
            f"""
            <b>Impacto Económico Estimado</b><br/><br/>
            Optimización estimada del 12% en costos de inventario.<br/>
            Ahorro aproximado: <b>${ahorro:,.0f}</b>
            """,
            normal
        )
    )

    content.append(Spacer(1, 15))

    # =====================================================
    # TECNOLOGIAS
    # =====================================================
    content.append(
        Paragraph(
            """
            <b>Tecnologías</b><br/>
            Python, Streamlit, Pandas, NumPy, Scikit-Learn, ReportLab
            """,
            normal
        )
    )

    content.append(PageBreak())

    # =====================================================
    # TABLA DATASET
    # =====================================================
    content.append(Paragraph("<b>Muestra de Datos</b>", title_style))

    try:
        head = list(df.columns)
        rows = [head]

        for _, r in df.head(20).iterrows():
            rows.append([str(r.get(c, "")) for c in head])

        t = Table(rows)

        t.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]))

        content.append(t)

    except:
        content.append(Paragraph("Error al generar tabla", normal))

    content.append(Spacer(1, 20))

    # =====================================================
    # CONCLUSIONES
    # =====================================================
    content.append(
        Paragraph("<b>Conclusiones</b>", title_style)
    )

    content.append(
        Paragraph(
            """
            • Centralización de datos.<br/>
            • Mejora en toma de decisiones.<br/>
            • Reducción de quiebres de stock.<br/>
            • Optimización de inventario mediante análisis.<br/>
            • Reportes automáticos ejecutivos.
            """,
            normal
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "<hr/>ESMAX Control Tower © 2026 - Proyecto académico",
            normal
        )
    )

    doc.build(content)
    buffer.seek(0)
    return buffer.read()
