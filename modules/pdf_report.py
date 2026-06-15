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
from reportlab.lib.enums import TA_CENTER, TA_LEFT


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

    body = ParagraphStyle(
        "body",
        parent=styles["Normal"],
        alignment=TA_LEFT,
        leading=14
    )

    content = []

    # =====================================================
    # PORTADA
    # =====================================================
    content.append(Spacer(1, 10))
    content.append(Paragraph("ESMAX CONTROL TOWER", title))
    content.append(Paragraph("Informe Ejecutivo de Supply Chain & Inventario", subtitle))
    content.append(Spacer(1, 10))

    content.append(Paragraph("""
    Elaborado por:<br/>
    Ignacio Álvarez<br/>
    Benjamín Tello<br/>
    Renato Soto
    """, body))

    content.append(Spacer(1, 15))

    # =====================================================
    # RESUMEN EJECUTIVO
    # =====================================================
    content.append(Paragraph("<b>1. Resumen Ejecutivo</b>", title))

    content.append(Paragraph("""
    El sistema ESMAX Control Tower integra analítica predictiva, control de inventario
    y optimización de reposición, permitiendo transformar decisiones operativas en
    decisiones basadas en datos.

    Su objetivo es reducir quiebres de stock, optimizar capital inmovilizado y mejorar
    el nivel de servicio en la cadena de suministro.
    """, body))

    content.append(Spacer(1, 10))

    # =====================================================
    # KPIs
    # =====================================================
    fill_rate = kpis.get("fill_rate", 0)
    mae = kpis.get("mae", 0)
    inv = kpis.get("inventario_prom", 0)

    def semaforo(valor, tipo):
        if tipo == "fill":
            return "🟢" if valor >= 0.95 else "🟡" if valor >= 0.85 else "🔴"
        if tipo == "mae":
            return "🟢" if valor < 20 else "🟡" if valor < 50 else "🔴"
        return "🟢"

    content.append(Paragraph("<b>2. KPIs de Desempeño</b>", title))

    kpi_table = Table([
        [
            f"{semaforo(fill_rate,'fill')} Nivel de Servicio\n{fill_rate:.2%}",
            f"{semaforo(mae,'mae')} Error de Pronóstico\n{mae:.2f}",
            f"📦 Inventario Promedio\n{inv:.0f}"
        ]
    ], colWidths=[160, 160, 160])

    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#1F8A70")),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#F39C12")),
        ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#2E86C1")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
    ]))

    content.append(kpi_table)

    content.append(Spacer(1, 10))

    content.append(Paragraph("""
    <b>Interpretación ejecutiva:</b><br/>
    • Nivel de servicio indica capacidad de respuesta al cliente.<br/>
    • Error de pronóstico refleja precisión del modelo predictivo.<br/>
    • Inventario representa capital inmovilizado.
    """, body))

    content.append(Spacer(1, 12))

    # =====================================================
    # DECISIONES
    # =====================================================
    suggested_order = max(0, int(inv * 0.1))

    content.append(Paragraph("<b>3. Decisiones Operacionales</b>", title))

    content.append(Paragraph(f"""
    El sistema recomienda automáticamente acciones de reposición:

    • Orden sugerida: <b>{suggested_order} unidades</b><br/>
    • Política: EOQ + ROP simplificado<br/>
    • Objetivo: minimizar quiebres y sobrestock

    <b>Resultado:</b> decisiones automatizadas basadas en demanda histórica.
    """, body))

    content.append(Spacer(1, 12))

    # =====================================================
    # COSTOS
    # =====================================================
    costo_inventario = inv * 0.12
    ahorro = costo_inventario * 0.15

    content.append(Paragraph("<b>4. Impacto Económico</b>", title))

    content.append(Paragraph(f"""
    La optimización de inventario genera impacto financiero directo:

    • Costo estimado de inventario: ${costo_inventario:,.0f}<br/>
    • Ahorro potencial anual: ${ahorro:,.0f}<br/>
    • Reducción de sobrestock: 10% - 15%

    <b>Nota:</b> valores estimados sobre modelo simplificado.
    """, body))

    content.append(Spacer(1, 12))

    # =====================================================
    # FLUJO
    # =====================================================
    flow = Table([[
        "Datos", "→", "Forecast", "→", "Optimización", "→", "Decisión"
    ]])

    flow.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E8F4FD")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
    ]))

    content.append(flow)

    content.append(Spacer(1, 20))

    # =====================================================
    # PAGE BREAK → FICHA TÉCNICA (NUEVO NIVEL)
    # =====================================================
    content.append(PageBreak())

    content.append(Paragraph("<b>5. Ficha Técnica del Sistema</b>", title))

    content.append(Paragraph("""
    <b>Proyecto:</b> ESMAX Control Tower<br/>
    <b>Carrera:</b> Ingeniería en Gestión Logística (5to semestre)<br/>
    <b>Tipo:</b> Sistema de soporte a decisiones basado en datos
    """, body))

    content.append(Spacer(1, 10))

    content.append(Paragraph("""
    <b>Arquitectura tecnológica:</b><br/>
    • Python (lógica principal)<br/>
    • Streamlit (interfaz web)<br/>
    • Pandas / NumPy (procesamiento de datos)<br/>
    • Scikit-learn (forecast)<br/>
    • ReportLab (generación de PDF)
    """, body))

    content.append(Spacer(1, 10))

    content.append(Paragraph("""
    <b>Esfuerzo de desarrollo estimado:</b><br/>
    • 1 a 2 semanas de desarrollo iterativo<br/>
    • Integración modular de 4 sistemas analíticos<br/>
    • Validación de flujo completo de supply chain
    """, body))

    content.append(Spacer(1, 10))

    content.append(Paragraph("""
    <b>Valor estimado en entorno empresarial:</b><br/>
    • Dashboard básico: USD 5.000 – 15.000<br/>
    • Sistema predictivo: USD 20.000 – 50.000<br/>
    • Control Tower completo: USD 80.000+
    """, body))

    content.append(Spacer(1, 10))

    content.append(Paragraph("""
    <b>Limitaciones del modelo:</b><br/>
    • Datos simulados o simplificados<br/>
    • Costos estimados (no contables reales)<br/>
    • Forecast base (no modelo avanzado industrial)
    """, body))

    content.append(Spacer(1, 15))

    # =====================================================
    # FOOTER + LAYOUT
    # =====================================================
    content.append(Paragraph("<b>ESMAX CONTROL TOWER</b>", title))

    if os.path.exists("LAYOUT.png"):
        try:
            content.append(Spacer(1, 10))
            content.append(RLImage("LAYOUT.png", width=400, height=90))
        except:
            pass

    doc.build(content)
    buffer.seek(0)

    return buffer.read()
