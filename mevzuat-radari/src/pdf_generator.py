"""
PDF Report Generator Module for Mevzuat Radarı.
Produces professional, executive-ready Internal Audit and Compliance PDF reports
with full UTF-8 / Turkish character support and precise Gazette location references.
"""
import os
from datetime import datetime
from typing import Optional
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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


# Register Unicode Font for Turkish character support
FONT_NAME = "Helvetica"
FONT_NAME_BOLD = "Helvetica-Bold"

CANDIDATE_FONTS = [
    ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ("/System/Library/Fonts/Supplemental/Verdana.ttf", "/System/Library/Fonts/Supplemental/Verdana Bold.ttf"),
    ("/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
]

for reg_path, bold_path in CANDIDATE_FONTS:
    if os.path.exists(reg_path):
        try:
            pdfmetrics.registerFont(TTFont("TurkishCustom", reg_path))
            FONT_NAME = "TurkishCustom"
            if os.path.exists(bold_path):
                pdfmetrics.registerFont(TTFont("TurkishCustom-Bold", bold_path))
                FONT_NAME_BOLD = "TurkishCustom-Bold"
            else:
                FONT_NAME_BOLD = "TurkishCustom"
            break
        except Exception:
            continue


def generate_pdf_report(report: DailyAuditReport, output_path: str) -> str:
    """
    Renders DailyAuditReport into a styled, professional PDF file at output_path.
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

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName=FONT_NAME_BOLD,
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=3,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName=FONT_NAME,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#475569"),
    )

    item_title_style = ParagraphStyle(
        "ItemTitle",
        parent=styles["Heading2"],
        fontName=FONT_NAME_BOLD,
        fontSize=10.5,
        leading=13.5,
        textColor=colors.HexColor("#0f172a"),
    )

    body_style = ParagraphStyle(
        "BodyTextCustom",
        parent=styles["Normal"],
        fontName=FONT_NAME,
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#334155"),
    )

    bold_label_style = ParagraphStyle(
        "BoldLabel",
        parent=body_style,
        fontName=FONT_NAME_BOLD,
        textColor=colors.HexColor("#0f172a"),
    )

    location_style = ParagraphStyle(
        "LocationStyle",
        parent=body_style,
        fontName=FONT_NAME,
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#2563eb"),
    )

    story = []

    # 1. Header Section
    story.append(Paragraph("T.C. RESMÎ GAZETE İÇ DENETİM & UYUM BÜLTENİ", title_style))
    story.append(
        Paragraph(
            f"<b>Kurum / Şirket:</b> {report.company_name} | <b>Dönem/Tarih:</b> {report.date} | <b>Sayı:</b> {report.gazette_number or 'Günlük Sayı'}<br/>"
            f"<b>Taranan Madde Sayısı:</b> {report.total_scanned} | <b>İlgili Bulunan Madde:</b> {report.relevant_count} | <i>Rapor Derleme: {report.generated_at}</i>",
            subtitle_style,
        )
    )
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=12))

    # 2. Evaluations Section
    if not report.evaluations:
        no_item_text = (
            "<b>Bu Dönem/Tarih İçin Şirketi İlgilendiren Kritik Karar Bulunmadı:</b><br/>"
            "Şirket profilindeki sektör, NACE kodları ve düzenleyici kurum kriterlerine uyan öncelikli bir tebliğ veya yönetmelik tespit edilmemiştir."
        )
        story.append(Paragraph(no_item_text, body_style))
    else:
        for idx, ev in enumerate(report.evaluations, 1):
            item_elements = []

            # Header with risk badge
            header_text = f"<b>[{ev.risk_level.upper()}]</b> {idx}. {ev.item.title}"
            item_elements.append(Paragraph(header_text, item_title_style))
            item_elements.append(Spacer(1, 2))

            # Resmî Gazete Precise Location Breadcrumb
            loc_text = ev.item.location_breadcrumb or f"{ev.item.gazette_date or report.date} Resmî Gazete > {ev.item.section} > {ev.item.category}"
            item_elements.append(Paragraph(f"<b>Kaynak Konumu:</b> {loc_text}", location_style))
            item_elements.append(Spacer(1, 3))

            # Metadata Table
            meta_data = [
                [
                    Paragraph(f"<b>Kategori:</b> {ev.item.category}", body_style),
                    Paragraph(f"<b>Alaka Skoru:</b> %{ev.relevance_score}", body_style),
                ],
                [
                    Paragraph(f"<b>Düzenleyen:</b> {ev.item.institution or 'Resmî Gazete'}", body_style),
                    Paragraph(f"<b>Yürürlük:</b> {ev.effective_date or 'Yayımı Tarihinde'}", body_style),
                ],
            ]
            meta_table = Table(meta_data, colWidths=[280, 240])
            meta_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                    ("PADDING", (0, 0), (-1, -1), 3),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#f1f5f9")),
                ])
            )
            item_elements.append(meta_table)
            item_elements.append(Spacer(1, 4))

            # Summary
            item_elements.append(Paragraph("<b>İç Denetim Yönetici Özeti:</b>", bold_label_style))
            item_elements.append(Paragraph(ev.executive_summary, body_style))
            item_elements.append(Spacer(1, 3))

            # Matched Reasons
            reasons_formatted = "<br/>".join([f"• {r}" for r in ev.matched_reasons])
            item_elements.append(Paragraph("<b>Eşleşme Gerekçeleri:</b>", bold_label_style))
            item_elements.append(Paragraph(reasons_formatted, body_style))
            item_elements.append(Spacer(1, 3))

            # Penalty & Risk
            if ev.penalty_and_legal_risk:
                item_elements.append(Paragraph("<b>Hukuki Risk & Yaptırım:</b>", bold_label_style))
                item_elements.append(Paragraph(ev.penalty_and_legal_risk, body_style))
                item_elements.append(Spacer(1, 3))

            # Affected Departments
            deps_str = ", ".join(ev.affected_departments)
            item_elements.append(Paragraph(f"<b>Etkilenen Departmanlar:</b> {deps_str}", body_style))
            item_elements.append(Spacer(1, 3))

            # Checklist
            item_elements.append(Paragraph("<b>İç Denetim Aksiyon Kontrol Listesi:</b>", bold_label_style))
            checklist_formatted = "<br/>".join([f"[  ] {chk}" for chk in ev.action_checklist])
            item_elements.append(Paragraph(checklist_formatted, body_style))
            item_elements.append(Spacer(1, 6))
            item_elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0"), spaceAfter=6))

            story.append(KeepTogether(item_elements))

    # 3. Footer
    story.append(Spacer(1, 8))
    footer_text = f"Bu rapor, Mevzuat Radarı tarafından {report.generated_at} tarihinde otomatik olarak derlenmiştir."
    story.append(Paragraph(footer_text, subtitle_style))

    doc.build(story)
    return os.path.abspath(output_path)
