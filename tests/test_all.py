"""
Unit and Integration Tests for Mevzuat Radarı (Multi-Layered Compliance Matrix).
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
    assert "STM" in profile.general.name
    assert len(profile.sectors_and_nace.nace_codes) > 0
    assert "Cumhurbaşkanlığı Savunma Sanayii Başkanlığı (SSB)" in profile.regulatory_bodies
    assert "defense_procurement_and_export_control" in profile.risk_priorities


def test_gazette_url_formatting():
    url, date_str = get_gazette_url_for_date("2026-08-29")
    assert date_str == "2026-08-29"
    assert "resmigazete.gov.tr" in url


def test_parse_mock_gazette_html():
    mock_html = """
    <html>
    <head><title>Resmî Gazete</title></head>
    <body>
        <div>Sayı : 33355</div>
        <h3>CUMHURBAŞKANI KARARLARI</h3>
        <a href="/eskiler/2026/08/20260829-2.pdf">Sınırları Gösterilen Alanın “Milli Savunma Üniversitesi Teknoloji Geliştirme Bölgesi” Olarak Tespit Edilmesi Hakkında Karar (Karar Sayısı: 11679)</a>
        <a href="/eskiler/2026/08/20260829-3.pdf">Sınırları Gösterilen Alanın İkinci Derece Kara Askeri Yasak Bölge İlan Edilmesi Hakkında Karar (Karar Sayısı: 11680)</a>
    </body>
    </html>
    """
    index = parse_gazette_index(mock_html, "2026-08-29")
    assert index.gazette_number == "33355"
    assert len(index.items) == 2
    assert "Milli Savunma Üniversitesi" in index.items[0].title
    assert index.items[0].is_pdf is True
    assert "33355" in (index.items[0].location_breadcrumb or "")


def test_scoring_high_relevance_defense():
    profile = load_company_profile("config/company_profile.yaml")
    item = GazetteItem(
        title="Sınırları Gösterilen Alanın “Milli Savunma Üniversitesi Teknoloji Geliştirme Bölgesi” Olarak Tespit Edilmesi Hakkında Karar",
        url="https://resmigazete.gov.tr/sample",
        category="Cumhurbaşkanı Kararı",
    )
    score, reasons, risk, domain, badge = score_item_relevance(item, profile)
    assert score >= 70
    assert risk == "Kritik"
    assert any("Ar-Ge" in r or "Milli Savunma" in r or "Savunma" in r for r in reasons)


def test_scoring_unrelated_item():
    profile = load_company_profile("config/company_profile.yaml")
    item = GazetteItem(
        title="Özel Hastaneler Yönetmeliğinde Değişiklik Yapılmasına Dair Yönetmelik",
        url="https://resmigazete.gov.tr/sample2",
        category="Yönetmelik",
        institution="Sağlık Bakanlığı",
    )
    score, reasons, risk, domain, badge = score_item_relevance(item, profile)
    assert score == 0
    assert risk == "Bilgi"


def test_affected_departments_inference_defense():
    deps = infer_affected_departments("Milli Savunma Üniversitesi Askeri Teknoloji ve İHA Kararı", [])
    assert "Savunma Projeleri Yönetimi" in deps
    assert "Ar-Ge & Teknoloji Yönetimi" in deps

    deps_security = infer_affected_departments("İkinci Derece Kara Askeri Yasak Bölge İlanı", [])
    assert "Tesis Güvenlik Koordinatörlüğü" in deps_security


def test_checklist_generation():
    checklist = generate_action_checklist("Katma Değer Vergisi Tebliği", "Tebliğ", "Yüksek", "VERGİ & MALİYE")
    assert len(checklist) > 0
    assert any("ERP" in c or "parametre" in c or "YMM" in c for c in checklist)


def test_templates_rendering():
    profile = load_company_profile("config/company_profile.yaml")
    item = GazetteItem(
        title="Milli Savunma Üniversitesi Teknoloji Geliştirme Bölgesi Kararı",
        url="https://resmigazete.gov.tr/msu",
        category="Karar",
        location_breadcrumb="2026-08-29 Resmî Gazete > Yürütme ve İdare > Cumhurbaşkanı Kararları",
    )
    evaluation = evaluate_gazette_item(item, profile)
    from src.models import DailyAuditReport
    report = DailyAuditReport(
        date="2026-08-29",
        company_name=profile.general.name,
        total_scanned=13,
        relevant_count=1,
        evaluations=[evaluation],
        generated_at="2026-08-29 12:00:00",
    )

    md = format_markdown_report(report)
    assert "Resmî Gazete İç Denetim & Uyum Bülteni" in md
    assert "Milli Savunma Üniversitesi" in md
    assert "Resmî Gazete Konumu" in md

    html = format_html_report(report)
    assert "<!DOCTYPE html>" in html
    assert "STM Savunma" in html


def test_web_api_endpoints():
    from fastapi.testclient import TestClient
    from src.web_app import app

    client = TestClient(app)

    # 1. Profile Endpoint
    resp = client.get("/api/profile")
    assert resp.status_code == 200
    data = resp.json()
    assert "general" in data
    assert "STM" in data["general"]["name"]

    # 2. Index Page HTML
    html_resp = client.get("/")
    assert html_resp.status_code == 200
    assert "Resmî Gazete" in html_resp.text


def test_llm_config_endpoints():
    from fastapi.testclient import TestClient
    from src.web_app import app

    client = TestClient(app)
    resp = client.get("/api/llm-config")
    assert resp.status_code == 200
    data = resp.json()
    assert "config" in data
    assert "mcp_snippet" in data

    # Test update LLM
    update_resp = client.post("/api/llm-config", json={
        "active_provider": "openai",
        "model_name": "gpt-4o",
        "api_key": "sk-test123"
    })
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "success"

    # Reset back to rule_based
    client.post("/api/llm-config", json={"active_provider": "rule_based"})


def test_advanced_rule_based_negative_filtering():
    """Verifies that academic/student university regulations are suppressed (score 0)."""
    profile = load_company_profile("config/company_profile.yaml")
    
    # Academic/student regulation with 'Milli Savunma'
    item_academic = GazetteItem(
        title="Milli Savunma Üniversitesi Lisansüstü Eğitim-Öğretim ve Sınav Yönetmeliği",
        url="https://resmigazete.gov.tr/sample3",
        category="Yönetmelik",
        institution="Milli Savunma Üniversitesi",
    )
    score, _, risk, _, _ = score_item_relevance(item_academic, profile)
    assert score == 0
    assert risk == "Bilgi"

    # Substring trap: 'cihaz' contains 'iha'
    item_medical = GazetteItem(
        title="Tıbbi Cihaz Satış ve Tanıtım Yönetmeliğinde Değişiklik",
        url="https://resmigazete.gov.tr/sample4",
        category="Yönetmelik",
        institution="Sağlık Bakanlığı",
    )
    score_med, _, risk_med, _, _ = score_item_relevance(item_medical, profile)
    assert score_med == 0
    assert risk_med == "Bilgi"

    # Genuine defense UAV procurement
    item_uav = GazetteItem(
        title="Milli Savunma Bakanlığı Taktik İHA ve Askeri Yazılım Tedarik Tebliği",
        url="https://resmigazete.gov.tr/sample5",
        category="Tebliğ",
        institution="Milli Savunma Bakanlığı",
    )
    score_uav, _, risk_uav, _, _ = score_item_relevance(item_uav, profile)
    assert score_uav >= 70
    assert risk_uav == "Kritik"


def test_horizontal_corporate_compliance():
    """Verifies that corporate horizontal regulations (Tax, Labor/HR, KVKK, Tenders) are captured."""
    profile = load_company_profile("config/company_profile.yaml")

    # 1. Tax & Finance
    item_tax = GazetteItem(
        title="Katma Değer Vergisi Genel Uygulama Tebliğinde Değişiklik Yapılmasına Dair Tebliğ (Seri No: 52)",
        url="https://resmigazete.gov.tr/tax",
        category="Tebliğ",
        institution="Hazine ve Maliye Bakanlığı",
    )
    score_tax, _, risk_tax, domain_tax, badge_tax = score_item_relevance(item_tax, profile)
    assert score_tax >= 50
    assert badge_tax == "VERGİ & MALİYE"

    # 2. Labor & HR (Minimum Wage)
    item_hr = GazetteItem(
        title="Asgari Ücret Tespit Komisyonu Kararı",
        url="https://resmigazete.gov.tr/hr",
        category="Tebliğ",
        institution="Çalışma ve Sosyal Güvenlik Bakanlığı",
    )
    score_hr, _, risk_hr, domain_hr, badge_hr = score_item_relevance(item_hr, profile)
    assert score_hr >= 50
    assert badge_hr == "İŞ HUKUKU & İK"

    # 3. KVKK & Data Privacy
    item_kvkk = GazetteItem(
        title="Kişisel Verilerin Yurt Dışına Aktarılmasına İlişkin Usul ve Esaslar Hakkında Yönetmelik",
        url="https://resmigazete.gov.tr/kvkk",
        category="Yönetmelik",
        institution="Kişisel Verileri Koruma Kurumu",
    )
    score_kvkk, _, risk_kvkk, domain_kvkk, badge_kvkk = score_item_relevance(item_kvkk, profile)
    assert score_kvkk >= 50
    assert badge_kvkk == "KVKK & SİBER"


def test_sector_presets_api():
    from fastapi.testclient import TestClient
    from src.web_app import app
    from src.sector_templates import get_preset_list, get_preset_data

    client = TestClient(app)
    
    # 1. Presets List Endpoint
    r1 = client.get("/api/presets")
    assert r1.status_code == 200
    presets = r1.json()
    assert len(presets) >= 4
    keys = [p["key"] for p in presets]
    assert "defense_aerospace" in keys
    assert "fintech_banking" in keys
    assert "ecommerce_retail" in keys

    # 2. Preset Detail Endpoint
    r2 = client.get("/api/presets/fintech_banking")
    assert r2.status_code == 200
    pdata = r2.json()
    assert "6493" in pdata["high_priority_keywords"]
    assert "BDDK" in str(pdata["regulatory_bodies"])


def test_deep_content_and_company_impact_analysis():
    """Verifies that decision text is analyzed against company profile with specific impact."""
    profile = load_company_profile("config/company_profile.yaml")
    
    mock_pdf_text = """
    CUMHURBAŞKANI KARARI (Karar Sayısı: 11679)
    MADDE 1- Ankara İli sınırları içerisinde yer alan alanın Milli Savunma Üniversitesi Teknoloji Geliştirme Bölgesi olarak tespit edilmesine karar verilmiştir.
    MADDE 2- Bu Karar yayımı tarihinde yürürlüğe girer.
    """
    
    item = GazetteItem(
        title="Milli Savunma Üniversitesi Teknoloji Geliştirme Bölgesi Kararı",
        url="https://resmigazete.gov.tr/sample_pdf.pdf",
        category="Cumhurbaşkanı Kararı",
        is_pdf=True,
    )
    
    evaluation = evaluate_gazette_item(item, profile, content=mock_pdf_text)
    
    assert evaluation.company_specific_impact is not None
    assert "STM" in evaluation.company_specific_impact or "şirketimiz" in evaluation.company_specific_impact.lower()
    assert evaluation.key_articles_summary is not None
    assert "MADDE 1" in evaluation.key_articles_summary
    assert "yayımı tarihinde" in evaluation.compliance_deadlines.lower()


def test_multi_sector_merge_and_evaluation():
    """Verifies hybrid multi-sector aggregation and evaluation (Defense + FinTech + Software + E-Commerce)."""
    from fastapi.testclient import TestClient
    from src.web_app import app

    client = TestClient(app)

    # 1. Test POST /api/presets/merge endpoint
    merge_resp = client.post("/api/presets/merge", json={
        "preset_keys": ["defense_aerospace", "fintech_banking", "software_saas", "ecommerce_retail"]
    })
    assert merge_resp.status_code == 200
    merged = merge_resp.json()

    assert "Savunma" in merged["primary_sector"]
    assert "Finans" in merged["primary_sector"] or "FinTech" in merged["primary_sector"]
    assert "Bilgisayar" in merged["primary_sector"] or "SaaS" in merged["primary_sector"] or "Yazılım" in merged["primary_sector"]
    assert "Ticaret" in merged["primary_sector"] or "E-Ticaret" in merged["primary_sector"]
    
    # NACE codes from multiple sectors merged
    assert any("30.30" in c for c in merged["nace_codes"])
    assert any("64.19" in c for c in merged["nace_codes"])
    assert any("62.01" in c for c in merged["nace_codes"])
    assert any("47.91" in c for c in merged["nace_codes"])

    # Regulatory bodies merged
    assert any("BDDK" in reg for reg in merged["regulatory_bodies"])
    assert any("SSB" in reg for reg in merged["regulatory_bodies"])

    # High priority keywords merged
    assert any("6493" in kw for kw in merged["high_priority_keywords"])
    assert any("milgem" in kw for kw in merged["high_priority_keywords"])
    assert any("5746" in kw for kw in merged["high_priority_keywords"])

    # Conflict resolution in negative keywords (no active sector term should be excluded as a standalone term)
    assert "savunma" not in merged["excluded_keywords"]
    assert "ödeme" not in merged["excluded_keywords"]
    # Noise exclusion remains intact
    assert "tez savunma" in merged["excluded_keywords"]
