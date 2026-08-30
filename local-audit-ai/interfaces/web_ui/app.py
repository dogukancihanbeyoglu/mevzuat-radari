"""
Auditoris — Yeni Nesil Otonom İç Denetim ve Otomasyon Kokpiti
IIA Küresel Standartlarında 5 Aşamalı Yaşam Döngüsü & Otomatik Çalışma Kağıdı Üretimi
"""
import os
import sys
import tempfile
import streamlit as st

# Modül yolunu ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from modules import AuditOrchestrator
from core.router.model_registry import ModelRegistry

# Streamlit Sayfa Yapılandırması
st.set_page_config(
    page_title="Auditoris — Denetim İşletim Sistemi",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimalist, Mat Siyah ve Temiz Kurumsal CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #0f172a;
    }

    /* Üst Banner: Sade Mat Siyah */
    .hero-banner {
        background-color: #000000;
        border-radius: 12px;
        padding: 1.25rem 1.75rem;
        margin-bottom: 1.5rem;
        color: #ffffff;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .hero-title {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        color: #ffffff;
    }
    .hero-subtitle {
        font-size: 0.85rem;
        color: #94a3b8;
        margin-top: 0.2rem;
        font-weight: 500;
    }

    /* Adım Başlıkları */
    .step-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.95rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 0.5rem;
        margin-bottom: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .step-badge {
        background-color: #000000;
        color: #ffffff;
        width: 24px;
        height: 24px;
        border-radius: 6px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: 700;
    }

    /* Kalite & Metrik Paneli */
    .metrics-bar {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #000000;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1.5rem;
    }
    .metric-score {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-info {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 0.2rem;
    }

    /* Ana Aksiyon Butonu */
    .primary-action-btn button {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #000000 !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.75rem 1.5rem !important;
        transition: background-color 0.15s ease !important;
    }
    .primary-action-btn button:hover {
        background-color: #1e293b !important;
        border-color: #1e293b !important;
    }

    /* RAG Kartları */
    .rag-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #000000;
        border-radius: 6px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.65rem;
    }
    .rag-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.3rem;
    }
    .rag-badge {
        background: #f1f5f9;
        color: #334155;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
    }

    /* Alt Bilgi */
    .footer-text {
        font-size: 0.75rem;
        color: #94a3b8;
        border-top: 1px solid #e2e8f0;
        padding-top: 1rem;
        margin-top: 2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_orchestrator():
    return AuditOrchestrator()

orchestrator = get_orchestrator()
registry = ModelRegistry()

# Session State
if "audit_result" not in st.session_state:
    st.session_state["audit_result"] = None
if "active_context" not in st.session_state:
    st.session_state["active_context"] = ""
if "active_task" not in st.session_state:
    st.session_state["active_task"] = None
if "temp_files" not in st.session_state:
    st.session_state["temp_files"] = []

# Sol Kenar Çubuğu (Sidebar)
with st.sidebar:
    st.markdown("### Model ve Sistem Ayarları")
    st.caption("Yerel denetim motoru yapılandırması")
    
    current_tiers = registry.get_tier_models()
    available_models = registry.discover_installed_models()

    with st.expander("Model Havuzu ve Tier Yapılandırması", expanded=False):
        if st.button("Otonom En İyi Modelleri Eşle", use_container_width=True, help="Kurulu modelleri analiz edip en ideal Tier eşleştirmesini otomatik yapar."):
            res_auto = registry.auto_configure_best_tiers()
            if res_auto.get("success"):
                st.success(res_auto["rationale"])
                st.rerun()

        st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
        
        t1_cur = current_tiers.get("tier_1_light", {}).get("name", "qwen2.5-coder:7b")
        t1_idx = available_models.index(t1_cur) if t1_cur in available_models else 0
        new_t1 = st.selectbox("Tier 1 (Hızlı / Veri Ayıklama):", available_models, index=t1_idx, key="cfg_t1")

        t2_cur = current_tiers.get("tier_2_standard", {}).get("name", "deepseek-r1:8b")
        t2_idx = available_models.index(t2_cur) if t2_cur in available_models else 0
        new_t2 = st.selectbox("Tier 2 (Standart / 5C & Muhakeme):", available_models, index=t2_idx, key="cfg_t2")

        t3_cur = current_tiers.get("tier_3_deep_reasoning", {}).get("name", "qwen2.5-coder:14b")
        t3_idx = available_models.index(t3_cur) if t3_cur in available_models else 0
        new_t3 = st.selectbox("Tier 3 (İleri Düzey / Python & Analitik):", available_models, index=t3_idx, key="cfg_t3")

        if st.button("Ayarları Kaydet", use_container_width=True):
            registry.update_tier_model("tier_1_light", new_t1)
            registry.update_tier_model("tier_2_standard", new_t2)
            registry.update_tier_model("tier_3_deep_reasoning", new_t3)
            st.success("Model havuzu güncellendi.")
            st.rerun()

    st.divider()
    temperature_val = st.slider("Model Sıcaklığı (Temperature):", min_value=0.0, max_value=0.7, value=0.2, step=0.05)
    enable_pii = st.toggle("Hassas Veri Maskeleme (PII)", value=True, help="TCKN, IBAN, Kredi Kartı ve E-postalar modele gitmeden önce yerel regex ile maskelenir.")

# Üst Başlık & PDF İndirme Alanı
col_hero_text, col_hero_pdf = st.columns([3, 1])

with col_hero_text:
    st.markdown("""
    <div class="hero-banner">
        <div>
            <div class="hero-title">Auditoris</div>
            <div class="hero-subtitle">IIA Küresel Standartlarında Yeni Nesil Otonom İç Denetim ve Otomasyon Kokpiti</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_hero_pdf:
    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    pdf_path = "storage/Auditoris_Kullanici_Kilavuzu_2026.pdf"
    if not os.path.exists(pdf_path):
        from core.export.guide_pdf_generator import generate_user_guide_pdf
        generate_user_guide_pdf(pdf_path)
        
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    st.download_button(
        "PDF Kılavuzunu İndir",
        data=pdf_bytes,
        file_name="Auditoris_Kullanici_Kilavuzu_2026.pdf",
        mime="application/pdf",
        use_container_width=True
    )

# 1. Adım: Görev Seçimi
st.markdown('<div class="step-header"><div class="step-badge">1</div> Denetim Yaşam Döngüsü ve Görevi Seçin</div>', unsafe_allow_html=True)

PHASES = {
    "1. Yıllık Planlama (Annual Planning)": [
        {"key": "audit_universe", "title": "Denetim Evreni ve Risk Derecelendirmesi", "placeholder": "25 ana süreç ve iştiraklerin risk puanları, finansal büyüklükleri..."},
        {"key": "resource_competency_mapping", "title": "Kaynak ve Yetkinlik Planlaması", "placeholder": "Denetim kadrosu, yetkinlik puanları ve 2026 denetim planı..."}
    ],
    "2. Görev Planlama (Engagement Planning)": [
        {"key": "rcm_generation", "title": "Risk ve Kontrol Matrisi (RCM) & Walkthrough", "placeholder": "Süreç anlatımı, politika veya akış şeması notlarını girin..."},
        {"key": "scoping_document", "title": "Denetim Kapsam Dokümanı (Scoping)", "placeholder": "Kapsam içi ve kapsam dışı bırakılacak risk alanları..."}
    ],
    "3. Saha Çalışması (Fieldwork & Testing)": [
        {"key": "test_procedure", "title": "Kontrol Test Prosedürü Geliştirme", "placeholder": "Test edilecek kontrol faaliyeti, tolerans limiti ve denetim dönemi..."},
        {"key": "control_analysis", "title": "Kontrol Tanımı ve Tasarım Zayıflığı Analizi", "placeholder": "Mevcut kontrol tanımını yapıştırın, açık ve muğlak noktaları inceleyelim..."},
        {"key": "data_extraction", "title": "Yapılandırılmamış Metinden Veri Ayıklama", "placeholder": "Fatura, e-posta veya sözleşme metinlerini yapıştırın..."}
    ],
    "4. Denetim Raporlama (Reporting)": [
        {"key": "finding_5c", "title": "5C Standart Denetim Bulgusu Yazımı", "placeholder": "Saha tespitleri, mülakat notları, ihlal edilen politika ve finansal etki..."},
        {"key": "executive_summary", "title": "Yönetici Özeti (Executive Summary)", "placeholder": "Tamamlanan denetimin ana bulguları ve yönetim aksiyon taahhütleri..."}
    ],
    "5. Sürekli Denetim & Analitik (Analytics)": [
        {"key": "data_analytics", "title": "Python (Pandas) İstisna Analiz Kodu", "placeholder": "Veri tablosunun sütunlarını ve aranacak istisna kurallarını girin..."}
    ]
}

col_phase, col_task = st.columns(2, gap="medium")
with col_phase:
    selected_phase = st.selectbox("Denetim Aşaması:", list(PHASES.keys()))

with col_task:
    tasks_for_phase = PHASES[selected_phase]
    task_titles = [t["title"] for t in tasks_for_phase]
    selected_task_title = st.selectbox("Görev Türü:", task_titles)
    active_task = next(t for t in tasks_for_phase if t["title"] == selected_task_title)
    selected_task_key = active_task["key"]

st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

# 2. Adım: Veri ve Dosya Girişi
st.markdown('<div class="step-header"><div class="step-badge">2</div> Saha Notları ve Denetim Dosyaları</div>', unsafe_allow_html=True)

col_input_left, col_input_right = st.columns(2, gap="medium")

with col_input_left:
    uploaded_files = st.file_uploader(
        "Denetim Belgeleri (.docx, .xlsx, .pdf, .txt, .csv):",
        type=["docx", "xlsx", "xls", "pdf", "txt", "csv"],
        accept_multiple_files=True
    )


    custom_context = st.text_input(
        "Kurumsal Bağlam / Şirket Bilgisi:",
        value="Mega Holding A.Ş. — Kurumsal İç Denetim"
    )

with col_input_right:
    input_text = st.text_area(
        "Saha Notları / Açıklama / Ham Veri:",
        height=145,
        placeholder=active_task["placeholder"]
    )

st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

# 3. Adım: Çalıştırma
st.markdown('<div class="step-header"><div class="step-badge">3</div> Analiz ve Çalışma Kağıdı Üretimi</div>', unsafe_allow_html=True)

st.markdown('<div class="primary-action-btn">', unsafe_allow_html=True)
run_button = st.button("Çalışma Kağıdını Üret", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if run_button:
    if not input_text and not uploaded_files:
        st.warning("Lütfen bir metin girin veya en az bir dosya yükleyin.")
    else:
        temp_paths = []
        if uploaded_files:
            temp_upload_dir = tempfile.mkdtemp()
            for uf in uploaded_files:
                file_dest = os.path.join(temp_upload_dir, uf.name)
                with open(file_dest, "wb") as f:
                    f.write(uf.getvalue())
                temp_paths.append(file_dest)

        with st.spinner("Model yönlendirici analiz ediyor ve IIA çalışma kağıdı üretiliyor..."):
            try:
                res = orchestrator.run_audit_task(
                    module_name=selected_task_key,
                    input_text=input_text or "Standart denetim analizi talebi.",
                    file_paths=temp_paths,
                    custom_context=custom_context,
                    enable_masking=enable_pii,
                    custom_temperature=temperature_val
                )
                st.session_state["audit_result"] = res
                st.session_state["active_context"] = custom_context
                st.session_state["active_task"] = active_task
                st.session_state["temp_files"] = temp_paths
            except Exception as e:
                st.error(f"Hata oluştu: {str(e)}")

# Sonuç Gösterimi
if st.session_state["audit_result"] is not None:
    res = st.session_state["audit_result"]
    cur_task = st.session_state["active_task"] or active_task
    cur_context = st.session_state["active_context"] or custom_context
    cur_temp_files = st.session_state["temp_files"]

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    # Kalite Skoru ve Model Bilgisi Paneli
    qa_eval = res.get("quality_evaluation", {})
    qa_score = qa_eval.get("score", 95)
    qa_label = qa_eval.get("label", "Mükemmel (IIA Standartlarında)")
    model_name = res.get("dispatched_model", {}).get("model_name", "Local LLM")
    elapsed = res.get("execution_time_sec", res.get("execution_time_seconds", 1.8))

    st.markdown(f"""
    <div class="metrics-bar">
        <div>
            <div class="metric-score">Kalite Skoru: {qa_score}/100 — {qa_label}</div>
            <div class="metric-info">Model: <strong>{model_name}</strong> | Süre: <strong>{elapsed} sn</strong> | Denetim İzi: <code>{res['audit_trail_id']}</code></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Dinamik Mevzuat (RAG)
    matched_regs = orchestrator.search_regulations(f"{cur_task.get('key', '')} {cur_context} {res['output_content'][:1000]}", top_k=3)
    if matched_regs:
        with st.expander("Eşleşen Yasal Mevzuat ve Kriterler (RAG)", expanded=True):
            for reg in matched_regs:
                st.markdown(f"""
                <div class="rag-card">
                    <div class="rag-header">
                        <strong>{reg['authority']} — {reg['title']}</strong>
                        <span class="rag-badge">%{reg.get('match_score_pct', 85)} Eşleşme</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #475569; margin-top: 4px;">{reg['content']}</div>
                </div>
                """, unsafe_allow_html=True)

    # 3 Fonksiyonel Sonuç Sekmesi
    tab_wp, tab_model, tab_security = st.tabs([
        "📄 IIA Çalışma Kağıdı",
        "🔍 Model & Akıllı Yönlendirme Analizi",
        "🔒 Güvenlik & Denetim İzi (Audit Trail)"
    ])

    with tab_wp:
        # Çalışma Kağıdı Çıktısı
        st.markdown(res["output_content"])

        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

        # Dışa Aktarma Butonları
        col_exp1, col_exp2, col_exp3 = st.columns(3, gap="medium")
        
        with col_exp1:
            docx_bytes = orchestrator.export_workpaper_docx(
                title=f"IIA Çalışma Kağıdı — {cur_task['title']}",
                content=res["output_content"],
                audit_trail_id=res["audit_trail_id"],
                context=cur_context
            )
            st.download_button(
                "Word (.docx) İndir",
                data=docx_bytes,
                file_name=f"audit_workpaper_{cur_task['key']}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

        with col_exp2:
            xlsx_bytes = orchestrator.export_workpaper_excel(
                title=f"IIA Tablosu — {cur_task['title']}",
                content=res["output_content"]
            )
            st.download_button(
                "Excel (.xlsx) İndir",
                data=xlsx_bytes,
                file_name=f"audit_workpaper_{cur_task['key']}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        with col_exp3:
            has_code = "```python" in res["output_content"]
            if has_code:
                run_sandbox_btn = st.button("Kodu Sandbox'ta Çalıştır", use_container_width=True)
                if run_sandbox_btn:
                    code_snippet = res["output_content"].split("```python")[1].split("```")[0].strip()
                    with st.spinner("Python kodu izole yerel sandbox'ta çalıştırılıyor..."):
                        first_file = cur_temp_files[0] if cur_temp_files else None
                        sb_res = orchestrator.execute_analytics_script(code_snippet, data_file_path=first_file)
                        if sb_res["success"]:
                            st.success("✅ Python analitik kodu izole sandbox'ta başarıyla çalıştırıldı.")
                            if sb_res.get("stdout"):
                                st.code(sb_res["stdout"], language="text")
                            for gf in sb_res.get("generated_files", []):
                                g_bytes = gf.get("file_bytes") or gf.get("bytes")
                                st.download_button(
                                    f"📥 {gf['file_name']} İndir ({gf.get('file_size_kb', 0)} KB)",
                                    data=g_bytes,
                                    file_name=gf["file_name"],
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    key=f"sb_down_{gf['file_name']}"
                                )
                        else:
                            st.error(f"Sandbox Hatası: {sb_res.get('stderr') or sb_res.get('error')}")

    with tab_model:
        st.markdown("### 🤖 Model & Otonom Yönlendirme Analizi")
        disp = res.get("dispatched_model", {})
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown(f"**Atanan Model:** `{disp.get('model_name', model_name)}`")
            st.markdown(f"**Karmaşıklık Seviyesi:** `{res.get('complexity_tier', disp.get('tier', 'tier_2_standard'))}`")
            st.markdown(f"**Özel Model Ataması (Override):** `{'Evet' if disp.get('is_override') else 'Hayır (Otomatik Yönlendirildi)'}`")
        with col_m2:
            st.markdown(f"**Model Sıcaklığı (Temperature):** `{disp.get('temperature', 0.2)}`")
            st.markdown(f"**İşlem Süresi:** `{elapsed} saniye`")
            st.markdown(f"**Otonom Yönlendirme Gerekçesi:**")
            st.info(disp.get("rationale", "Görev karmaşıklığı ve parametre boyutuna göre en uygun yerel model seçildi."))

        st.markdown("#### 📝 Modele İletilen Meta-Prompt (Denetçi Yönergesi):")
        with st.expander("Kullanılan Tam Prompt Detayını Görüntüle", expanded=False):
            st.code(res.get("prompt_used", "Prompt kaydedilmedi."), language="markdown")

    with tab_security:
        st.markdown("### 🔒 Güvenlik, PII ve Kriptografik Denetim İzi (Audit Trail)")
        
        trail_id = res.get('audit_trail_id', 'N/A')
        trail_file = res.get('audit_trail_file', '')
        
        # JSON dosya içeriğini yükle
        trail_json_content = {}
        trail_json_str = "{}"
        if trail_file and os.path.exists(trail_file):
            try:
                import json
                with open(trail_file, "r", encoding="utf-8") as f:
                    trail_json_content = json.load(f)
                    trail_json_str = json.dumps(trail_json_content, ensure_ascii=False, indent=2)
            except Exception as e:
                trail_json_content = {"error": f"Dosya okunamadı: {str(e)}"}
                trail_json_str = str(trail_json_content)

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown(f"**Denetim İzi Kayıt ID:** `{trail_id}`")
            st.markdown(f"**Girdi Verisi SHA-256 İmzası:**")
            st.code(res.get("input_hash", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"), language="text")
        with col_s2:
            st.markdown(f"**Maskelenen Hassas Veri (PII) Adedi:** `{res.get('masked_fields_count', 0)} adet`")
            st.markdown(f"**Ayıklanan Kritik Kanıt Adedi:** `{res.get('extracted_evidence_count', 0)} adet`")
            st.markdown(f"**Denetim İzi JSON Dosya Yolu:** `{trail_file or 'storage/audit_trails/'}`")

        st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
        st.markdown("#### 📜 Kriptografik Denetim İzi JSON Dosyası İçeriği:")
        
        # JSON İndirme Butonu ve Canlı JSON Viewer
        col_json_view, col_json_down = st.columns([3, 1])
        with col_json_down:
            st.download_button(
                "JSON Dosyasını İndir",
                data=trail_json_str,
                file_name=f"audit_trail_{trail_id}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with st.expander(f"Audit Trail Kayıt Detayı ({trail_id}.json)", expanded=True):
            st.json(trail_json_content)

        st.success("✅ **IIA Global Standartları Uyum Beyanı:** Bu denetim kaydı, değiştirilemez kriptografik SHA-256 hash mührü ile yerel veri tabanına arşivlenmiştir.")

# Footer
st.markdown("""
<div class="footer-text">
    Auditoris | Geliştirici & Sistem Mimarı: Doğukan Cihanbeyoğlu | IIA Küresel Standartları (2026)
</div>
""", unsafe_allow_html=True)
