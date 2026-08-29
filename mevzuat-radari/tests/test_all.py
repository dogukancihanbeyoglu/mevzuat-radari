"""
Unit and Integration Tests for Mevzuat Radarı.
"""
import pytest
import os
import sys

# Ensure src is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.models import (
    CompanyProfile,
    GeneralCompanyInfo,
    SectorsAndNace,
    OperationalTraits,
    KeywordsConfig,
    GazetteItem,
    GazetteIndex,
)
from src.scraper import parse_gazette_index, get_gazette_url_for_date
from src.evaluator import (
    load_company_profile,
    score_item_relevance,
    infer_affected_departments,
    generate_action_checklist,
    evaluate_gazette_item,
)
from src.templates import format_markdown_report, format_html_report


def test_company_profile_loading():
    profile = load_company_profile("config/company_profile.yaml")
    assert profile.general.name is not None
    assert len(profile.sectors_and_nace.nace_codes) > 0
    assert len(profile.regulatory_bodies) > 0
    assert "tax_and_finance" in profile.risk_priorities


def test_gazette_url_formatting():
    url, date_str = get_gazette_url_for_date("2026-08-29")
    assert date_str == "2026-08-29"
    assert "resmigazete.gov.tr" in url


def test_parse_mock_gazette_html():
    mock_html = """
    <html>
    <head><title>Resmî Gazete</title></head>
    <body>
        <div>Sayı : 33000</div>
        <h3>YÖNETMELİKLER</h3>
        <p>Ticaret Bakanlığından:</p>
        <a href="/eskiler/2026/08/20260829-1.htm">Mesafeli Sözleşmeler Yönetmeliğinde Değişiklik Yapılmasına Dair Yönetmelik</a>
        <a href="/eskiler/2026/08/20260829-2.pdf">Katma Değer Vergisi Genel Uygulama Tebliği</a>
    </body>
    </html>
    """
    index = parse_gazette_index(mock_html, "2026-08-29")
    assert index.gazette_number == "33000"
    assert len(index.items) == 2
    assert index.items[0].category == "Yönetmelik"
    assert "Mesafeli" in index.items[0].title
    assert index.items[1].is_pdf is True


def test_scoring_high_relevance_ecommerce():
    profile = load_company_profile("config/company_profile.yaml")
    item = GazetteItem(
        title="Elektronik Ticarette Mesafeli Sözleşmeler ve Tüketici İadeleri Tebliği",
        url="https://resmigazete.gov.tr/sample",
        category="Tebliğ",
        institution="Ticaret Bakanlığı",
    )
    score, reasons, risk = score_item_relevance(item, profile)
    assert score >= 75
    assert risk == "Kritik"
    assert any("E-Ticaret" in r or "anahtar" in r for r in reasons)


def test_scoring_unrelated_item():
    profile = load_company_profile("config/company_profile.yaml")
    item = GazetteItem(
        title="Orman Köylülerinin Kalkındırılması ve Ağaçlandırma İhalesi Tebliği",
        url="https://resmigazete.gov.tr/sample2",
        category="Tebliğ",
        institution="Tarım ve Orman Bakanlığı",
    )
    score, reasons, risk = score_item_relevance(item, profile)
    assert score == 0
    assert risk == "Bilgi"


def test_affected_departments_inference():
    deps = infer_affected_departments("Katma Değer Vergisi Fatura Düzenleme Tebliği", [])
    assert "Mali İşler & Muhasebe" in deps

    deps_hr = infer_affected_departments("Asgari Ücret ve Kıdem Tazminatı Tavanı Genelgesi", [])
    assert "İnsan Kaynakları" in deps_hr


def test_checklist_generation():
    checklist = generate_action_checklist("Katma Değer Vergisi Tebliği", "Tebliğ", "Yüksek")
    assert len(checklist) > 0
    assert any("ERP" in c or "parametre" in c for c in checklist)


def test_templates_rendering():
    profile = load_company_profile("config/company_profile.yaml")
    item = GazetteItem(
        title="Ödeme Kuruluşları Bilgi Sistemleri Tebliği",
        url="https://resmigazete.gov.tr/pay",
        category="Tebliğ",
    )
    evaluation = evaluate_gazette_item(item, profile)
    from src.models import DailyAuditReport
    report = DailyAuditReport(
        date="2026-08-29",
        company_name="Mega Perakende A.Ş.",
        total_scanned=10,
        relevant_count=1,
        evaluations=[evaluation],
        generated_at="2026-08-29 12:00:00",
    )

    md = format_markdown_report(report)
    assert "Resmî Gazete İç Denetim & Uyum Bülteni" in md
    assert "Ödeme Kuruluşları" in md

    html = format_html_report(report)
    assert "<!DOCTYPE html>" in html
    assert "Mega Perakende A.Ş." in html
