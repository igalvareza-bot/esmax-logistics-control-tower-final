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

    # =====================================================
    # PORTADA EJECUTIVA
    # =====================================================

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
    content.append(Paragraph("Informe Ejecutivo de Gestión de Inventario", subtitle))

    content.append(Spacer(1, 15))

    content.append(Paragraph("""
    <b>Elaborado por:</b><br/>
    Ignacio Álvarez<br/>
    Benjamín Tello<br/>
    Renato Soto
    """, body))

    content.append(Spacer(1, 15))

    # =====================================================
    # INTRO EJECUTIVA
    # =====================================================

    content.append(Paragraph("<b>1. Resumen Ejecutivo</b>", title))

    content.append(Spacer(1, 5))

    content.append(Paragraph("""
    Este sistema permite a la organización ESMAX mejorar la toma de decisiones
    en la gestión de inventarios mediante análisis de datos, proyección de demanda
    y optimización de reposición de stock.

    El objetivo principal es reducir costos operacionales, minimizar quiebres de stock
    y mejorar la eficiencia del capital inmovilizado.
    """, body))

    content.append(Spacer(1, 10))

    # =====================================================
    # KPIs GERENCIALES
    # =====================================================

    fill_rate = kpis.get("fill_rate", 0)
    mae = kpis.get("mae", 0)
    inv = kpis.get("inventario_prom", 0)

    content.append(Paragraph("<b>2. Indicadores Clave de Desempeño</b>", title))

    kpi_table = Table([[
        f"Nivel de Servicio\n{fill_rate:.2%}",
        f"Error de Pronóstico\n{mae:.2f}",
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
    - El nivel de servicio refleja la capacidad de cumplir demanda del cliente.<br/>
    - El error de pronóstico indica la precisión del modelo de planificación.<br/>
    - El inventario promedio representa capital inmovilizado.
    """, body))

    content.append(Spacer(1, 15))

    # =====================================================
    # JUSTIFICACION PYTHON
    # =====================================================

    content.append(Paragraph("<b>3. Justificación Tecnológica (Python)</b>", title))

    content.append(Paragraph("""
    El sistema fue desarrollado en <b>Python</b> debido a su capacidad analítica,
    ecosistema de librerías y escalabilidad para proyectos de ciencia de datos.

    Python permite integrar:
    • Procesamiento de datos (Pandas)<br/>
    • Modelos predictivos (Scikit-learn)<br/>
    • Automatización de reportes (ReportLab)<br/>
    • Dashboards interactivos (Streamlit)

    Esto reduce significativamente el tiempo de análisis manual y habilita
    decisiones basadas en datos en tiempo real.
    """, body))

    content.append(Spacer(1, 15))

    # =====================================================
    # OPTIMIZACION Y COSTOS
    # =====================================================

    ahorro = inv * 0.12

    content.append(Paragraph("<b>4. Impacto en Costos y Optimización</b>", title))

    content.append(Paragraph(f"""
    El modelo de optimización permite reducir inventario innecesario mediante
    la aplicación de reglas de reposición (ROP, EOQ y stock de seguridad).

    <b>Impacto estimado:</b><br/>
    • Reducción de sobrestock: 10% - 15%<br/>
    • Mejora en rotación de inventario<br/>
    • Disminución de capital inmovilizado

    <b>Ahorro estimado anual:</b> ${ahorro:,.0f}
    """, body))

    content.append(Spacer(1, 15))

    # =====================================================
    # FLUJO
    # =====================================================

    content.append(Paragraph("<b>5. Flujo del Sistema</b>", title))

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

    content.append(Spacer(1, 15))

    # =====================================================
    # DATOS
    # =====================================================

    content.append(Paragraph("<b>6. Estructura de Datos</b>", title))

    table = [
        ["Campo", "Descripción"],
        ["fecha", "Tiempo de registro"],
        ["sku", "Identificador de producto"],
        ["demanda", "Demanda proyectada"],
        ["ventas", "Ventas reales"],
        ["inventario", "Stock disponible"],
        ["lead_time", "Tiempo de reposición"],
        ["costo_unitario", "Costo por unidad"]
    ]

    t = Table(table, colWidths=[120, 350])

    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B2E4A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    content.append(t)

    content.append(Spacer(1, 15))

    # =====================================================
    # CONCLUSION EJECUTIVA
    # =====================================================

    content.append(Paragraph("<b>7. Conclusión Ejecutiva</b>", title))

    content.append(Paragraph("""
    La implementación de ESMAX Control Tower permite transformar la gestión de inventario
    desde un enfoque reactivo a uno predictivo.

    Esto habilita:
    • Mayor eficiencia operativa<br/>
    • Reducción de costos estructurales<br/>
    • Mejor nivel de servicio al cliente<br/>
    • Toma de decisiones basada en datos

    El sistema representa una herramienta escalable para la digitalización
    de la cadena de suministro.
    """, body))

    content.append(Spacer(1, 20))

    # =====================================================
    # FOOTER
    # =====================================================

    content.append(Paragraph("""
    <hr/>
    ESMAX Control Tower © 2026<br/>
    Proyecto desarrollado por Ignacio Álvarez, Benjamín Tello y Renato Soto
    """, body))

    doc.build(content)
    buffer.seek(0)
    return buffer.read()
