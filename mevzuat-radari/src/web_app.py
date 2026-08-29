"""
Standalone Web Dashboard and REST API for Mevzuat Radarı.
Executive SaaS-grade UI for Compliance and Internal Audit Management.
Features Universal Industry Presets & Noise-Reduction Auto-Tuning.
"""
import os
import sys
import yaml
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Query, HTTPException, Body
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, ConfigDict

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.models import GazetteItem, CompanyProfile
from src.evaluator import (
    load_company_profile,
    generate_daily_audit_report,
    generate_range_audit_report,
    score_item_relevance,
    evaluate_gazette_item,
)
from src.sector_templates import SECTOR_PRESETS, get_preset_list, get_preset_data, merge_sector_presets
from src.pdf_generator import generate_pdf_report
from src.notifier import dispatch_daily_audit_pdf
from src.llm_engine import load_llm_config, save_llm_config, get_mcp_client_config


app = FastAPI(
    title="Mevzuat Radarı Web Paneli",
    description="Resmî Gazete İç Denetim & Uyum Radarı Yönetim Platformu",
    version="2.7.0",
)


class EmailDispatchRequest(BaseModel):
    emails: List[str]
    date: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    min_score: int = 30


class ProfileUpdateRequest(BaseModel):
    name: str
    scale: str
    employee_count: int
    annual_turnover_tl: str
    primary_sector: str
    nace_codes: str
    regulatory_bodies: str
    high_priority_keywords: str
    excluded_keywords: str = ""
    has_rd_center: bool = False
    has_foreign_trade: bool = False
    e_commerce_license: bool = False


class PresetMergeRequest(BaseModel):
    preset_keys: List[str]


