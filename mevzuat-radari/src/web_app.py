"""
Standalone Web Dashboard and REST API for Mevzuat Radarı.
Powered by FastAPI, modern responsive UI and live scraping & audit engine.
"""
import os
import sys
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Query, HTTPException, Body
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.models import GazetteItem
from src.evaluator import (
    load_company_profile,
    generate_daily_audit_report,
    score_item_relevance,
    evaluate_gazette_item,
)
from src.pdf_generator import generate_pdf_report
from src.notifier import dispatch_daily_audit_pdf


app = FastAPI(
    title="Mevzuat Radarı Web Paneli",
    description="Resmî Gazete İç Denetim & Uyum Radarı Web Servisi",
    version="1.2.0",
)


class EmailDispatchRequest(BaseModel):
    emails: List[str]
    date: Optional[str] = None
    min_score: int = 30


class SimulateRequest(BaseModel):
    title: str
    category: str = "Tebliğ"
    institution: str = ""


@app.get("/api/profile")
def get_profile() -> Dict[str, Any]:
    """Returns active company profile."""
    profile = load_company_profile()
    return profile.model_dump()


@app.get("/api/scan")
def run_scan(
    date: Optional[str] = Query(None, description="Tarih: YYYY-MM-DD"),
    min_score: int = Query(30, description="Minimum alaka skoru (0-100)"),
) -> Dict[str, Any]:
    """Executes live Gazette scan and audit evaluation."""
    try:
        report = generate_daily_audit_report(date_str=date, min_score=min_score)
        
        # Ensure PDF is generated in reports directory
        reports_dir = os.path.join(project_root, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        clean_date = report.date.replace("/", "-").replace(".", "-")
        pdf_path = os.path.join(reports_dir, f"{clean_date}.pdf")
        generate_pdf_report(report, pdf_path)
        
        return report.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/send-email")
def send_email_report(req: EmailDispatchRequest) -> Dict[str, Any]:
    """Dispatches audit PDF report to requested email addresses."""
    try:
        res = dispatch_daily_audit_pdf(
            recipient_emails=req.emails,
            date_str=req.date,
            min_score=req.min_score,
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/reports/pdf")
def download_pdf(date: Optional[str] = Query(None)):
    """Downloads the generated PDF report."""
    target_date = date or datetime.now().strftime("%Y-%m-%d")
    clean_date = target_date.replace("/", "-").replace(".", "-")
    pdf_path = os.path.join(project_root, "reports", f"{clean_date}.pdf")
    
    if not os.path.exists(pdf_path):
        # Generate on the fly
        report = generate_daily_audit_report(date_str=target_date, min_score=30)
        generate_pdf_report(report, pdf_path)

    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF raporu bulunamadı.")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"Mevzuat_Denetim_Bulteni_{clean_date}.pdf",
    )


@app.post("/api/simulate")
def simulate_regulation(req: SimulateRequest) -> Dict[str, Any]:
    """Simulates relevance and impact of a custom regulation."""
    profile = load_company_profile()
    item = GazetteItem(
        title=req.title,
        url="https://www.resmigazete.gov.tr/canli-test",
        category=req.category,
        institution=req.institution if req.institution else None,
    )
    score, reasons, risk = score_item_relevance(item, profile)
    ev = evaluate_gazette_item(item, profile)
    return {
        "title": req.title,
        "relevance_score": score,
        "risk_level": risk,
        "matched_reasons": reasons,
        "affected_departments": ev.affected_departments,
        "executive_summary": ev.executive_summary,
        "penalty_and_legal_risk": ev.penalty_and_legal_risk,
        "action_checklist": ev.action_checklist,
    }


@app.get("/", response_class=HTMLResponse)
def index_page():
    """Serves the interactive web panel."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resmî Gazete İç Denetim & Uyum Radarı</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Inter', sans-serif; }}</style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen antialiased p-4 md:p-8">
    <div class="max-w-5xl mx-auto space-y-6">

        <!-- HEADER -->
        <header class="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl backdrop-blur">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-700 pb-5">
                <div class="flex items-center gap-3">
                    <div class="w-12 h-12 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-2xl">
                        🛡️
                    </div>
                    <div>
                        <h1 class="text-xl md:text-2xl font-extrabold text-white tracking-tight">
                            Resmî Gazete İç Denetim & Uyum Radarı
                        </h1>
                        <p class="text-xs md:text-sm text-slate-400">
                            Model Context Protocol (MCP) & AI Destekli Mevzuat İzleme ve Risk Analiz Paneli
                        </p>
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        ● Canlı Web Servisi Aktif
                    </span>
                </div>
            </div>

            <!-- PROFILE SUMMARY -->
            <div id="profile-summary" class="grid grid-cols-2 md:grid-cols-4 gap-3 mt-5 text-xs">
                <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-700/50">
                    <span class="text-slate-400 block text-[11px]">Aktif Şirket Profili:</span>
                    <span id="prof-name" class="font-bold text-white block truncate mt-0.5">Yükleniyor...</span>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-700/50">
                    <span class="text-slate-400 block text-[11px]">Ölçek & Ciro:</span>
                    <span id="prof-scale" class="font-bold text-white block truncate mt-0.5">Yükleniyor...</span>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-700/50">
                    <span class="text-slate-400 block text-[11px]">Ana Faaliyet / NACE:</span>
                    <span id="prof-sector" class="font-bold text-white block truncate mt-0.5">Yükleniyor...</span>
                </div>
                <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-700/50">
                    <span class="text-slate-400 block text-[11px]">Düzenleyiciler:</span>
                    <span id="prof-regulators" class="font-bold text-white block truncate mt-0.5">Yükleniyor...</span>
                </div>
            </div>
        </header>

        <!-- SCANNING & ACTION CONTROLS -->
        <section class="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl space-y-4">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div class="flex flex-wrap items-center gap-3">
                    <div>
                        <label class="block text-[11px] font-semibold text-slate-400 mb-1">Taranacak Tarih:</label>
                        <input id="scan-date" type="date" value="{today_str}" class="px-3 py-2 text-xs rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                    <div>
                        <label class="block text-[11px] font-semibold text-slate-400 mb-1">Min. Alaka Eşiği (%):</label>
                        <select id="min-score" class="px-3 py-2 text-xs rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="30" selected>%30 (Önerilen)</option>
                            <option value="50">%50 (Yüksek & Kritik)</option>
                            <option value="70">%70 (Yalnızca Kritik)</option>
                            <option value="10">%10 (Tüm Eşleşmeler)</option>
                        </select>
                    </div>
                    <div class="pt-5">
                        <button onclick="executeLiveScan()" id="btn-scan" class="px-5 py-2 text-xs font-bold rounded-xl bg-blue-600 hover:bg-blue-500 text-white shadow-lg shadow-blue-600/30 transition flex items-center gap-2">
                            <span>🔍</span> <span>Canlı Taramayı Başlat</span>
                        </button>
                    </div>
                </div>

                <div class="flex items-center gap-2 pt-2 md:pt-5">
                    <button onclick="downloadCurrentPdf()" class="px-4 py-2 text-xs font-semibold rounded-xl bg-slate-700 hover:bg-slate-600 text-white border border-slate-600 transition flex items-center gap-1.5 shadow">
                        <span>📥</span> <span>PDF Raporu İndir</span>
                    </button>
                </div>
            </div>

            <!-- EMAIL DISPATCH BOX -->
            <div class="pt-4 border-t border-slate-700/80 flex flex-col md:flex-row gap-3 items-center">
                <input id="email-recipients" type="text" placeholder="E-Posta Dağıtım Listesi (örn: denetim@stm.com.tr, uyum@stm.com.tr)" value="denetim@stm.com.tr, uyum@stm.com.tr" class="w-full md:flex-1 px-4 py-2 text-xs rounded-xl bg-slate-900 border border-slate-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500">
                <button onclick="sendEmailReport()" id="btn-email" class="w-full md:w-auto px-5 py-2 text-xs font-bold rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-600/30 transition flex items-center justify-center gap-2">
                    <span>🚀</span> <span>PDF'i E-Posta ile Gönder</span>
                </button>
            </div>
            
            <div id="action-status" class="hidden text-xs p-3 rounded-xl"></div>
        </section>

        <!-- SCAN RESULTS SECTION -->
        <main id="results-area" class="space-y-4">
            <div class="bg-slate-800/40 border border-slate-800 rounded-2xl p-12 text-center text-slate-400 text-sm">
                Taramayı başlatmak için yukarıdaki <strong>"Canlı Taramayı Başlat"</strong> butonuna tıklayın.
            </div>
        </main>

    </div>

    <script>
        async function loadProfile() {{
            try {{
                const res = await fetch('/api/profile');
                const data = await res.json();
                document.getElementById('prof-name').innerText = data.general.name;
                document.getElementById('prof-scale').innerText = data.general.employee_count + ' Çalışan | ' + data.general.annual_turnover_tl;
                document.getElementById('prof-sector').innerText = data.sectors_and_nace.primary_sector;
                document.getElementById('prof-regulators').innerText = data.regulatory_bodies.slice(0, 3).join(', ') + '...';
            }} catch(e) {{
                console.error(e);
            }}
        }}

        async function executeLiveScan() {{
            const date = document.getElementById('scan-date').value;
            const minScore = document.getElementById('min-score').value;
            const btn = document.getElementById('btn-scan');
            const resultsArea = document.getElementById('results-area');

            btn.innerHTML = '<span>⏳</span> <span>Resmî Gazete Taranıyor...</span>';
            btn.disabled = true;

            resultsArea.innerHTML = `
                <div class="bg-slate-800/60 border border-slate-700 rounded-2xl p-12 text-center text-slate-300">
                    <div class="inline-block animate-spin text-3xl mb-3">⚙️</div>
                    <p class="font-semibold text-sm">resmigazete.gov.tr fihristi indiriliyor ve şirket profili ile eşleştiriliyor...</p>
                </div>
            `;

            try {{
                const res = await fetch(`/api/scan?date=${{date}}&min_score=${{minScore}}`);
                const data = await res.json();
                renderScanResults(data);
            }} catch (e) {{
                resultsArea.innerHTML = `<div class="p-4 bg-red-500/20 border border-red-500/30 text-red-300 rounded-xl text-xs">Hata: ${{e.message}}</div>`;
            }} finally {{
                btn.innerHTML = '<span>🔍</span> <span>Canlı Taramayı Başlat</span>';
                btn.disabled = false;
            }}
        }}

        function renderScanResults(data) {{
            const container = document.getElementById('results-area');
            
            if (!data.evaluations || data.evaluations.length === 0) {{
                container.innerHTML = `
                    <div class="bg-slate-800/80 border border-slate-700 rounded-2xl p-8 text-center space-y-3 shadow-lg">
                        <div class="w-12 h-12 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto text-2xl font-bold">✓</div>
                        <h3 class="text-base font-bold text-white">Bu Tarih İçin Şirketi İlgilendiren Kritik Karar Bulunmadı</h3>
                        <p class="text-xs text-slate-400 max-w-lg mx-auto leading-relaxed">
                            Toplam <strong>${{data.total_scanned}}</strong> madde tarandı. Şirket profilinizdeki savunma, askeri ve Ar-Ge kriterlerine uyan öncelikli bir tebliğ/karar bulunmamıştır (0 Yanıltıcı Alarm).
                        </p>
                    </div>
                `;
                return;
            }}

            const cards = data.evaluations.map((ev, i) => {{
                const isCrit = ev.risk_level === 'Kritik';
                const badgeColor = isCrit ? 'bg-red-500/20 text-red-400 border-red-500/30' : (ev.risk_level === 'Yüksek' ? 'bg-amber-500/20 text-amber-400 border-amber-500/30' : 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30');
                const barColor = isCrit ? '#ef4444' : (ev.risk_level === 'Yüksek' ? '#f59e0b' : '#eab308');

                return `
                    <div class="bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl space-y-4">
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-700 pb-3">
                            <div class="flex items-center gap-2">
                                <span class="px-2.5 py-0.5 rounded-full text-xs font-extrabold border ${{badgeColor}}">
                                    ${{ev.risk_level.toUpperCase()}}
                                </span>
                                <span class="text-xs font-semibold text-slate-400">${{ev.item.category}}</span>
                                <span class="text-xs text-slate-500">•</span>
                                <span class="text-xs font-medium text-slate-400 truncate max-w-[240px]">${{ev.item.institution || 'Resmî Gazete'}}</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <span class="text-xs text-slate-400">Alaka Skoru:</span>
                                <div class="w-24 bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-700">
                                    <div class="h-2 rounded-full" style="width: ${{ev.relevance_score}}%; background-color: ${{barColor}};"></div>
                                </div>
                                <span class="text-xs font-extrabold text-white">%${{ev.relevance_score}}</span>
                            </div>
                        </div>

                        <h3 class="text-sm md:text-base font-bold text-white leading-snug">
                            ${{i + 1}}. ${{ev.item.title}}
                        </h3>

                        <div class="text-xs bg-slate-900/80 p-3.5 rounded-xl border border-slate-700/60 space-y-1">
                            <span class="font-semibold text-blue-400 block">🎯 Eşleşme Gerekçeleri:</span>
                            <ul class="list-disc list-inside text-slate-300 space-y-0.5">
                                ${{ev.matched_reasons.map(r => `<li>${{r}}</li>`).join('')}}
                            </ul>
                        </div>

                        <div class="text-xs space-y-1">
                            <span class="font-semibold text-slate-300">📝 İç Denetim Yönetici Özeti:</span>
                            <p class="text-slate-400 leading-relaxed">${{ev.executive_summary}}</p>
                        </div>

                        ${{ev.penalty_and_legal_risk ? `
                            <div class="text-xs p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-300">
                                <strong>⚠️ Yaptırım & Hukuki Risk:</strong> ${{ev.penalty_and_legal_risk}}
                            </div>
                        ` : ''}}

                        <div class="text-xs flex flex-wrap items-center gap-1.5 pt-1">
                            <span class="font-semibold text-slate-300 mr-1">🏢 Etkilenen Departmanlar:</span>
                            ${{ev.affected_departments.map(d => `<span class="px-2 py-0.5 rounded-md bg-slate-900 border border-slate-700 text-slate-200 font-medium">${{d}}</span>`).join('')}}
                        </div>

                        <div class="pt-3 border-t border-slate-700/80 text-xs">
                            <span class="font-semibold text-slate-300 block mb-2">✅ İç Denetim Aksiyon Kontrol Listesi:</span>
                            <div class="space-y-1.5">
                                ${{ev.action_checklist.map(chk => `
                                    <label class="flex items-start gap-2 cursor-pointer select-none text-slate-400 hover:text-white transition">
                                        <input type="checkbox" class="mt-0.5 rounded bg-slate-900 border-slate-700 text-blue-600 focus:ring-0">
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
                <div class="flex items-center justify-between text-xs text-slate-400 px-1">
                    <span>📊 Tarama Sonucu: <strong>${{data.total_scanned}}</strong> madde tarandı, <strong>${{data.relevant_count}}</strong> aksiyon maddesi bulundu.</span>
                    <span>Tarih: ${{data.date}}</span>
                </div>
                ${{cards}}
            `;
        }}

        async function sendEmailReport() {{
            const emailsStr = document.getElementById('email-recipients').value;
            const date = document.getElementById('scan-date').value;
            const statusBox = document.getElementById('action-status');
            const btn = document.getElementById('btn-email');

            const emails = emailsStr.split(',').map(e => e.trim()).filter(e => e);
            if (emails.length === 0) {{
                alert('Lütfen en az bir e-posta adresi girin.');
                return;
            }}

            btn.disabled = true;
            btn.innerHTML = '<span>⏳</span> <span>Gönderiliyor...</span>';
            statusBox.className = 'text-xs p-3 rounded-xl bg-blue-500/10 border border-blue-500/20 text-blue-300 block';
            statusBox.innerHTML = 'PDF derleniyor ve dağıtım listesine aktarılıyor...';

            try {{
                const res = await fetch('/api/send-email', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ emails, date }})
                }});
                const data = await res.json();
                statusBox.className = 'text-xs p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 block';
                statusBox.innerHTML = `<strong>✓ Başarılı:</strong> ${{data.message || 'Rapor gönderildi.'}}`;
            }} catch(e) {{
                statusBox.className = 'text-xs p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-300 block';
                statusBox.innerHTML = `<strong>Hata:</strong> ${{e.message}}`;
            }} finally {{
                btn.disabled = false;
                btn.innerHTML = '<span>🚀</span> <span>PDF\'i E-Posta ile Gönder</span>';
            }}
        }}

        function downloadCurrentPdf() {{
            const date = document.getElementById('scan-date').value;
            window.open(`/api/reports/pdf?date=${{date}}`, '_blank');
        }}

        // Load profile and run initial scan on load
        window.addEventListener('DOMContentLoaded', () => {{
            loadProfile();
            executeLiveScan();
        }});
    </script>
</body>
</html>
"""
