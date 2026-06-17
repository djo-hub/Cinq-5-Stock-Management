from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
import os
from app.config import load_settings
from app.i18n import t, translate_status
from app.utils import resource_path


def _footer_builder(contact_line):
    """Return a canvas callback that draws the contact info as a centred footer."""
    def _draw_footer(canvas, doc):
        if contact_line:
            canvas.saveState()
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(colors.HexColor("#666666"))
            page_width = A4[0]
            canvas.drawCentredString(page_width / 2, 1.2 * cm, contact_line)
            canvas.restoreState()
    return _draw_footer


def generate_invoice_pdf(invoice, output_path=None):
    if output_path is None:
        date_str = invoice.date.strftime("%Y-%m-%d")
        output_path = f"invoice_{date_str}_#{invoice.id}.pdf"

    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []

    cfg = load_settings()
    biz_name    = cfg.get("business_name", "MY BUSINESS")
    biz_address = cfg.get("business_address", "")
    biz_phone   = cfg.get("business_phone", "")
    biz_email   = cfg.get("business_email", "")
    currency    = cfg.get("currency", "DA")
    tva_rate    = cfg.get("tva_rate", 0.0)

    contact_parts = [p for p in [biz_address, biz_phone, biz_email] if p]
    contact_line  = " | ".join(contact_parts)

    # Logo
    logo_path = resource_path(os.path.join("assets", "icon-2.png"))
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=5.5*cm, height=3.5*cm)
        logo.hAlign = "CENTER"
        story.append(logo)
        story.append(Spacer(1, 0.3*cm))

    # Header (business name only — contact info moved to footer)
    story.append(Paragraph(f"<b>{biz_name}</b>", styles["Title"]))
    story.append(Spacer(1, 0.5*cm))

    # Invoice meta
    story.append(Paragraph(f"<b>{t('pdf.invoice_num')}</b> {invoice.id}", styles["Normal"]))
    story.append(Paragraph(f"<b>{t('pdf.date')}</b> {invoice.date.strftime('%Y-%m-%d')}", styles["Normal"]))
    story.append(Paragraph(f"<b>{t('pdf.client')}</b> {invoice.client.name}", styles["Normal"]))
    story.append(Paragraph(f"<b>{t('pdf.phone')}</b> {invoice.client.phone}", styles["Normal"]))
    story.append(Spacer(1, 0.5*cm))

    # Items table
    table_data = [[t("pdf.col_num"), t("pdf.col_product"), t("pdf.col_qty"), t("pdf.col_unit_price"), t("pdf.col_total")]]
    subtotal = 0.0
    for idx, item in enumerate(invoice.items, 1):
        item_total = item.qty * item.unit_price
        subtotal += item_total
        table_data.append([
            str(idx),
            item.product.name,
            str(item.qty),
            f"{item.unit_price:.2f} {currency}",
            f"{item_total:.2f} {currency}"
        ])
    
    # Calculate TVA and total
    tva_amount = subtotal * (tva_rate / 100.0)
    total = subtotal + tva_amount
    
    # Add subtotal, TVA, and total rows
    table_data.append(["", "", "", f"{t('pdf.subtotal')}", f"{subtotal:.2f} {currency}"])
    if tva_rate > 0:
        table_data.append(["", "", "", f"{t('pdf.tva').format(rate=tva_rate)}", f"{tva_amount:.2f} {currency}"])
    table_data.append(["", "", "", f"{t('pdf.total')}", f"{total:.2f} {currency}"])

    table = Table(table_data, colWidths=[1*cm, 7*cm, 2*cm, 3.5*cm, 3.5*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -3), [colors.white, colors.HexColor("#f2f2f2")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, -3), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -3), (-1, -1), colors.HexColor("#ecf0f1")),
    ]))
    story.append(table)
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(f"<b>{t('pdf.status')}</b> {translate_status(invoice.status)}", styles["Normal"]))
    if invoice.notes:
        story.append(Paragraph(f"<b>{t('pdf.notes')}</b> {invoice.notes}", styles["Normal"]))

    footer_cb = _footer_builder(contact_line)
    doc.build(story, onFirstPage=footer_cb, onLaterPages=footer_cb)
    return output_path
