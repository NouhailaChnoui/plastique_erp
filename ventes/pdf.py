"""Génération de la facture PDF de vente avec ReportLab."""
import io
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER

BLUE = colors.HexColor("#2955e0")
GRAY = colors.HexColor("#5b6577")
LIGHT = colors.HexColor("#eef1f7")


def generer_facture_pdf(vente):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=20 * mm, bottomMargin=20 * mm, leftMargin=18 * mm, rightMargin=18 * mm,
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CompanyName", fontSize=16, textColor=BLUE, fontName="Helvetica-Bold", spaceAfter=2))
    styles.add(ParagraphStyle(name="FactureTitle", fontSize=20, alignment=TA_RIGHT, textColor=BLUE, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="Small", fontSize=9, textColor=GRAY))
    styles.add(ParagraphStyle(name="SmallRight", fontSize=9, textColor=GRAY, alignment=TA_RIGHT))
    styles.add(ParagraphStyle(name="SectionLabel", fontSize=9, textColor=GRAY, fontName="Helvetica-Bold"))

    elements = []

    # --- En-tête : logo / nom entreprise + titre facture ---
    header_data = [[
        Paragraph(f"<para>{settings.NOM_ENTREPRISE}</para>", styles["CompanyName"]),
        Paragraph("FACTURE", styles["FactureTitle"]),
    ]]
    header_table = Table(header_data, colWidths=[100 * mm, 72 * mm])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(header_table)
    elements.append(Paragraph("Achat et vente de matières plastiques", styles["Small"]))
    elements.append(Spacer(1, 4 * mm))

    meta_data = [[
        Paragraph(f"<b>N° Facture :</b> {vente.numero_facture}", styles["Small"]),
        Paragraph(f"<b>Date :</b> {vente.date_vente.strftime('%d/%m/%Y')}", styles["SmallRight"]),
    ]]
    meta_table = Table(meta_data, colWidths=[100 * mm, 72 * mm])
    elements.append(meta_table)
    elements.append(Spacer(1, 6 * mm))

    # --- Bloc client ---
    client = vente.client
    client_lines = [f"<b>Facturé à :</b>", client.nom]
    if client.telephone:
        client_lines.append(client.telephone)
    if client.ville or client.adresse:
        client_lines.append(f"{client.adresse} {client.ville}".strip())
    elements.append(Paragraph("<br/>".join(client_lines), styles["Small"]))
    elements.append(Spacer(1, 8 * mm))

    # --- Tableau produit ---
    table_data = [["Produit", "Quantité", "Prix unitaire (DH)", "Total (DH)"]]
    table_data.append([
        vente.materiau.nom,
        f"{vente.quantite:.2f}",
        f"{vente.prix_unitaire:.2f}",
        f"{vente.montant_total:.2f}",
    ])

    prod_table = Table(table_data, colWidths=[65 * mm, 35 * mm, 40 * mm, 32 * mm])
    prod_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e3e8f1")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(prod_table)
    elements.append(Spacer(1, 6 * mm))

    # --- Total ---
    total_data = [["", "Montant total", f"{vente.montant_total:.2f} DH"]]
    total_table = Table(total_data, colWidths=[100 * mm, 40 * mm, 32 * mm])
    total_table.setStyle(TableStyle([
        ("FONTNAME", (1, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (1, 0), (-1, -1), 11),
        ("TEXTCOLOR", (1, 0), (-1, -1), BLUE),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("LINEABOVE", (1, 0), (-1, 0), 1, BLUE),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(total_table)
    elements.append(Spacer(1, 14 * mm))

    elements.append(Paragraph(f"N° bon de pesée : {vente.numero_bon}", styles["Small"]))
    elements.append(Spacer(1, 20 * mm))
    elements.append(Paragraph("Merci de votre confiance.", styles["Small"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def generer_facture_groupee_pdf(ventes):
    """Génère un relevé PDF regroupant plusieurs ventes avec un total général."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=20 * mm, bottomMargin=20 * mm, leftMargin=18 * mm, rightMargin=18 * mm,
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CompanyNameG", fontSize=16, textColor=BLUE, fontName="Helvetica-Bold", spaceAfter=2))
    styles.add(ParagraphStyle(name="FactureTitleG", fontSize=18, alignment=TA_RIGHT, textColor=BLUE, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="SmallG", fontSize=9, textColor=GRAY))
    styles.add(ParagraphStyle(name="SmallRightG", fontSize=9, textColor=GRAY, alignment=TA_RIGHT))

    elements = []

    header_data = [[
        Paragraph(f"<para>{settings.NOM_ENTREPRISE}</para>", styles["CompanyNameG"]),
        Paragraph("RELEVÉ DE FACTURES", styles["FactureTitleG"]),
    ]]
    header_table = Table(header_data, colWidths=[100 * mm, 72 * mm])
    header_table.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(header_table)
    elements.append(Paragraph("Achat et vente de matières plastiques", styles["SmallG"]))
    elements.append(Spacer(1, 4 * mm))

    from django.utils import timezone
    today_str = timezone.now().strftime("%d/%m/%Y")
    elements.append(Paragraph(f"<b>Date d'édition :</b> {today_str}", styles["SmallG"]))
    elements.append(Paragraph(f"<b>Nombre de factures :</b> {len(ventes)}", styles["SmallG"]))
    elements.append(Spacer(1, 8 * mm))

    table_data = [["Facture", "Client", "Matière", "Date", "Quantité", "Prix unit. (DH)", "Montant (DH)"]]
    total_general = 0
    for v in ventes:
        table_data.append([
            v.numero_facture,
            v.client.nom,
            v.materiau.nom,
            v.date_vente.strftime("%d/%m/%Y"),
            f"{v.quantite:.2f} Kg",
            f"{v.prix_unitaire:.2f}",
            f"{v.montant_total:.2f}",
        ])
        total_general += v.montant_total

    prod_table = Table(table_data, colWidths=[25 * mm, 32 * mm, 28 * mm, 20 * mm, 20 * mm, 24 * mm, 23 * mm])
    prod_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ALIGN", (3, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e3e8f1")),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    elements.append(prod_table)
    elements.append(Spacer(1, 6 * mm))

    total_data = [["", "TOTAL GÉNÉRAL", f"{total_general:.2f} DH"]]
    total_table = Table(total_data, colWidths=[110 * mm, 40 * mm, 24 * mm])
    total_table.setStyle(TableStyle([
        ("FONTNAME", (1, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (1, 0), (-1, -1), 11),
        ("TEXTCOLOR", (1, 0), (-1, -1), BLUE),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("LINEABOVE", (1, 0), (-1, 0), 1, BLUE),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(total_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
