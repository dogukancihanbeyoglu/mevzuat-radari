"""
Unit and Integration Tests for Mevzuat Radarı (STM Savunma A.Ş. Profile).
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
    score, reasons, risk = score_item_relevance(item, profile)
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
    score, reasons, risk = score_item_relevance(item, profile)
    assert score == 0
    assert risk == "Bilgi"


def test_affected_departments_inference_defense():
    deps = infer_affected_departments("Milli Savunma Üniversitesi Askeri Teknoloji ve İHA Kararı", [])
    assert "Savunma Projeleri Yönetimi" in deps
    assert "Ar-Ge & Teknoloji Yönetimi" in deps

    deps_security = infer_affected_departments("İkinci Derece Kara Askeri Yasak Bölge İlanı", [])
    assert "Tesis Güvenlik Koordinatörlüğü" in deps_security


def test_checklist_generation():
    checklist = generate_action_checklist("Katma Değer Vergisi Tebliği", "Tebliğ", "Yüksek")
    assert len(checklist) > 0
    assert any("ERP" in c or "parametre" in c for c in checklist)


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
    score, _, risk = score_item_relevance(item_academic, profile)
    assert score == 0
    assert risk == "Bilgi"

    # Substring trap: 'cihaz' contains 'iha'
    item_medical = GazetteItem(
        title="Tıbbi Cihaz Satış ve Tanıtım Yönetmeliğinde Değişiklik",
        url="https://resmigazete.gov.tr/sample4",
        category="Yönetmelik",
        institution="Sağlık Bakanlığı",
    )
    score_med, _, risk_med = score_item_relevance(item_medical, profile)
    assert score_med == 0
    assert risk_med == "Bilgi"

    # Genuine defense UAV procurement
    item_uav = GazetteItem(
        title="Milli Savunma Bakanlığı Taktik İHA ve Askeri Yazılım Tedarik Tebliği",
        url="https://resmigazete.gov.tr/sample5",
        category="Tebliğ",
        institution="Milli Savunma Bakanlığı",
    )
    score_uav, _, risk_uav = score_item_relevance(item_uav, profile)
    assert score_uav >= 70
    assert risk_uav == "Kritik"


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
