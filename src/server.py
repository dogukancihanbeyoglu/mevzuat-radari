"""
Model Context Protocol (MCP) Server for Mevzuat Radarı.
Provides interactive tools and resources for AI Agents (Antigravity, Claude Desktop, Cursor, etc.).
"""
import os
import sys
import json
from typing import Optional, Dict, Any, List

# Ensure project src is in path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from mcp.server.mcpserver import MCPServer
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP as MCPServer
    except ImportError:
        raise ImportError("mcp paketi bulunamadı. Lütfen 'pip install mcp' komutunu çalıştırın.")

from src.models import GazetteItem
from src.scraper import fetch_gazette_index, fetch_regulation_content
from src.evaluator import (
    load_company_profile,
    score_item_relevance,
    evaluate_gazette_item,
    generate_daily_audit_report,
)
from src.templates import format_markdown_report
from src.pdf_generator import generate_pdf_report
from src.notifier import dispatch_daily_audit_pdf, EmailNotifier


# Initialize MCP Server
app = MCPServer(
    name="mevzuat-radari",
    description="Resmî Gazete İç Denetim, Mevzuat ve Uyum Takip Radarı MCP Sunucusu",
)


@app.tool()
def get_company_profile() -> Dict[str, Any]:
    """
    Şirketin kayıtlı uyum ve iç denetim profilini döner.
    Profil: Sektörler, NACE kodları, tabi olunan düzenleyici kurumlar, ciro ölçeği ve risk öncelikleri.
    """
    profile = load_company_profile()
    return profile.model_dump()


@app.tool()
def fetch_gazette_fihrist(date: str = "") -> Dict[str, Any]:
    """
    Belirtilen günün (veya bugünün) Resmî Gazete fihristini yapılandırılmış liste olarak çeker.
    Parametre:
        date: 'YYYY-MM-DD' veya 'DD.MM.YYYY' formatında tarih. Boş bırakılırsa bugünün sayısı çekilir.
    """
    target_date = date.strip() if date and date.strip() else None
    index = fetch_gazette_index(target_date)
    return index.model_dump()


@app.tool()
def read_regulation_text(url: str) -> str:
    """
    Resmî Gazete'de yayımlanan bir kararın, yönetmeliğin veya tebliğin tam metnini temizlenmiş olarak getirir.
    Parametre:
        url: Belgenin Resmî Gazete bağlantı adresi (.htm veya .pdf).
    """
    return fetch_regulation_content(url)


@app.tool()
def evaluate_daily_gazette(date: str = "", min_relevance_score: int = 30) -> str:
    """
    Günün (veya verilen tarihin) Resmî Gazetesini şirket profiliyle eşleştirir, 
    risk ve etki analizi yaparak eksiksiz bir İç Denetim & Uyum Bülteni (Markdown) üretir.
    """
    target_date = date.strip() if date and date.strip() else None
    report = generate_daily_audit_report(date_str=target_date, min_score=min_relevance_score)
    return format_markdown_report(report)


@app.tool()
def generate_audit_pdf(date: str = "", min_relevance_score: int = 30) -> Dict[str, Any]:
    """
    Günün (veya verilen tarihin) iç denetim değerlendirmesini kurumsal PDF bülteni olarak üretir ve dosya yolunu döner.
    """
    target_date = date.strip() if date and date.strip() else None
    report = generate_daily_audit_report(date_str=target_date, min_score=min_relevance_score)
    
    reports_dir = os.path.join(project_root, "reports")
    clean_date = report.date.replace("/", "-").replace(".", "-")
    pdf_path = os.path.join(reports_dir, f"{clean_date}.pdf")
    
    saved_path = generate_pdf_report(report, pdf_path)
    return {
        "status": "success",
        "date": report.date,
        "company_name": report.company_name,
        "relevant_items": report.relevant_count,
        "pdf_path": saved_path,
        "pdf_size_bytes": os.path.getsize(saved_path),
    }


@app.tool()
def send_audit_report_pdf(recipients: List[str], date: str = "", min_relevance_score: int = 30) -> Dict[str, Any]:
    """
    İç Denetim & Uyum bültenini PDF ekiyle birlikte belirtilen e-posta adreslerine raporlar.
    Parametreler:
        recipients: E-posta adresleri listesi (örn: ["denetim@sirket.com", "uyum@sirket.com"])
        date: Tarih (YYYY-MM-DD)
        min_relevance_score: Minimum alaka eşiği (varsayılan 30)
    """
    target_date = date.strip() if date and date.strip() else None
    return dispatch_daily_audit_pdf(
        recipient_emails=recipients,
        date_str=target_date,
        min_score=min_relevance_score,
    )


@app.tool()
def test_regulation_relevance(title: str, category: str = "Tebliğ", institution: str = "") -> Dict[str, Any]:
    """
    Verilen bir mevzuat başlığını şirket profiliyle eşleştirerek alaka skorunu, risk derecesini ve etkilenen departmanları test eder.
    """
    profile = load_company_profile()
    item = GazetteItem(
        title=title,
        url="https://www.resmigazete.gov.tr/ornek",
        category=category,
        institution=institution if institution else None,
    )
    score, reasons, risk = score_item_relevance(item, profile)
    ev = evaluate_gazette_item(item, profile)
    return {
        "title": title,
        "relevance_score": score,
        "risk_level": risk,
        "matched_reasons": reasons,
        "affected_departments": ev.affected_departments,
        "action_checklist": ev.action_checklist,
    }


def run_server():
    """Starts the stdio MCP server."""
    app.run()


if __name__ == "__main__":
    run_server()
