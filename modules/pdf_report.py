import io
import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER


def generar_pdf_bytes(df, kpis):

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

    title = ParagraphStyle(
        "title",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0B2E4A")
    )

    subtitle = ParagraphStyle(
        "subtitle",
        parent=styles["Heading2"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1F6AA5")
    )

    body = styles["Normal"]

    content = []

    # =========================
    # PORTADA
    # =========================
    if os.path.exists("LAYOUT.png"):
        try:
            content.append(RLImage("LAYOUT.png", width=520, height=120))
            content.append(Spacer(1, 10))
        except:
            pass

    logos = []

    if os.path.exists("logo_esmax.png"):
        try:
            logos.append(RLImage("logo_esmax.png", width=120, height=40))
        except:
            pass

    if os.path.exists("python_logo.png"):
        try:
            logos.append(RLImage("python_logo.png", width=55, height=55))
        except:
            pass

    if logos:
        content.append(Table([logos]))
        content.append(Spacer(1, 15))

    content.append(Paragraph("ESMAX CONTROL TOWER", title))
    content.append(Paragraph("Informe Ejecutivo de Supply Chain & Inventario", subtitle))
    content.append(Spacer(1, 10))

    content.append(Paragraph("""
    <b>Elaborado por:</b><br/>
    Ignacio Álvarez<br/>
    Benjamín Tello<br/>
    Renato Soto
    """, body))

    content.append(Spacer(1, 15))

    # =========================
    # RESUMEN EJECUTIVO
    # =========================
    content.append(Paragraph("<b>1. Resumen Ejecutivo</b>", title))

    content.append(Paragraph("""
    Este sistema permite optimizar la gestión de inventario mediante analítica predictiva,
    control de demanda y modelos de reposición automatizados.

    Su objetivo es mejorar el nivel de servicio, reducir quiebres de stock
    y disminuir capital inmovilizado en inventario.
    """, body))

    content.append(Spacer(1, 12))

    # =========================
    # KPIs
    # =========================
    fill_rate = kpis.get("fill_rate", 0)
    mae = kpis.get("mae", 0)
    inv = kpis.get("inventario_prom", 0)

    content.append(Paragraph("<b>2. Indicadores Clave (KPIs)</b>", title))

    kpi_table = Table([[
        f"Nivel de Servicio\n{fill_rate:.2%}",
        f"Error Pronóstico\n{mae:.2f}",
        f"Inventario Promedio\n{inv:.0f}"
    ]], colWidths=[160, 160, 160])

    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#1F8A70")),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#F39C12")),
        ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#2E86C1")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
    ]))

    content.append(kpi_table)

    content.append(Spacer(1, 10))

    content.append(Paragraph("""
    <b>Interpretación Gerencial:</b><br/>
    • Nivel de servicio indica capacidad de respuesta a demanda.<br/>
    • MAE refleja precisión del modelo de planificación.<br/>
    • Inventario promedio representa capital inmovilizado.
    """, body))

    content.append(Spacer(1, 12))

    # =========================
    # COSTOS (MEJORADO)
    # =========================
    costo_inventario = inv * 0.15
    ahorro_estimado = costo_inventario * 0.12

    content.append(Paragraph("<b>3. Impacto Económico y Costos</b>", title))

    content.append(Paragraph(f"""
    El modelo de optimización impacta directamente en costos logísticos:

    • Costo de mantener inventario: 10% - 20% anual<br/>
    • Reducción de sobrestock estimada: 10% - 15%<br/>
    • Mejora en rotación de inventario

    <b>Estimación financiera:</b><br/>
    • Costo anual de inventario: ${costo_inventario:,.0f}<br/>
    • Ahorro potencial: ${ahorro_estimado:,.0f}
    """, body))

    content.append(Spacer(1, 12))

    # =========================
    # DECISIONES
    # =========================
    content.append(Paragraph("<b>4. Decisiones Operacionales</b>", title))

    content.append(Paragraph("""
    El sistema permite tomar decisiones automáticas:

    • Cuándo reordenar inventario (ROP)<br/>
    • Cuánto pedir (EOQ)<br/>
    • Nivel de stock de seguridad<br/>

    Esto transforma la gestión desde reactiva a predictiva.
    """, body))

    content.append(Spacer(1, 12))

    # =========================
    # FLUJO
    # =========================
    flow = Table([[
        "Datos", "→", "Procesamiento", "→", "Forecast", "→", "Optimización", "→", "Reporte"
    ]])

    flow.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F4FD")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
    ]))

    content.append(flow)

    content.append(Spacer(1, 12))

    # =========================
    # CONCLUSIÓN
    # =========================
    content.append(Paragraph("<b>5. Conclusión</b>", title))

    content.append(Paragraph("""
    ESMAX Control Tower permite transformar la gestión de inventario en un proceso
    basado en datos, reduciendo incertidumbre y mejorando eficiencia operativa.

    Representa una herramienta escalable para la digitalización logística.
    """, body))

    doc.build(content)
    buffer.seek(0)

    return buffer.read()
