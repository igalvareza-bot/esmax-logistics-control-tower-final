# modules/pdf_report.py
import io
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generar_pdf_bytes(df, kpis):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=None)
    styles = getSampleStyleSheet()
    content = []

    # Intentar incluir layout grande como cabecera si existe
    if os.path.exists("LAYOUT.png"):
        try:
            img = RLImage("LAYOUT.png", width=500, height=120)
            content.append(img)
            content.append(Spacer(1, 8))
        except Exception:
            pass

    # Intentar incluir logo pequeño
    if os.path.exists("logo_esmax.png"):
        try:
            logo = RLImage("logo_esmax.png", width=120, height=40)
            content.append(logo)
            content.append(Spacer(1, 6))
        except Exception:
            pass

    content.append(Paragraph("ESMAX CONTROL TOWER REPORT", styles["Title"]))
    content.append(Spacer(1, 8))
    content.append(Paragraph(f"Fill Rate: {kpis.get('fill_rate',0):.2%}", styles["Normal"]))
    content.append(Paragraph(f"MAE: {kpis.get('mae',0):.1f}", styles["Normal"]))
    content.append(Paragraph(f"Inventario Prom: {kpis.get('inventario_prom',0):.0f}", styles["Normal"]))
    content.append(Spacer(1, 12))

    # Tabla resumen (primeras 20 filas)
    try:
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
    except Exception:
        content.append(Paragraph("No se pudo generar tabla de muestra.", styles["Normal"]))

    doc.build(content)
    buffer.seek(0)
    return buffer.read()
