"""
PDF Report Generator Module for Mevzuat Radarı.
Produces professional, executive-ready Internal Audit and Compliance PDF reports.
"""
import os
from datetime import datetime
from typing import Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)

from .models import DailyAuditReport


def generate_pdf_report(report: DailyAuditReport, output_path: str) -> str:
    """
    Renders DailyAuditReport into a styled PDF file at output_path.
    Returns the absolute path to the generated PDF.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1a365d"),
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4a5568"),
    )

    item_title_style = ParagraphStyle(
        "ItemTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#2d3748"),
    )

    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2d3748"),
    )

    bold_label_style = ParagraphStyle(
        "BoldLabel",
        parent=body_style,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1a202c"),
    )

    story = []

    # 1. Header Section
    story.append(Paragraph("Resmî Gazete İç Denetim & Uyum Bülteni", title_style))
    story.append(
        Paragraph(
            f"<b>Şirket:</b> {report.company_name} | <b>Tarih:</b> {report.date} | <b>Sayı:</b> {report.gazette_number or 'Günlük'}<br/>"
            f"<b>Taranan Madde:</b> {report.total_scanned} | <b>İlgili Bulunan:</b> {report.relevant_count} | <i>Oluşturulma: {report.generated_at}</i>",
            subtitle_style,
        )
    )
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#cbd5e0"), spaceAfter=14))

    # 2. Evaluations Section
    if not report.evaluations:
        no_item_text = (
            "<b>Bugün İçin Şirketi İlgilendiren Kritik Bir Karar Bulunmadı:</b><br/>"
            "Şirket profilindeki sektör, NACE kodları ve düzenleyici kurum kriterlerine uyan öncelikli bir tebliğ/yönetmelik tespit edilmemiştir."
        )
        story.append(Paragraph(no_item_text, body_style))
    else:
        for idx, ev in enumerate(report.evaluations, 1):
            item_elements = []

            # Risk color
            risk_bg = colors.HexColor("#fee2e2") if ev.risk_level == "Kritik" else (
                colors.HexColor("#ffedd5") if ev.risk_level == "Yüksek" else colors.HexColor("#fef9c3")
            )
            risk_text_color = colors.HexColor("#991b1b") if ev.risk_level == "Kritik" else (
                colors.HexColor("#9a3412") if ev.risk_level == "Yüksek" else colors.HexColor("#854d0e")
            )

            header_text = f"<b>[{ev.risk_level.upper()}]</b> {idx}. {ev.item.title}"
            item_elements.append(Paragraph(header_text, item_title_style))
            item_elements.append(Spacer(1, 4))

            # Metadata Table
            meta_data = [
                [
                    Paragraph(f"<b>Kategori:</b> {ev.item.category}", body_style),
                    Paragraph(f"<b>Alaka Skoru:</b> %{ev.relevance_score}", body_style),
                ],
                [
                    Paragraph(f"<b>Düzenleyen:</b> {ev.item.institution or 'Belirtilmemiş'}", body_style),
                    Paragraph(f"<b>Yürürlük:</b> {ev.effective_date or 'Yayımı Tarihinde'}", body_style),
                ],
            ]
            meta_table = Table(meta_data, colWidths=[280, 240])
            meta_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                    ("PADDING", (0, 0), (-1, -1), 4),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#edf2f7")),
                ])
            )
            item_elements.append(meta_table)
            item_elements.append(Spacer(1, 6))

            # Summary
            item_elements.append(Paragraph("<b>Yönetici Özeti:</b>", bold_label_style))
            item_elements.append(Paragraph(ev.executive_summary, body_style))
            item_elements.append(Spacer(1, 5))

            # Reasons
            reasons_formatted = "<br/>".join([f"• {r}" for r in ev.matched_reasons])
            item_elements.append(Paragraph("<b>Eşleşme Gerekçeleri:</b>", bold_label_style))
            item_elements.append(Paragraph(reasons_formatted, body_style))
            item_elements.append(Spacer(1, 5))

            # Penalty & Risk
            if ev.penalty_and_legal_risk:
                item_elements.append(Paragraph("<b>Yaptırım & Cezai Risk:</b>", bold_label_style))
                item_elements.append(Paragraph(ev.penalty_and_legal_risk, body_style))
                item_elements.append(Spacer(1, 5))

            # Affected Departments
            deps_str = ", ".join(ev.affected_departments)
            item_elements.append(Paragraph(f"<b>Etkilenen Departmanlar:</b> {deps_str}", body_style))
            item_elements.append(Spacer(1, 5))

            # Checklist
            item_elements.append(Paragraph("<b>İç Denetim Aksiyon Kontrol Listesi:</b>", bold_label_style))
            checklist_formatted = "<br/>".join([f"[  ] {chk}" for chk in ev.action_checklist])
            item_elements.append(Paragraph(checklist_formatted, body_style))
            item_elements.append(Spacer(1, 10))
            item_elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=10))

            story.append(KeepTogether(item_elements))

    # 3. Footer / Disclaimer
    story.append(Spacer(1, 14))
    footer_text = f"Bu rapor, Mevzuat Radarı (Model Context Protocol) tarafından {report.generated_at} tarihinde otomatik olarak oluşturulmuştur."
    story.append(Paragraph(footer_text, subtitle_style))

    # Build document
    doc.build(story)
    return os.path.abspath(output_path)