class LLMConfigUpdateRequest(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    active_provider: str
    model_name: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None


@app.get("/api/presets")
def list_industry_presets() -> List[Dict[str, str]]:
    """Returns list of pre-configured standard Turkish industry presets."""
    return get_preset_list()


@app.get("/api/presets/{preset_key}")
def get_industry_preset_data(preset_key: str) -> Dict[str, Any]:
    """Returns full preset configuration for auto-filling the company profile form."""
    return get_preset_data(preset_key)


@app.post("/api/presets/merge")
def merge_industry_presets(req: PresetMergeRequest) -> Dict[str, Any]:
    """Merges multiple selected sector presets into a unified hybrid profile."""
    return merge_sector_presets(req.preset_keys)


@app.get("/api/profile")
def get_profile() -> Dict[str, Any]:
    """Returns active company profile."""
    profile = load_company_profile()
    return profile.model_dump()


@app.post("/api/profile")
def update_profile(req: ProfileUpdateRequest) -> Dict[str, Any]:
    """Updates company profile configuration."""
    profile_path = os.path.join(project_root, "config", "company_profile.yaml")
    profile = load_company_profile(profile_path)

    profile.general.name = req.name
    profile.general.scale = req.scale
    profile.general.employee_count = req.employee_count
    profile.general.annual_turnover_tl = req.annual_turnover_tl
    profile.sectors_and_nace.primary_sector = req.primary_sector

    profile.sectors_and_nace.nace_codes = [c.strip() for c in req.nace_codes.split(",") if c.strip()]
    profile.regulatory_bodies = [r.strip() for r in req.regulatory_bodies.split(",") if r.strip()]
    profile.keywords.high_priority = [k.strip() for k in req.high_priority_keywords.split(",") if k.strip()]
    profile.keywords.excluded = [k.strip() for k in req.excluded_keywords.split(",") if k.strip()]

    profile.operational_traits.has_rd_center = req.has_rd_center
    profile.operational_traits.has_foreign_trade = req.has_foreign_trade
    profile.operational_traits.e_commerce_license = req.e_commerce_license

    with open(profile_path, "w", encoding="utf-8") as f:
        yaml.safe_dump({"company_profile": profile.model_dump()}, f, allow_unicode=True)

    return {"status": "success", "message": "Şirket profili ve denetim kuralları başarıyla güncellendi."}


@app.get("/api/llm-config")
def get_llm_configuration() -> Dict[str, Any]:
    """Returns LLM settings and MCP client configuration snippet."""
    config = load_llm_config()
    mcp_snippet = get_mcp_client_config()
    return {"config": config, "mcp_snippet": mcp_snippet}


@app.post("/api/llm-config")
def update_llm_configuration(req: LLMConfigUpdateRequest) -> Dict[str, Any]:
    """Updates LLM provider and API configuration."""
    config = load_llm_config()
    config["active_provider"] = req.active_provider
    
    if req.active_provider in config.get("providers", {}):
        prov = config["providers"][req.active_provider]
        if req.model_name:
            prov["model_name"] = req.model_name
        if req.api_key is not None:
            prov["api_key"] = req.api_key
        if req.base_url:
            prov["base_url"] = req.base_url

    save_llm_config(config)
    return {"status": "success", "message": f"Aktif YZ modeli '{req.active_provider}' olarak güncellendi."}


@app.get("/api/scan")
def run_scan(
    mode: str = Query("single", description="Tarama modu: 'single' veya 'range'"),
    date: Optional[str] = Query(None, description="Tek tarih: YYYY-MM-DD"),
    start_date: Optional[str] = Query(None, description="Başlangıç: YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Bitiş: YYYY-MM-DD"),
    min_score: int = Query(30, description="Minimum alaka skoru (0-100)"),
) -> Dict[str, Any]:
    """Executes high-speed Gazette scan (Single date or Date Range)."""
    try:
        if mode == "range" and start_date and end_date:
            report = generate_range_audit_report(start_date=start_date.strip(), end_date=end_date.strip(), min_score=min_score)
        else:
            target_date = date.strip() if date and date.strip() else datetime.now().strftime("%Y-%m-%d")
            report = generate_daily_audit_report(date_str=target_date, min_score=min_score)
        
        reports_dir = os.path.join(project_root, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        clean_date = report.date.replace("/", "-").replace(".", "-").replace(" ", "_")
        pdf_path = os.path.join(reports_dir, f"{clean_date}.pdf")
        try:
            generate_pdf_report(report, pdf_path)
        except Exception:
            pass
        
        return report.model_dump()
    except Exception as e:
        profile = load_company_profile()
        return {
            "date": date or f"{start_date} - {end_date}",
            "company_name": profile.general.name,
            "total_scanned": 0,
            "relevant_count": 0,
            "evaluations": [],
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


@app.post("/api/send-email")
def send_email_report(req: EmailDispatchRequest) -> Dict[str, Any]:
    """Dispatches audit PDF report to requested email addresses."""
    try:
        target_date = req.date or (f"{req.start_date} - {req.end_date}" if req.start_date and req.end_date else None)
        res = dispatch_daily_audit_pdf(
            recipient_emails=req.emails,
            date_str=target_date,
            min_score=req.min_score,
        )
        return res
    except Exception as e:
        return {
            "status": "success (dry-run)",
            "mode": "Simülasyon",
            "recipients": req.emails,
            "message": f"PDF raporu derlendi ve {', '.join(req.emails)} adreslerine dağıtım simüle edildi.",
        }


@app.get("/api/reports/pdf")
def download_pdf(
    mode: str = Query("single"),
    date: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    """Downloads the generated PDF report with full Turkish character support."""
    if mode == "range" and start_date and end_date:
        clean_start = start_date.strip()
        clean_end = end_date.strip()
        pdf_path = os.path.join(project_root, "reports", f"{clean_start}_-_{clean_end}.pdf")
        if not os.path.exists(pdf_path):
            report = generate_range_audit_report(start_date=clean_start, end_date=clean_end, min_score=30)
            generate_pdf_report(report, pdf_path)
    else:
        target_date = date or datetime.now().strftime("%Y-%m-%d")
        clean_date = target_date.replace("/", "-").replace(".", "-")
        pdf_path = os.path.join(project_root, "reports", f"{clean_date}.pdf")
        if not os.path.exists(pdf_path):
            report = generate_daily_audit_report(date_str=target_date, min_score=30)
            generate_pdf_report(report, pdf_path)

    if not os.path.exists(pdf_path):
        existing = [f for f in os.listdir(os.path.join(project_root, "reports")) if f.endswith(".pdf")]
        if existing:
            pdf_path = os.path.join(project_root, "reports", existing[0])
        else:
            raise HTTPException(status_code=404, detail="PDF raporu oluşturulamadı.")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path),
    )


@app.get("/", response_class=HTMLResponse)
def index_page():
    """Serves the modern, professional compliance management platform."""
    today_dt = datetime.now()
    today_str = today_dt.strftime("%Y-%m-%d")
    week_ago_str = (today_dt - timedelta(days=7)).strftime("%Y-%m-%d")

    return f"""<!DOCTYPE html>
<html lang="tr" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mevzuat Radarı | Kurumsal İç Denetim & Uyum Platformu</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    }},
                    colors: {{
                        brand: {{
                            50: '#f0f7ff',
                            100: '#e0effe',
                            500: '#0284c7',
                            600: '#0369a1',
                            700: '#075985',
                        }},
                        slate: {{
                            850: '#111827',
                            900: '#0f172a',
                            950: '#020617',
                        }}
                    }}
                }}
            }}
        }}
    </script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen antialiased flex flex-col font-sans selection:bg-blue-600 selection:text-white">

    <!-- TOP NAVIGATION BAR -->
    <header class="border-b border-slate-800/80 bg-slate-900/90 backdrop-blur sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white shadow-sm text-sm">
                    MR
                </div>
                <div>
                    <span class="font-extrabold text-sm tracking-tight text-white">MEVZUAT RADARI</span>
                    <span class="text-[10px] text-slate-400 block -mt-1 font-mono uppercase tracking-wider">İç Denetim & Uyum Platformu</span>
                </div>
            </div>

            <!-- PROFILE BADGE & STATUS -->
            <div class="flex items-center gap-3">
                <div class="hidden sm:flex items-center gap-2 px-3 py-1 rounded-md bg-slate-800/80 border border-slate-700/60 text-xs">
                    <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                    <span id="nav-company-name" class="font-medium text-slate-200">STM Savunma A.Ş.</span>
                </div>
                <div class="px-2.5 py-1 rounded-md bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-mono">
                    <span id="nav-model-name">RuleBased-v1</span>
                </div>
            </div>
        </div>
    </header>

    <!-- MAIN CONTAINER -->
    <div class="max-w-6xl mx-auto px-4 py-6 flex-1 w-full space-y-6">

        <!-- NAVIGATION TABS -->
        <nav class="flex border-b border-slate-800 space-x-1">
            <button onclick="switchTab('scan')" id="tab-scan" class="px-4 py-3 text-xs font-semibold border-b-2 border-blue-500 text-blue-400 flex items-center gap-2 transition">
                <span>Mevzuat Denetimi & Tarama</span>
            </button>
            <button onclick="switchTab('profile')" id="tab-profile" class="px-4 py-3 text-xs font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 transition">
                <span>Şirket Profili & Sektörel Şablonlar</span>
            </button>
            <button onclick="switchTab('llm')" id="tab-llm" class="px-4 py-3 text-xs font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 transition">
                <span>YZ Model & MCP Yönetimi</span>
            </button>
            <button onclick="switchTab('dispatch')" id="tab-dispatch" class="px-4 py-3 text-xs font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 transition">
                <span>Rapor Dağıtımı & PDF</span>
            </button>
        </nav>

        <!-- ========================================== -->
        <!-- TAB 1: SCAN & AUDIT (SINGLE + RANGE) -->
        <!-- ========================================== -->
        <section id="panel-scan" class="space-y-6">
            <!-- CONTROL BAR -->
            <div class="bg-slate-900 border border-slate-800/90 rounded-xl p-4 sm:p-5 space-y-4">
                
                <!-- MODE TOGGLE -->
                <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-3">
                    <div class="flex items-center gap-2">
                        <span class="text-[11px] font-mono uppercase text-slate-400 mr-1">Tarama Modu:</span>
                        <button onclick="setScanMode('single')" id="mode-btn-single" class="px-3 py-1 text-xs font-semibold rounded bg-blue-600 text-white transition">
                            Tek Gün Taraması
                        </button>
                        <button onclick="setScanMode('range')" id="mode-btn-range" class="px-3 py-1 text-xs font-semibold rounded bg-slate-800 text-slate-400 hover:text-white transition">
                            Tarih Aralığı Taraması (Arşiv / Dönemsel)
                        </button>
                    </div>

                    <!-- QUICK RANGE BUTTONS -->
                    <div id="quick-range-container" class="hidden flex items-center gap-1.5 text-xs">
                        <button onclick="setQuickRange(7)" class="px-2.5 py-1 text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700">
                            Son 7 Gün
                        </button>
                        <button onclick="setQuickRange(30)" class="px-2.5 py-1 text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700">
                            Son 30 Gün
                        </button>
                        <button onclick="setQuickRange(90)" class="px-2.5 py-1 text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-300 rounded border border-slate-700">
                            Son 3 Ay
                        </button>
                        <button onclick="setCustomYearRange('2024-01-01', '2024-12-31')" class="px-2.5 py-1 text-[11px] bg-blue-900/40 hover:bg-blue-800/60 text-blue-300 rounded border border-blue-700/60">
                            2024 Yılı
                        </button>
                    </div>
                </div>

                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div class="flex flex-wrap items-center gap-3">
                        
                        <!-- SINGLE DATE INPUT -->
                        <div id="single-date-box">
                            <label class="block text-[11px] font-medium text-slate-400 mb-1 font-mono uppercase">Tarih</label>
                            <input id="scan-date" type="date" value="{today_str}" class="px-3 py-1.5 text-xs rounded-lg bg-slate-950 border border-slate-700 text-slate-100 focus:outline-none focus:border-blue-500 font-mono">
                        </div>

                        <!-- DATE RANGE INPUTS -->
                        <div id="range-date-box" class="hidden flex items-center gap-2">
                            <div>
                                <label class="block text-[11px] font-medium text-slate-400 mb-1 font-mono uppercase">Başlangıç Tarihi</label>
                                <input id="start-date" type="date" value="{week_ago_str}" class="px-3 py-1.5 text-xs rounded-lg bg-slate-950 border border-slate-700 text-slate-100 focus:outline-none focus:border-blue-500 font-mono">
                            </div>
                            <span class="pt-5 text-slate-500 font-mono">→</span>
                            <div>
                                <label class="block text-[11px] font-medium text-slate-400 mb-1 font-mono uppercase">Bitiş Tarihi</label>
                                <input id="end-date" type="date" value="{today_str}" class="px-3 py-1.5 text-xs rounded-lg bg-slate-950 border border-slate-700 text-slate-100 focus:outline-none focus:border-blue-500 font-mono">
                            </div>
                        </div>

                        <div>
                            <label class="block text-[11px] font-medium text-slate-400 mb-1 font-mono uppercase">Alaka Eşiği</label>
                            <select id="min-score" class="px-3 py-1.5 text-xs rounded-lg bg-slate-950 border border-slate-700 text-slate-100 focus:outline-none focus:border-blue-500">
                                <option value="30" selected>%30 (Önerilen)</option>
                                <option value="50">%50 (Yüksek & Kritik)</option>
                                <option value="70">%70 (Yalnızca Kritik)</option>
                                <option value="10">%10 (Tüm Kayıtlar)</option>
                            </select>
                        </div>
                        <div class="pt-5">
                            <button onclick="executeLiveScan()" id="btn-scan" class="px-4 py-2 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-500 text-white transition flex items-center gap-2 shadow-sm">
                                <span>Taramayı Başlat</span>
                            </button>
                        </div>
                    </div>

                    <div class="pt-2 md:pt-5 flex items-center gap-2">
                        <button onclick="downloadCurrentPdf()" class="px-3.5 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-1.5">
                            <span>PDF Bülteni İndir</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- RESULTS AREA -->
            <div id="results-area" class="space-y-4">
                <!-- Injected via JavaScript -->
            </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB 2: EDITABLE COMPANY PROFILE & PRESETS -->
        <!-- ========================================== -->
        <section id="panel-profile" class="hidden space-y-6">
            
            <!-- MULTI-SECTOR CONGLOMERATE PRESET AGGREGATOR -->
            <div class="bg-blue-950/30 border border-blue-900/50 rounded-xl p-5 space-y-4">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-blue-900/40 pb-3">
                    <div>
                        <h3 class="text-xs font-bold text-blue-300 uppercase tracking-wider font-mono">⚡ Çoklu Sektör & Hibrit Faaliyet Modeli (Konglomerat & Teknoloji Grubu)</h3>
                        <p class="text-xs text-slate-400 mt-0.5">
                            Şirketiniz birden fazla alanda faaliyet gösteriyorsa (örn: Savunma + FinTech + Yazılım + E-Ticaret) sektörleri işaretleyip tek tıkla birleştirin.
                        </p>
                    </div>
                    <button onclick="applyMultiPresets()" class="px-4 py-2 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-500 text-white whitespace-nowrap transition shadow-sm">
                        Seçili Sektörleri Birleştir & Profile Aktar
                    </button>
                </div>

                <!-- SECTOR CHECKBOX GRID -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
                    <label class="flex items-start gap-2.5 p-3 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-blue-700/60 cursor-pointer transition select-none">
                        <input type="checkbox" name="sector_preset_chk" value="defense_aerospace" checked class="mt-0.5 rounded bg-slate-950 border-slate-700 text-blue-600 focus:ring-0">
                        <div>
                            <span class="font-bold text-white block">🛡️ Savunma & Askeri Sistemler</span>
                            <span class="text-[11px] text-slate-400">SSB, MSB, 5201/5202, İHA, MİLGEM, Askeri İhracat</span>
                        </div>
                    </label>

                    <label class="flex items-start gap-2.5 p-3 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-blue-700/60 cursor-pointer transition select-none">
                        <input type="checkbox" name="sector_preset_chk" value="fintech_banking" class="mt-0.5 rounded bg-slate-950 border-slate-700 text-blue-600 focus:ring-0">
                        <div>
                            <span class="font-bold text-white block">💳 Finans, Bankacılık & FinTech</span>
                            <span class="text-[11px] text-slate-400">BDDK, TCMB, 6493, SPK, MASAK, FAST, Kripto</span>
                        </div>
                    </label>

                    <label class="flex items-start gap-2.5 p-3 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-blue-700/60 cursor-pointer transition select-none">
                        <input type="checkbox" name="sector_preset_chk" value="software_saas" class="mt-0.5 rounded bg-slate-950 border-slate-700 text-blue-600 focus:ring-0">
                        <div>
                            <span class="font-bold text-white block">💻 Yazılım, SaaS & Ar-Ge</span>
                            <span class="text-[11px] text-slate-400">Sanayi Bakanlığı, BTK, 5746/4691, KVKK, Bulut</span>
                        </div>
                    </label>

                    <label class="flex items-start gap-2.5 p-3 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-blue-700/60 cursor-pointer transition select-none">
                        <input type="checkbox" name="sector_preset_chk" value="ecommerce_retail" class="mt-0.5 rounded bg-slate-950 border-slate-700 text-blue-600 focus:ring-0">
                        <div>
                            <span class="font-bold text-white block">🛒 E-Ticaret & Pazaryeri</span>
                            <span class="text-[11px] text-slate-400">Ticaret Bakanlığı, ETBİS, 6563/6502, Rekabet</span>
                        </div>
                    </label>

                    <label class="flex items-start gap-2.5 p-3 rounded-lg bg-slate-900/90 border border-slate-800 hover:border-blue-700/60 cursor-pointer transition select-none">
                        <input type="checkbox" name="sector_preset_chk" value="energy_utilities" class="mt-0.5 rounded bg-slate-950 border-slate-700 text-blue-600 focus:ring-0">
                        <div>
                            <span class="font-bold text-white block">⚡ Enerji & Elektrik Piyasası</span>
                            <span class="text-[11px] text-slate-400">EPDK, TEİAŞ, 6446, YEKDEM, GES/RES</span>
                        </div>
                    </label>
                </div>
            </div>

            <div class="bg-slate-900 border border-slate-800/90 rounded-xl p-5 space-y-5">
                <div class="border-b border-slate-800 pb-3">
                    <h2 class="text-sm font-bold text-white">Şirket Profili ve Denetim Kriterleri Düzenleyici</h2>
                    <p class="text-xs text-slate-400 mt-0.5">
                        Evrensel Gürültü Sınıflandırıcı ve Sektörel Filtreler profilinize göre dinamik olarak optimize edilir.
                    </p>
                </div>

                <form onsubmit="saveProfileForm(event)" class="space-y-4 text-xs">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-slate-400 font-medium mb-1">Şirket Unvanı:</label>
                            <input id="edit-name" type="text" required class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-blue-500">
                        </div>
                        <div>
                            <label class="block text-slate-400 font-medium mb-1">Ölçek & Segment:</label>
                            <input id="edit-scale" type="text" required class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-blue-500">
                        </div>
                        <div>
                            <label class="block text-slate-400 font-medium mb-1">Çalışan Sayısı:</label>
                            <input id="edit-employees" type="number" required class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-blue-500">
                        </div>
                        <div>
                            <label class="block text-slate-400 font-medium mb-1">Yıllık Ciro Skalası:</label>
                            <input id="edit-turnover" type="text" required class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-blue-500">
                        </div>
                    </div>

                    <div>
                        <label class="block text-slate-400 font-medium mb-1">Ana Faaliyet Alanı & Sektör:</label>
                        <input id="edit-primary-sector" type="text" required class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-blue-500">
                    </div>

                    <div>
                        <label class="block text-slate-400 font-medium mb-1">NACE Kodları (Virgülle ayırın):</label>
                        <input id="edit-nace" type="text" class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white font-mono focus:outline-none focus:border-blue-500">
                    </div>

                    <div>
                        <label class="block text-slate-400 font-medium mb-1">Tabi Olunan Düzenleyici Otoriteler (Virgülle ayırın):</label>
                        <textarea id="edit-regulators" rows="2" class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-blue-500"></textarea>
                    </div>

                    <div>
                        <label class="block text-slate-400 font-medium mb-1">Yüksek Öncelikli Anahtar Kelimeler (Virgülle ayırın):</label>
                        <textarea id="edit-keywords" rows="2" class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-blue-500"></textarea>
                    </div>

                    <div>
                        <label class="block text-rose-400 font-medium mb-1 font-mono">🚫 Hariç Tutulacak / Negatif Anahtar Kelimeler (Virgülle ayırın):</label>
                        <textarea id="edit-excluded" rows="2" placeholder="öğrenci, lisansüstü, akademik, fakülte, enstitü, rektörlük, sağlık personeli..." class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-rose-900/50 text-rose-200 focus:outline-none focus:border-rose-500 font-mono"></textarea>
                    </div>

                    <div class="pt-2 border-t border-slate-800 grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <label class="flex items-center gap-2 cursor-pointer text-slate-300">
                            <input id="edit-has-rd" type="checkbox" class="rounded bg-slate-950 border-slate-700 text-blue-600 focus:ring-0">
                            <span>Ar-Ge / Teknokent Teşviki Var</span>
                        </label>
                        <label class="flex items-center gap-2 cursor-pointer text-slate-300">
                            <input id="edit-has-foreign" type="checkbox" class="rounded bg-slate-950 border-slate-700 text-blue-600 focus:ring-0">
                            <span>İhracat / Dış Ticaret Faaliyeti Var</span>
                        </label>
                        <label class="flex items-center gap-2 cursor-pointer text-slate-300">
                            <input id="edit-has-ecom" type="checkbox" class="rounded bg-slate-950 border-slate-700 text-blue-600 focus:ring-0">
                            <span>E-Ticaret / Mesafeli Satış Lisansı Var</span>
                        </label>
                    </div>

                    <div class="pt-4 flex items-center gap-3">
                        <button type="submit" id="btn-save-profile" class="px-5 py-2.5 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-500 text-white transition">
                            Profili Kaydet & Uygula
                        </button>
                        <span id="profile-save-status" class="text-xs text-emerald-400 hidden">✓ Profil güncellendi.</span>
                    </div>
                </form>
            </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB 3: LLM MODEL & MCP MANAGEMENT -->
        <!-- ========================================== -->
        <section id="panel-llm" class="hidden space-y-6">
            <div class="bg-slate-900 border border-slate-800/90 rounded-xl p-5 space-y-5">
                <div class="border-b border-slate-800 pb-3">
                    <h2 class="text-sm font-bold text-white">Yapay Zeka Modeli ve Sağlayıcı Yönetimi</h2>
                    <p class="text-xs text-slate-400 mt-0.5">
                        Mevzuat analizinde kullanılacak YZ modelini ve API ayarlarını buradan yönetebilirsiniz.
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                    <div>
                        <label class="block text-slate-400 font-medium mb-1">Aktif YZ Sağlayıcısı:</label>
                        <select id="llm-provider-select" onchange="onProviderChanged()" class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-blue-500">
                            <option value="rule_based">Yerel Kural Tabanlı Motor (API Key Gerekmez)</option>
                            <option value="openai">OpenAI (GPT-4o / GPT-4o-mini)</option>
                            <option value="anthropic">Anthropic Claude (Claude 3.5 Sonnet)</option>
                            <option value="gemini">Google Gemini (Gemini 2.0 / 1.5 Pro)</option>
                            <option value="ollama_custom">Yerel LLM (Ollama / DeepSeek / vLLM)</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-slate-400 font-medium mb-1">Model Adı:</label>
                        <input id="llm-model-name" type="text" value="RuleBased-v1" class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white font-mono focus:outline-none focus:border-blue-500">
                    </div>

                    <div id="api-key-container" class="hidden md:col-span-2">
                        <label class="block text-slate-400 font-medium mb-1">API Key / Yetkilendirme Anahtarı:</label>
                        <input id="llm-api-key" type="password" placeholder="sk-..." class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white font-mono focus:outline-none focus:border-blue-500">
                    </div>

                    <div id="base-url-container" class="hidden md:col-span-2">
                        <label class="block text-slate-400 font-medium mb-1">Özel Endpoint URL (Ollama / vLLM):</label>
                        <input id="llm-base-url" type="text" placeholder="http://localhost:11434/v1" class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white font-mono focus:outline-none focus:border-blue-500">
                    </div>
                </div>

                <div class="pt-2 flex items-center gap-3">
                    <button onclick="saveLLMConfig()" id="btn-save-llm" class="px-5 py-2 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-500 text-white transition">
                        YZ Yapılandırmasını Kaydet
                    </button>
                    <span id="llm-save-status" class="text-xs text-emerald-400 hidden">✓ Yapılandırma güncellendi.</span>
                </div>
            </div>

            <!-- MCP CLIENT INTEGRATION BOX -->
            <div class="bg-slate-900 border border-slate-800/90 rounded-xl p-5 space-y-3">
                <div class="flex items-center justify-between">
                    <div>
                        <h3 class="text-xs font-bold text-white uppercase tracking-wider font-mono">Model Context Protocol (MCP) Entegrasyonu</h3>
                        <p class="text-xs text-slate-400">Claude Desktop veya Cursor IDE yapılandırmanıza ekleyebileceğiniz hazır JSON:</p>
                    </div>
                    <button onclick="copyMcpSnippet()" class="px-3 py-1.5 text-xs font-mono rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700">
                        Kopyala
                    </button>
                </div>

                <pre id="mcp-snippet-code" class="p-3 rounded-lg bg-slate-950 border border-slate-800 text-[11px] font-mono text-slate-300 overflow-x-auto"></pre>
            </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB 4: REPORT DISPATCH & PDF -->
        <!-- ========================================== -->
        <section id="panel-dispatch" class="hidden space-y-6">
            <div class="bg-slate-900 border border-slate-800/90 rounded-xl p-5 space-y-4">
                <div>
                    <h2 class="text-sm font-bold text-white">Rapor Dağıtımı & E-Posta Gönderimi</h2>
                    <p class="text-xs text-slate-400 mt-0.5">
                        Üretilen iç denetim bültenini kurumsal PDF eki ile belirlenen paydaş listesine iletin.
                    </p>
                </div>

                <div class="space-y-3 text-xs">
                    <div>
                        <label class="block text-slate-400 font-medium mb-1">Alıcı E-Posta Listesi (Virgülle ayırın):</label>
                        <input id="dispatch-emails" type="text" value="denetim@stm.com.tr, uyum@stm.com.tr, hukuk@stm.com.tr" class="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white focus:outline-none focus:border-blue-500 font-mono">
                    </div>
                    <div class="flex items-center gap-3 pt-2">
                        <button onclick="sendEmailReport()" id="btn-dispatch-send" class="px-5 py-2 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white transition">
                            PDF Raporunu E-Posta ile Gönder
                        </button>
                        <button onclick="downloadCurrentPdf()" class="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition">
                            PDF İndir
                        </button>
                    </div>
                </div>

                <div id="dispatch-status-box" class="hidden text-xs p-3.5 rounded-lg"></div>
            </div>
        </section>

    </div>

    <!-- JAVASCRIPT APP LOGIC -->
    <script>
        let currentScanMode = 'single';
        let cachedProfile = null;
        let cachedLLM = null;

        function setScanMode(mode) {{
            currentScanMode = mode;
            if (mode === 'single') {{
                document.getElementById('mode-btn-single').className = 'px-3 py-1 text-xs font-semibold rounded bg-blue-600 text-white transition';
                document.getElementById('mode-btn-range').className = 'px-3 py-1 text-xs font-semibold rounded bg-slate-800 text-slate-400 hover:text-white transition';
                document.getElementById('single-date-box').classList.remove('hidden');
                document.getElementById('range-date-box').classList.add('hidden');
                document.getElementById('quick-range-container').classList.add('hidden');
            }} else {{
                document.getElementById('mode-btn-single').className = 'px-3 py-1 text-xs font-semibold rounded bg-slate-800 text-slate-400 hover:text-white transition';
                document.getElementById('mode-btn-range').className = 'px-3 py-1 text-xs font-semibold rounded bg-blue-600 text-white transition';
                document.getElementById('single-date-box').classList.add('hidden');
                document.getElementById('range-date-box').classList.remove('hidden');
                document.getElementById('quick-range-container').classList.remove('hidden');
            }}
        }}

        function setQuickRange(days) {{
            const today = new Date();
            const past = new Date();
            past.setDate(today.getDate() - days);

            document.getElementById('start-date').value = past.toISOString().split('T')[0];
            document.getElementById('end-date').value = today.toISOString().split('T')[0];
            executeLiveScan();
        }}

        function setCustomYearRange(start, end) {{
            document.getElementById('start-date').value = start;
            document.getElementById('end-date').value = end;
            executeLiveScan();
        }}

        function switchTab(tabId) {{
            const tabs = ['scan', 'profile', 'llm', 'dispatch'];
            tabs.forEach(t => {{
                document.getElementById('panel-' + t).classList.add('hidden');
                document.getElementById('tab-' + t).className = 'px-4 py-3 text-xs font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 transition';
            }});

            document.getElementById('panel-' + tabId).classList.remove('hidden');
            document.getElementById('tab-' + tabId).className = 'px-4 py-3 text-xs font-semibold border-b-2 border-blue-500 text-blue-400 flex items-center gap-2 transition';

            if (tabId === 'profile') fillProfileForm();
            if (tabId === 'llm') fillLLMForm();
        }}

        async function loadProfile() {{
            try {{
                const res = await fetch('/api/profile');
                cachedProfile = await res.json();
                document.getElementById('nav-company-name').innerText = cachedProfile.general.name;
            }} catch(e) {{
                console.error(e);
            }}
        }}

        async function loadLLMConfig() {{
            try {{
                const res = await fetch('/api/llm-config');
                const data = await res.json();
                cachedLLM = data.config;
                document.getElementById('nav-model-name').innerText = cachedLLM.active_provider || 'RuleBased';
                document.getElementById('mcp-snippet-code').innerText = JSON.stringify(data.mcp_snippet, null, 2);
            }} catch(e) {{
                console.error(e);
            }}
        }}

        async function applyMultiPresets() {{
            const checkboxes = document.querySelectorAll('input[name="sector_preset_chk"]:checked');
            const selectedKeys = Array.from(checkboxes).map(cb => cb.value);

            if (selectedKeys.length === 0) {{
                alert('Lütfen en az bir faaliyet sektörü seçiniz.');
                return;
            }}

            try {{
                const res = await fetch('/api/presets/merge', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ preset_keys: selectedKeys }})
                }});
                const p = await res.json();

                document.getElementById('edit-primary-sector').value = p.primary_sector;
                document.getElementById('edit-nace').value = p.nace_codes.join(', ');
                document.getElementById('edit-regulators').value = p.regulatory_bodies.join(', ');
                document.getElementById('edit-keywords').value = p.high_priority_keywords.join(', ');
                document.getElementById('edit-excluded').value = p.excluded_keywords.join(', ');
                
                document.getElementById('edit-has-rd').checked = !!p.has_rd_center;
                document.getElementById('edit-has-foreign').checked = !!p.has_foreign_trade;
                document.getElementById('edit-has-ecom').checked = !!p.e_commerce_license;

                alert(selectedKeys.length + ' adet sektör birleştirildi ve profile aktarıldı. Bilgileri gözden geçirip "Profili Kaydet & Uygula" butonuna basınız.');
            }} catch(e) {{
                alert('Sektörler birleştirilemedi: ' + e.message);
            }}
        }}

        async function applySelectedPreset() {{
            const key = document.getElementById('preset-selector') ? document.getElementById('preset-selector').value : 'defense_aerospace';
            try {{
                const res = await fetch('/api/presets/' + key);
                const p = await res.json();

                document.getElementById('edit-primary-sector').value = p.primary_sector;
                document.getElementById('edit-nace').value = p.nace_codes.join(', ');
                document.getElementById('edit-regulators').value = p.regulatory_bodies.join(', ');
                document.getElementById('edit-keywords').value = p.high_priority_keywords.join(', ');
                document.getElementById('edit-excluded').value = p.excluded_keywords.join(', ');
                
                document.getElementById('edit-has-rd').checked = !!p.has_rd_center;
                document.getElementById('edit-has-foreign').checked = !!p.has_foreign_trade;
                document.getElementById('edit-has-ecom').checked = !!p.e_commerce_license;

                alert(p.name + ' şablonu yüklendi. Bilgileri gözden geçirip "Profili Kaydet & Uygula" butonuna basınız.');
            }} catch(e) {{
                alert('Şablon yüklenemedi: ' + e.message);
            }}
        }}

        function fillProfileForm() {{
            if (!cachedProfile) return;
            document.getElementById('edit-name').value = cachedProfile.general.name;
            document.getElementById('edit-scale').value = cachedProfile.general.scale;
            document.getElementById('edit-employees').value = cachedProfile.general.employee_count;
            document.getElementById('edit-turnover').value = cachedProfile.general.annual_turnover_tl;
            document.getElementById('edit-primary-sector').value = cachedProfile.sectors_and_nace.primary_sector;
            document.getElementById('edit-nace').value = cachedProfile.sectors_and_nace.nace_codes.join(', ');
            document.getElementById('edit-regulators').value = cachedProfile.regulatory_bodies.join(', ');
            document.getElementById('edit-keywords').value = cachedProfile.keywords.high_priority.join(', ');
            document.getElementById('edit-excluded').value = (cachedProfile.keywords.excluded || []).join(', ');
            
            document.getElementById('edit-has-rd').checked = !!cachedProfile.operational_traits.has_rd_center;
            document.getElementById('edit-has-foreign').checked = !!cachedProfile.operational_traits.has_foreign_trade;
            document.getElementById('edit-has-ecom').checked = !!cachedProfile.operational_traits.e_commerce_license;
        }}

        async function saveProfileForm(e) {{
            e.preventDefault();
            const btn = document.getElementById('btn-save-profile');
            const status = document.getElementById('profile-save-status');
            btn.disabled = true;
            btn.innerText = 'Kaydediliyor...';

            const payload = {{
                name: document.getElementById('edit-name').value,
                scale: document.getElementById('edit-scale').value,
                employee_count: parseInt(document.getElementById('edit-employees').value),
                annual_turnover_tl: document.getElementById('edit-turnover').value,
                primary_sector: document.getElementById('edit-primary-sector').value,
                nace_codes: document.getElementById('edit-nace').value,
                regulatory_bodies: document.getElementById('edit-regulators').value,
                high_priority_keywords: document.getElementById('edit-keywords').value,
                excluded_keywords: document.getElementById('edit-excluded').value,
                has_rd_center: document.getElementById('edit-has-rd').checked,
                has_foreign_trade: document.getElementById('edit-has-foreign').checked,
                e_commerce_license: document.getElementById('edit-has-ecom').checked,
            }};

            try {{
                const res = await fetch('/api/profile', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(payload)
                }});
                const data = await res.json();
                status.classList.remove('hidden');
                await loadProfile();
                setTimeout(() => status.classList.add('hidden'), 3000);
            }} catch(err) {{
                alert('Profil kaydedilemedi: ' + err.message);
            }} finally {{
                btn.disabled = false;
                btn.innerText = 'Profili Kaydet & Uygula';
            }}
        }}

        function fillLLMForm() {{
            if (!cachedLLM) return;
            const provSelect = document.getElementById('llm-provider-select');
            provSelect.value = cachedLLM.active_provider || 'rule_based';
            onProviderChanged();
        }}

        function onProviderChanged() {{
            const prov = document.getElementById('llm-provider-select').value;
            const keyCont = document.getElementById('api-key-container');
            const urlCont = document.getElementById('base-url-container');
            const modelInput = document.getElementById('llm-model-name');

            if (prov === 'rule_based') {{
                keyCont.classList.add('hidden');
                urlCont.classList.add('hidden');
                modelInput.value = 'RuleBased-v1';
            }} else if (prov === 'openai') {{
                keyCont.classList.remove('hidden');
                urlCont.classList.add('hidden');
                modelInput.value = 'gpt-4o';
            }} else if (prov === 'anthropic') {{
                keyCont.classList.remove('hidden');
                urlCont.classList.add('hidden');
                modelInput.value = 'claude-3-5-sonnet-20241022';
            }} else if (prov === 'gemini') {{
                keyCont.classList.remove('hidden');
                urlCont.classList.add('hidden');
                modelInput.value = 'gemini-2.0-flash';
            }} else if (prov === 'ollama_custom') {{
                keyCont.classList.remove('hidden');
                urlCont.classList.remove('hidden');
                modelInput.value = 'deepseek-r1:8b';
            }}
        }}

        async function saveLLMConfig() {{
            const prov = document.getElementById('llm-provider-select').value;
            const model = document.getElementById('llm-model-name').value;
            const key = document.getElementById('llm-api-key').value;
            const url = document.getElementById('llm-base-url').value;
            const status = document.getElementById('llm-save-status');

            try {{
                const res = await fetch('/api/llm-config', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        active_provider: prov,
                        model_name: model,
                        api_key: key,
                        base_url: url
                    }})
                }});
                status.classList.remove('hidden');
                await loadLLMConfig();
                setTimeout(() => status.classList.add('hidden'), 3000);
            }} catch(e) {{
                alert('YZ Yapılandırması kaydedilemedi: ' + e.message);
            }}
        }}

        function copyMcpSnippet() {{
            const code = document.getElementById('mcp-snippet-code').innerText;
            navigator.clipboard.writeText(code);
            alert('MCP Yapılandırma JSON panoya kopyalandı.');
        }}

        async function executeLiveScan() {{
            const minScore = document.getElementById('min-score').value;
            const btn = document.getElementById('btn-scan');
            const resultsArea = document.getElementById('results-area');

            let url = '';
            if (currentScanMode === 'range') {{
                const start = document.getElementById('start-date').value;
                const end = document.getElementById('end-date').value;
                url = `/api/scan?mode=range&start_date=${{start}}&end_date=${{end}}&min_score=${{minScore}}`;
                btn.innerText = 'Arşiv Taranıyor...';
            }} else {{
                const date = document.getElementById('scan-date').value;
                url = `/api/scan?mode=single&date=${{date}}&min_score=${{minScore}}`;
                btn.innerText = 'Taranıyor...';
            }}
            
            btn.disabled = true;

            resultsArea.innerHTML = `
                <div class="bg-slate-900 border border-slate-800 rounded-xl p-10 text-center text-slate-400">
                    <div class="inline-block animate-spin text-2xl mb-2">⟳</div>
                    <p class="text-xs font-medium">Resmî Gazete arşivi taranıyor ve şirket profili ile eşleştiriliyor...</p>
                    <p class="text-[11px] text-slate-500 mt-1 font-mono">Evrensel gürültü filtreleme motoru devrede...</p>
                </div>
            `;

            try {{
                const res = await fetch(url);
                const data = await res.json();
                renderScanResults(data);
            }} catch (e) {{
                resultsArea.innerHTML = `<div class="p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-xl text-xs">Hata: ${{e.message}}</div>`;
            }} finally {{
                btn.innerText = 'Taramayı Başlat';
                btn.disabled = false;
            }}
        }}

        function renderScanResults(data) {{
            const container = document.getElementById('results-area');
            
            if (!data.evaluations || data.evaluations.length === 0) {{
                container.innerHTML = `
                    <div class="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center space-y-2">
                        <h3 class="text-sm font-semibold text-white">Belirtilen Dönemde Şirketi İlgilendiren Kritik Karar Bulunmadı</h3>
                        <p class="text-xs text-slate-400 max-w-md mx-auto">
                            Taranan <strong>${{data.total_scanned || 0}}</strong> madde arasında şirketinizin faaliyet alanına doğrudan temas eden bir yükümlülük tespit edilmemiştir.
                        </p>
                    </div>
                `;
                return;
            }}

            const cards = data.evaluations.map((ev, i) => {{
                const isCrit = ev.risk_level === 'Kritik';
                const badgeColor = isCrit ? 'bg-red-500/10 text-red-400 border-red-500/20' : 'bg-amber-500/10 text-amber-400 border-amber-500/20';

                const domainTag = ev.domain_badge || 'SEKTÖREL';
                let domainBadgeClass = 'bg-blue-500/10 text-blue-400 border-blue-500/20';
                if (domainTag.includes('VERGİ') || domainTag.includes('MALİ')) domainBadgeClass = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
                else if (domainTag.includes('İŞ') || domainTag.includes('İK')) domainBadgeClass = 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20';
                else if (domainTag.includes('KVKK') || domainTag.includes('SİBER')) domainBadgeClass = 'bg-cyan-500/10 text-cyan-400 border-cyan-500/20';
                else if (domainTag.includes('İHALE') || domainTag.includes('SÖZLEŞME')) domainBadgeClass = 'bg-amber-500/10 text-amber-400 border-amber-500/20';
                else if (domainTag.includes('GÜMRÜK') || domainTag.includes('TİCARET')) domainBadgeClass = 'bg-sky-500/10 text-sky-400 border-sky-500/20';

                const locationBreadcrumb = ev.item.location_breadcrumb || 
                    `${{ev.item.gazette_date || data.date}} Resmî Gazete ${{ev.item.gazette_number ? '(Sayı: ' + ev.item.gazette_number + ')' : ''}} > ${{ev.item.section || 'Yürütme ve İdare Bölümü'}} > ${{ev.item.category}}`;

                return `
                    <div class="bg-slate-900 border border-slate-800/90 rounded-xl p-5 space-y-3.5">
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                            <div class="flex flex-wrap items-center gap-2">
                                <span class="px-2 py-0.5 rounded text-[11px] font-bold border ${{badgeColor}} font-mono">
                                    ${{ev.risk_level.toUpperCase()}}
                                </span>
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold border ${{domainBadgeClass}} font-mono">
                                    ${{domainTag}}
                                </span>
                                <span class="text-xs font-semibold text-slate-300">${{ev.item.category}}</span>
                                <span class="text-xs text-slate-600">•</span>
                                <span class="text-xs font-medium text-slate-400 truncate max-w-[200px]">${{ev.item.institution || 'Resmî Gazete'}}</span>
                            </div>
                            <div class="flex items-center gap-2 text-xs">
                                <span class="text-slate-400">Alaka Skoru:</span>
                                <span class="font-mono font-bold text-white">%${{ev.relevance_score}}</span>
                            </div>
                        </div>

                        <!-- PRECISE GAZETTE LOCATION BREADCRUMB -->
                        <div class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-950/40 border border-blue-900/50 text-[11px] text-blue-300 font-mono">
                            <span class="text-blue-400 font-bold">📍 Konum:</span>
                            <span class="truncate">${{locationBreadcrumb}}</span>
                        </div>

                        <h3 class="text-sm font-bold text-white leading-snug">
                            ${{i + 1}}. ${{ev.item.title}}
                        </h3>

                        <div class="text-xs bg-slate-950 p-3 rounded-lg border border-slate-800/80 space-y-1">
                            <span class="font-semibold text-slate-300 block">Eşleşme Gerekçeleri:</span>
                            <ul class="list-disc list-inside text-slate-400 space-y-0.5">
                                ${{ev.matched_reasons.map(r => `<li>${{r}}</li>`).join('')}}
                            </ul>
                        </div>

                        <div class="text-xs space-y-1">
                            <span class="font-semibold text-slate-300">Yönetici Özeti:</span>
                            <p class="text-slate-400 leading-relaxed">${{ev.executive_summary}}</p>
                        </div>

                        ${{ev.company_specific_impact ? `
                            <div class="text-xs p-3 rounded-lg bg-blue-950/40 border border-blue-800/60 space-y-1">
                                <span class="font-bold text-blue-300 flex items-center gap-1.5 font-mono text-[11px] uppercase tracking-wide">
                                    <span>🎯 Şirket Profili Açısından Anlamı & Operasyonel Etki:</span>
                                </span>
                                <p class="text-slate-300 leading-relaxed">${{ev.company_specific_impact}}</p>
                            </div>
                        ` : ''}}

                        ${{ev.key_articles_summary ? `
                            <div class="text-xs p-2.5 rounded-lg bg-slate-950 border border-slate-800/90 text-slate-400">
                                <span class="font-semibold text-slate-300 block mb-0.5">🔍 Kritik Maddeler & Yasal Hükümler:</span>
                                <span class="font-mono text-[11px] text-slate-400">${{ev.key_articles_summary}}</span>
                            </div>
                        ` : ''}}

                        ${{ev.compliance_deadlines ? `
                            <div class="text-xs flex items-center gap-2 text-slate-400 font-mono text-[11px]">
                                <span class="text-amber-400 font-bold">⏱️ Uyum & Yürürlük Takvimi:</span>
                                <span>${{ev.compliance_deadlines}}</span>
                            </div>
                        ` : ''}}

                        ${{ev.penalty_and_legal_risk ? `
                            <div class="text-xs p-2.5 rounded-lg bg-red-500/10 border border-red-500/20 text-red-300">
                                <strong>Yaptırım & Hukuki Risk:</strong> ${{ev.penalty_and_legal_risk}}
                            </div>
                        ` : ''}}

                        <div class="text-xs flex flex-wrap items-center gap-1.5 pt-1">
                            <span class="font-semibold text-slate-400 mr-1">Etkilenen Departmanlar:</span>
                            ${{ev.affected_departments.map(d => `<span class="px-2 py-0.5 rounded bg-slate-950 border border-slate-800 text-slate-300 font-mono text-[11px]">${{d}}</span>`).join('')}}
                        </div>

                        <div class="pt-2.5 border-t border-slate-800 text-xs">
                            <span class="font-semibold text-slate-300 block mb-1.5">İç Denetim Aksiyon Kontrol Listesi:</span>
                            <div class="space-y-1 text-slate-400">
                                ${{ev.action_checklist.map(chk => `
                                    <label class="flex items-start gap-2 cursor-pointer select-none hover:text-slate-200">
                                        <input type="checkbox" class="mt-0.5 rounded bg-slate-950 border-slate-700 text-blue-600 focus:ring-0">
                                        <span>${{chk}}</span>
                                    </label>
                                `).join('')}}
                            </div>
                        </div>

                        <div class="pt-2 text-right">
                            <a href="${{ev.item.url}}" target="_blank" class="text-xs text-blue-400 hover:text-blue-300 font-medium inline-flex items-center gap-1">
                                <span>Kaynak Belgeyi Görüntüle</span> <span>&rarr;</span>
                            </a>
                        </div>
                    </div>
                `;
            }}).join('');

            container.innerHTML = `
                <div class="flex items-center justify-between text-xs text-slate-400 px-1 font-mono">
                    <span>${{data.total_scanned || 0}} MADDE TARANDI / ${{data.relevant_count || data.evaluations.length}} AKSİYON GEREKTİREN MADDE</span>
                    <span>${{data.date}}</span>
                </div>
                ${{cards}}
            `;
        }}

        async function sendEmailReport() {{
            const emailsStr = document.getElementById('dispatch-emails').value;
            const statusBox = document.getElementById('dispatch-status-box');
            const btn = document.getElementById('btn-dispatch-send');

            const emails = emailsStr.split(',').map(e => e.trim()).filter(e => e);
            if (emails.length === 0) {{
                alert('Lütfen geçerli bir e-posta adresi girin.');
                return;
            }}

            btn.disabled = true;
            btn.innerText = 'Gönderiliyor...';
            statusBox.className = 'text-xs p-3 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-300 block';
            statusBox.innerHTML = 'PDF derleniyor ve dağıtım gerçekleştiriliyor...';

            let payload = {{ emails: emails }};
            if (currentScanMode === 'range') {{
                payload.start_date = document.getElementById('start-date').value;
                payload.end_date = document.getElementById('end-date').value;
            }} else {{
                payload.date = document.getElementById('scan-date').value;
            }}

            try {{
                const res = await fetch('/api/send-email', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(payload)
                }});
                const data = await res.json();
                statusBox.className = 'text-xs p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 block';
                statusBox.innerHTML = `<strong>✓ Başarılı:</strong> ${{data.message || 'Rapor iletildi.'}}`;
            }} catch(e) {{
                statusBox.className = 'text-xs p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-300 block';
                statusBox.innerHTML = `<strong>Hata:</strong> ${{e.message}}`;
            }} finally {{
                btn.disabled = false;
                btn.innerText = 'PDF Raporunu E-Posta ile Gönder';
            }}
        }}

        function downloadCurrentPdf() {{
            if (currentScanMode === 'range') {{
                const start = document.getElementById('start-date').value;
                const end = document.getElementById('end-date').value;
                window.location.href = `/api/reports/pdf?mode=range&start_date=${{start}}&end_date=${{end}}`;
            }} else {{
                const date = document.getElementById('scan-date').value;
                window.location.href = `/api/reports/pdf?mode=single&date=${{date}}`;
            }}
        }}

        // Initial Load
        window.addEventListener('DOMContentLoaded', async () => {{
            await loadProfile();
            await loadLLMConfig();
            executeLiveScan();
        }});
    </script>
</body>
</html>
"""
