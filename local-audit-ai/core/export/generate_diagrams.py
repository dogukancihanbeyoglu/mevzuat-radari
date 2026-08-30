"""
Auditoris — Profesyonel Sistem ve Motor Topolojisi Çizim Üreticisi
Matplotlib 300 DPI, Türkçe Karakter (%100 UTF-8 / Arial) ve Kurumsal Enterprise Tasarım Mimarisi
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl

# Türkçe Karakter Desteği için Arial / DejaVu Sans Font Yapılandırması
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Helvetica']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

os.makedirs("storage/diagrams", exist_ok=True)

def draw_badge(ax, x, y, text, bg_color='#0f172a', text_color='#ffffff', fontsize=7.5, pad=0.06):
    bbox = dict(boxstyle=f"round,pad={pad},rounding_size=0.08", facecolor=bg_color, edgecolor='none')
    ax.text(x, y, text, fontsize=fontsize, fontweight='bold', ha='center', va='center', color=text_color, bbox=bbox)

# =========================================================================
# DİYAGRAM 1: Genel Sistem & Hava Boşluklu (Air-Gapped) Topoloji
# =========================================================================
def create_diagram_1():
    fig, ax = plt.subplots(figsize=(13, 7.2), dpi=300)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('#ffffff')

    # Başlık Alanı
    ax.text(6.5, 6.8, "AUDİTORİS — GENEL SİSTEM VE SIFIR BULUT SIZINTISI MİMARİ TOPOLOJİSİ", 
            fontsize=13.5, fontweight='bold', ha='center', color='#0f172a')
    ax.text(6.5, 6.45, "Hava Boşluklu (Air-Gapped) Yapı, Yerel Donanım Güvencesi ve Uçtan Uca İcra Hattı", 
            fontsize=9.5, ha='center', color='#64748b')

    layers = [
        ("1. İSTEMCİ VE KULLANICI ARAYÜZÜ", 0.4, 4.7, 3.6, 1.35, '#2563eb', '#eff6ff', 
         "• Modern Streamlit Denetim Kokpiti\n• 5 Aşama ve 10 Görev Türü Seçimi\n• Ham Veri ve Saha Notu Girişi\n• 3 Fonksiyonel Sekme ve Önizleme"),
        
        ("2. GÜVENLİK VE PII MASKELEME KATMANI", 4.7, 4.7, 3.6, 1.35, '#059669', '#ecfdf5',
         "• KVKK / GDPR Uyumlu Regex Sanitizer\n• Deterministik Varlık Maskeleme ([TCKN_1])\n• Sıfır Bulut Sızıntısı (Zero-Telemetry)\n• SHA-256 Girdi/Çıktı Bütünlük İmzası"),
        
        ("3. OTONOM MODEL YÖNLENDİRİCİ", 9.0, 4.7, 3.6, 1.35, '#d97706', '#fffbeb',
         "• Complexity Router & Tier Belirleme\n• Tier 1 (3B): Hızlı Veri Ayıklama\n• Tier 2 (7B-8B): Muhakeme / RCM / 5C\n• Tier 3 (14B): İleri Kodlama & Analitik"),

        ("4. YEREL MODEL ÇIKARIM MOTORU", 1.5, 2.5, 4.5, 1.45, '#4f46e5', '#eef2ff',
         "• Ollama Engine (127.0.0.1 Yerel Soket)\n• Qwen 2.5 Coder (7B/14B) & DeepSeek-R1 (8B)\n• Llama 3.2 (3B) Hafif Çıkarım Motoru\n• Tamamen Çevrimdışı ve Şifreli Bellek İcrası"),

        ("5. BİLGİ TABANI VE İZOLE SANDBOX", 7.0, 2.5, 4.5, 1.45, '#7c3aed', '#f5f3ff',
         "• Çevrimdışı Vektör RAG (ChromaDB)\n• BDDK, MASAK, SPK, KVKK ve IIA Kütüphanesi\n• İzole Subprocess Python Sandbox Ortamı\n• AST Güvenlik Filtresi ve Otomatik Kod Koşumu"),

        ("6. KURUMSAL VE ÇOKLU SİSTEM ÇIKTI MOTORU", 3.0, 0.4, 7.0, 1.35, '#0f172a', '#f1f5f9',
         "• Resmi Antetli Word (.docx) Raporları  • openpyxl ile Biçimlendirilmiş Zebra Excel (.xlsx)\n• Pandas ile Üretilen İstisna Dosyası (audit_exceptions.xlsx)  • Kriptografik Audit Trail (JSON)\n• IIA Küresel Standartları (2026) 5C Uyum Mührü ve Kalite Kontrol Skoru")
    ]

    for title, x, y, w, h, border, bg, desc in layers:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15",
                                      facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.26, title, fontsize=8.5, fontweight='bold', ha='center', color=border)
        ax.text(x + 0.18, y + 0.16, desc, fontsize=7.2, va='bottom', color='#1e293b', linespacing=1.28)

    # Akış Bağlantı Okları
    arrow_props = dict(facecolor='#475569', edgecolor='none', width=1.6, headwidth=6, headlength=6)
    ax.annotate('', xy=(4.7, 5.35), xytext=(4.0, 5.35), arrowprops=arrow_props)
    ax.annotate('', xy=(9.0, 5.35), xytext=(8.3, 5.35), arrowprops=arrow_props)
    
    ax.annotate('', xy=(3.75, 3.95), xytext=(9.8, 4.7), arrowprops=dict(facecolor='#4f46e5', edgecolor='none', width=1.5, headwidth=6, headlength=6))
    ax.annotate('', xy=(9.25, 3.95), xytext=(10.8, 4.7), arrowprops=dict(facecolor='#7c3aed', edgecolor='none', width=1.5, headwidth=6, headlength=6))

    ax.annotate('', xy=(5.5, 1.75), xytext=(3.75, 2.5), arrowprops=dict(facecolor='#0f172a', edgecolor='none', width=1.6, headwidth=6, headlength=6))
    ax.annotate('', xy=(7.5, 1.75), xytext=(9.25, 2.5), arrowprops=dict(facecolor='#0f172a', edgecolor='none', width=1.6, headwidth=6, headlength=6))

    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.2)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("storage/diagrams/diag_01_system_topology.png", bbox_inches='tight')
    plt.close()

# =========================================================================
# DİYAGRAM 2: 5 Aşama ve 10 Görev Süreç Topolojisi
# =========================================================================
def create_diagram_2():
    fig, ax = plt.subplots(figsize=(13, 7.0), dpi=300)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('#ffffff')

    ax.text(6.5, 6.6, "AUDİTORİS — 5 DENETİM AŞAMASI VE 10 GÖREV İŞ AKIŞ TOPOLOJİSİ", 
            fontsize=13.5, fontweight='bold', ha='center', color='#0f172a')
    ax.text(6.5, 6.25, "IIA Küresel Standartları (2026) ve COSO Uyumlu Uçtan Uca Denetim Yaşam Döngüsü", 
            fontsize=9.5, ha='center', color='#64748b')

    phases = [
        ("1. YILLIK PLANLAMA", 0.3, 0.8, 2.3, 5.0, '#0284c7', '#f0f9ff',
         [("GÖREV 01", "Denetim Evreni ve\nRisk Derecelendirmesi\n• 18 İştirak Skorlama\n• Frekans Tablosu"),
          ("GÖREV 02", "Kaynak ve Yetkinlik\nPlanlaması (Competency)\n• Ekip Yetkinlik Matrisi\n• Dış Kaynak Stratejisi")]),
        
        ("2. GÖREV PLANLAMA", 2.85, 0.8, 2.3, 5.0, '#2563eb', '#eff6ff',
         [("GÖREV 03", "Risk ve Kontrol Matrisi\n(RCM) & Walkthrough\n• 6 Sütunlu RCM\n• 3-5 Mülakat Sorusu"),
          ("GÖREV 04", "Görev Kapsam\nDokümanı (Scoping)\n• Kapsam İçi / Dışı\n• Zaman ve Hedef Sınırı")]),
        
        ("3. SAHA ÇALIŞMASI", 5.4, 0.8, 2.3, 5.0, '#059669', '#ecfdf5',
         [("GÖREV 05", "Kontrol Test Prosedürü\n• 4-Ögeli Test Planı\n• Örneklem Metodolojisi"),
          ("GÖREV 06", "Kontrol Tasarım Analizi\n• SoD Açığı Eleştirisi\n• Güçlü Alternatif Kontrol"),
          ("GÖREV 07", "Serbest Metin Veri Çıkarımı\n• Fatura/Sözleşme JSON\n• 7 Sütunlu Temiz Tablo")]),

        ("4. RAPORLAMA", 7.95, 0.8, 2.3, 5.0, '#d97706', '#fffbeb',
         [("GÖREV 08", "5C Standart Denetim\nBulgusu Yazımı\n• Condition, Criteria, Cause\n• Effect, Recommendation"),
          ("GÖREV 09", "Yönetici Özeti (Summary)\n• Komite ve YK Brifingi\n• Aksiyon Takip Matrisi")]),

        ("5. SÜREKLİ ANALİTİK", 10.5, 0.8, 2.2, 5.0, '#7c3aed', '#f5f3ff',
         [("GÖREV 10", "Python İstisna Kodu &\nİzole Sandbox İcrası\n• Pandas Anomali Filtresi\n• audit_exceptions.xlsx")])
    ]

    for title, x, y, w, h, border, bg, tasks in phases:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12",
                                      facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.28, title, fontsize=8.2, fontweight='bold', ha='center', color=border)

        curr_y = y + h - 0.65
        for tag, desc in tasks:
            task_h = 1.25 if len(tasks) == 3 else 1.95
            task_rect = patches.FancyBboxPatch((x + 0.1, curr_y - task_h), w - 0.2, task_h,
                                               boxstyle="round,pad=0.04,rounding_size=0.08",
                                               facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=1)
            ax.add_patch(task_rect)
            ax.text(x + 0.18, curr_y - 0.25, tag, fontsize=7.5, fontweight='bold', color=border)
            ax.text(x + 0.18, curr_y - 0.52, desc, fontsize=6.8, va='top', color='#1e293b', linespacing=1.22)
            curr_y -= (task_h + 0.25)

    arrow_props = dict(facecolor='#0f172a', edgecolor='none', width=2, headwidth=7, headlength=7)
    for ax_x in [2.6, 5.15, 7.7, 10.25]:
        ax.annotate('', xy=(ax_x + 0.22, 3.3), xytext=(ax_x - 0.04, 3.3), arrowprops=arrow_props)

    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.0)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("storage/diagrams/diag_02_five_phase_lifecycle.png", bbox_inches='tight')
    plt.close()

# =========================================================================
# DİYAGRAM 3: Motor 1 & 2 — Smart Evidence Extractor ve PII Masker Topolojisi
# =========================================================================
def create_diagram_3():
    fig, ax = plt.subplots(figsize=(13, 6.2), dpi=300)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('#ffffff')

    ax.text(6.5, 5.8, "MOTOR 1 & 2: SMART EVIDENCE EXTRACTOR VE PII MASKELEME MOTORU", 
            fontsize=13, fontweight='bold', ha='center', color='#0f172a')
    ax.text(6.5, 5.45, "KVKK/GDPR Uyumlu Deterministik Maskeleme, Büyük Tablo Süzme ve Kriptografik İmzalama", 
            fontsize=9.2, ha='center', color='#64748b')

    nodes = [
        ("1. HAM DENETİM VERİSİ", 0.5, 1.8, 2.6, 3.0, '#dc2626', '#fef2f2',
         "• 25.000+ Satır Excel / CSV\n• Müşteri TCKN ve İsimleri\n• Şirket IBAN ve Hesapları\n• Serbest Metin Saha Notları"),
        
        ("2. SMART EVIDENCE SÜZGECİ", 3.5, 1.8, 2.8, 3.0, '#2563eb', '#eff6ff',
         "• Sayısal Eşik Filtreleme\n• Limit Aşımı Süzgeci\n• MASAK Şüpheli İşlem Ayrıştırma\n• Token Boyutunu %85 Düşürme"),

        ("3. PII MASKER MOTORU", 6.7, 1.8, 2.8, 3.0, '#059669', '#ecfdf5',
         "• Deterministik RegEx Parser\n• Varlık Dönüşümü:\n  TCKN -> [TCKN_1]\n  IBAN -> [IBAN_1]\n• Bellek-İçi Ters Eşleme Sözlüğü"),

        ("4. GÜVENLİ PAYLOAD & AUDIT HASH", 9.9, 1.8, 2.6, 3.0, '#0f172a', '#f1f5f9',
         "• %100 Anonim Model Girdisi\n• SHA-256 Girdi Özeti\n• Sıfır Bulut Veri Sızıntısı\n• Güvenli Yerel LLM İcrası")
    ]

    for title, x, y, w, h, border, bg, desc in nodes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12",
                                      facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.32, title, fontsize=8, fontweight='bold', ha='center', color=border)
        ax.text(x + 0.16, y + 0.25, desc, fontsize=7.5, va='bottom', color='#1e293b', linespacing=1.35)

    arrow_props = dict(facecolor='#0f172a', edgecolor='none', width=1.6, headwidth=6, headlength=6)
    ax.annotate('', xy=(3.45, 3.3), xytext=(3.12, 3.3), arrowprops=arrow_props)
    ax.annotate('', xy=(6.65, 3.3), xytext=(6.32, 3.3), arrowprops=arrow_props)
    ax.annotate('', xy=(9.85, 3.3), xytext=(9.52, 3.3), arrowprops=arrow_props)

    # Alt Bilgi Çubuğu
    footer_rect = patches.FancyBboxPatch((0.5, 0.4), 12.0, 0.9, boxstyle="round,pad=0.04,rounding_size=0.08",
                                          facecolor='#0f172a', edgecolor='none')
    ax.add_patch(footer_rect)
    ax.text(6.5, 0.95, "KVKK MADDE 12 VE BDDK BİLGİ SİSTEMLERİ TEBLİĞİ GÜVENCESİ", 
            fontsize=8, fontweight='bold', ha='center', color='#ffffff')
    ax.text(6.5, 0.65, "Tüm PII anonimleştirme işlemleri yerel RAM bellekte gerçekleşir; disk üzerinde asla şifresiz kayıt tutulmaz.", 
            fontsize=7.2, ha='center', color='#cbd5e1')

    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.2)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("storage/diagrams/diag_03_engine_pii_security.png", bbox_inches='tight')
    plt.close()

# =========================================================================
# DİYAGRAM 4: Motor 3 — Dinamik Çevrimdışı Vektör RAG Topolojisi
# =========================================================================
def create_diagram_4():
    fig, ax = plt.subplots(figsize=(13, 6.2), dpi=300)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('#ffffff')

    ax.text(6.5, 5.8, "MOTOR 3: DİNAMİK ÇEVRİMD IŞI VEKTÖR RAG VE MEVZUAT EŞLEME MOTORU", 
            fontsize=13, fontweight='bold', ha='center', color='#0f172a')
    ax.text(6.5, 5.45, "ChromaDB Vektör Veritabanı, Hibrit Arama ve Tartışmasız Yasal Dayanak (Criteria) Enjeksiyonu", 
            fontsize=9.2, ha='center', color='#64748b')

    nodes = [
        ("1. MEVZUAT BİLGİ TABANI", 0.5, 1.8, 2.6, 3.0, '#7c3aed', '#f5f3ff',
         "• BDDK Kanunu & Tebliğleri\n• 5549 Sayılı MASAK Kanunu\n• SPK, TTK ve TCK Maddeleri\n• IIA Küresel Standartları 2026\n• COSO ERM İlkeleri"),
        
        ("2. VEKTÖR VE EMBEDDING", 3.5, 1.8, 2.8, 3.0, '#4f46e5', '#eef2ff',
         "• Hiyerarşik Chunking\n• Yerel Embedding Motoru\n• ChromaDB Vektör İndeksi\n• Sıfır İnternet / Çevrimdışı"),

        ("3. HİBRİT ARAMA MOTORU", 6.7, 1.8, 2.8, 3.0, '#0284c7', '#f0f9ff',
         "• Cosine Similarity Vektör Arama\n• TF-IDF Anahtar Kelime Arama\n• Dinamik Yeniden Sıralama\n• %95+ İlgililik Eşiği"),

        ("4. 5C CRITERIA ENJEKSİYONU", 9.9, 1.8, 2.6, 3.0, '#059669', '#ecfdf5',
         "• Tam Yasal Madde Metni\n• Resmi Ceza / Yaptırım Maddesi\n• Model Promptuna Otomatik Bağlantı\n• Savcılık / Komite Geçerliliği")
    ]

    for title, x, y, w, h, border, bg, desc in nodes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12",
                                      facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.32, title, fontsize=7.8, fontweight='bold', ha='center', color=border)
        ax.text(x + 0.16, y + 0.25, desc, fontsize=7.3, va='bottom', color='#1e293b', linespacing=1.35)

    arrow_props = dict(facecolor='#0f172a', edgecolor='none', width=1.6, headwidth=6, headlength=6)
    ax.annotate('', xy=(3.45, 3.3), xytext=(3.12, 3.3), arrowprops=arrow_props)
    ax.annotate('', xy=(6.65, 3.3), xytext=(6.32, 3.3), arrowprops=arrow_props)
    ax.annotate('', xy=(9.85, 3.3), xytext=(9.52, 3.3), arrowprops=arrow_props)

    # Alt Bilgi
    footer_rect = patches.FancyBboxPatch((0.5, 0.4), 12.0, 0.9, boxstyle="round,pad=0.04,rounding_size=0.08",
                                          facecolor='#0f172a', edgecolor='none')
    ax.add_patch(footer_rect)
    ax.text(6.5, 0.95, "HALÜSİNASYON ENGELLEME GÜVENCESİ (GROUNDED RAG)", 
            fontsize=8, fontweight='bold', ha='center', color='#ffffff')
    ax.text(6.5, 0.65, "Model mevzuat maddelerini uyduramaz; sadece yerel ChromaDB vektör kütüphanesindeki doğrulanmış metinleri alıntılar.", 
            fontsize=7.2, ha='center', color='#cbd5e1')

    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.2)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("storage/diagrams/diag_04_engine_rag_vector.png", bbox_inches='tight')
    plt.close()

# =========================================================================
# DİYAGRAM 5: Motor 4 — Otonom Karmaşıklık Yönlendirici (Auto-Tiering)
# =========================================================================
def create_diagram_5():
    fig, ax = plt.subplots(figsize=(13, 6.2), dpi=300)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('#ffffff')

    ax.text(6.5, 5.8, "MOTOR 4: OTONOM MODEL YÖNLENDİRİCİ (AUTO-TIERING) VE MODEL HAVUZU", 
            fontsize=13, fontweight='bold', ha='center', color='#0f172a')
    ax.text(6.5, 5.45, "Görev Zorluğu Analizi, Dinamik Tier Atama ve Yerel Model Havuzu Koordinasyonu", 
            fontsize=9.2, ha='center', color='#64748b')

    # Sol Giriş
    rect_in = patches.FancyBboxPatch((0.5, 2.0), 2.8, 2.6, boxstyle="round,pad=0.06,rounding_size=0.12",
                                      facecolor='#eff6ff', edgecolor='#2563eb', linewidth=1.8)
    ax.add_patch(rect_in)
    ax.text(1.9, 4.25, "GÖREV ANALİZİ & METAVERİ", fontsize=8, fontweight='bold', ha='center', color='#2563eb')
    ax.text(0.68, 2.3, "• Seçilen Denetim Görevi\n• Girdi Token Sayısı\n• İstenen Mantık Zorluğu\n• Kodlama Gereksinimi", 
            fontsize=7.5, va='bottom', color='#1e293b', linespacing=1.35)

    # Sağ Tier Kutuları
    tiers = [
        ("TIER 1: HAFİF ÇIKARIM", 6.2, 3.7, 6.3, 1.1, '#059669', '#ecfdf5',
         "• Model: Llama 3.2 (3B) / Qwen 2.5 (3B)  • Görev: Serbest Metinden Tablo Çıkarma (Görev 07)\n• Hız: 20 Saniye Altı  • Sıfır GPU Yükü  • Hafif Regex & JSON Parser"),

        ("TIER 2: STANDART MUHAKEME & 5C", 6.2, 2.4, 6.3, 1.1, '#2563eb', '#eff6ff',
         "• Model: Qwen 2.5 Coder (7B) / DeepSeek-R1 (8B)  • Görev: Denetim Evreni, RCM, 5C Bulgu (Görev 01-09)\n• Yüksek Mantık ve Mevzuat Uyumu  • IIA 5C Kural Seti İcrası"),

        ("TIER 3: İLERİ KODLAMA & ANALİTİK", 6.2, 1.1, 6.3, 1.1, '#7c3aed', '#f5f3ff',
         "• Model: Qwen 2.5 Coder (14B) / CodeLlama  • Görev: Python Pandas İstisna Kodu (Görev 10)\n• 25.000 Satırlık Veri Analitiği  • Sandbox Otomatik Kod Koşumu")
    ]

    for title, x, y, w, h, border, bg, desc in tiers:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.1",
                                      facecolor=bg, edgecolor=border, linewidth=1.6)
        ax.add_patch(rect)
        ax.text(x + 0.15, y + h - 0.28, title, fontsize=8, fontweight='bold', color=border)
        ax.text(x + 0.15, y + 0.15, desc, fontsize=7.2, va='bottom', color='#1e293b', linespacing=1.25)

    # Bağlantı Okları
    arrow_props = dict(facecolor='#0f172a', edgecolor='none', width=1.6, headwidth=6, headlength=6)
    ax.annotate('', xy=(6.15, 4.25), xytext=(3.35, 3.5), arrowprops=arrow_props)
    ax.annotate('', xy=(6.15, 2.95), xytext=(3.35, 3.3), arrowprops=arrow_props)
    ax.annotate('', xy=(6.15, 1.65), xytext=(3.35, 3.1), arrowprops=arrow_props)

    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.2)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("storage/diagrams/diag_05_engine_router_dispatcher.png", bbox_inches='tight')
    plt.close()

# =========================================================================
# DİYAGRAM 6: Motor 5 — İzole Python Sandbox ve Sürekli Analitik
# =========================================================================
def create_diagram_6():
    fig, ax = plt.subplots(figsize=(13, 6.2), dpi=300)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('#ffffff')

    ax.text(6.5, 5.8, "MOTOR 5: İZOLE PYTHON SANDBOX VE SÜREKLİ ANALİTİK MOTORU", 
            fontsize=13, fontweight='bold', ha='center', color='#0f172a')
    ax.text(6.5, 5.45, "Güvenli Subprocess Yürütme, AST Statik Analizi ve Otomatik Çok Sekmeli Excel Raporlama", 
            fontsize=9.2, ha='center', color='#64748b')

    nodes = [
        ("1. VERİ & LLM SCRIPTİ", 0.5, 1.8, 2.6, 3.0, '#0284c7', '#f0f9ff',
         "• 25.000 Satır Banka Verisi\n• Qwen 2.5 Coder Scripti\n• LTV / MASAK Anomali Filtresi\n• Ham Python Kod Bloğu"),
        
        ("2. AST GÜVENLİK DENETİMİ", 3.5, 1.8, 2.8, 3.0, '#dc2626', '#fef2f2',
         "• Soyut Sözdizim Ağacı (AST)\n• Yasaklı Kütüphane Engeli:\n  (os.system, socket, eval)\n• Salt Pandas & NumPy İzni\n• Bellek Sınırı (512 MB)"),

        ("3. İZOLE SUBPROCESS İCRASI", 6.7, 1.8, 2.8, 3.0, '#059669', '#ecfdf5',
         "• Geçici Temp Çalışma Alanı\n• Sıfır Ağ İletişimi\n• Canlı Terminal Log Yakalama\n• 30 Saniye Zaman Aşımı"),

        ("4. İSTİSNA EXCEL RAPORU", 9.9, 1.8, 2.6, 3.0, '#d97706', '#fffbeb',
         "• audit_exceptions.xlsx\n• LTV_Breach Sekmesi\n• MASAK_Bypass Sekmesi\n• Anomali Özet İstatistiği\n• Tek Tıkla İndirme Butonu")
    ]

    for title, x, y, w, h, border, bg, desc in nodes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12",
                                      facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.32, title, fontsize=7.8, fontweight='bold', ha='center', color=border)
        ax.text(x + 0.16, y + 0.25, desc, fontsize=7.3, va='bottom', color='#1e293b', linespacing=1.35)

    arrow_props = dict(facecolor='#0f172a', edgecolor='none', width=1.6, headwidth=6, headlength=6)
    ax.annotate('', xy=(3.45, 3.3), xytext=(3.12, 3.3), arrowprops=arrow_props)
    ax.annotate('', xy=(6.65, 3.3), xytext=(6.32, 3.3), arrowprops=arrow_props)
    ax.annotate('', xy=(9.85, 3.3), xytext=(9.52, 3.3), arrowprops=arrow_props)

    # Alt Bilgi
    footer_rect = patches.FancyBboxPatch((0.5, 0.4), 12.0, 0.9, boxstyle="round,pad=0.04,rounding_size=0.08",
                                          facecolor='#0f172a', edgecolor='none')
    ax.add_patch(footer_rect)
    ax.text(6.5, 0.95, "SİSTEM GÜVENLİĞİ VE İZOLASYON GARANTİSİ", 
            fontsize=8, fontweight='bold', ha='center', color='#ffffff')
    ax.text(6.5, 0.65, "Sandbox yalnızca denetçi arayüzden onay verdiğinde çalışır; sistem dosyalarını ve işletim sistemini asla değiştiremez.", 
            fontsize=7.2, ha='center', color='#cbd5e1')

    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.2)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("storage/diagrams/diag_06_engine_sandbox_analytics.png", bbox_inches='tight')
    plt.close()

# =========================================================================
# DİYAGRAM 7: Motor 6 — IIA 5C Kalite Değerlendirici ve Çoklu Format İhracı
# =========================================================================
def create_diagram_7():
    fig, ax = plt.subplots(figsize=(13, 6.2), dpi=300)
    ax.set_facecolor('#f8fafc')
    fig.patch.set_facecolor('#ffffff')

    ax.text(6.5, 5.8, "MOTOR 6: IIA 5C KALİTE DEĞERLENDİRİCİ VE SİSTEM ÇIKTI MOTORU", 
            fontsize=13, fontweight='bold', ha='center', color='#0f172a')
    ax.text(6.5, 5.45, "5C Eksiksizlik Denetimi, Kalite Skoru Puanlama ve Resmi Kurumsal Belge Üretimi", 
            fontsize=9.2, ha='center', color='#64748b')

    nodes = [
        ("1. MODEL ÇIKTI BELGESİ", 0.5, 1.8, 2.6, 3.0, '#4f46e5', '#eef2ff',
         "• Üretilen Çalışma Kağıdı\n• Risk ve Kontrol Listeleri\n• Sayısal Tablo Verileri\n• Örneklem Test Sonuçları"),
        
        ("2. IIA QA/QC DEĞERLENDİRİCİ", 3.5, 1.8, 2.8, 3.0, '#059669', '#ecfdf5',
         "• 5C Kontrolü (Durum, Kriter,\n  Kök Neden, Etki, Öneri)\n• 0-100 Kalite Skoru\n• 95/100 Mükemmel Rozeti\n• Eksik Alan Tespiti & Düzeltme"),

        ("3. FORMATLAMA ŞABLONLARI", 6.7, 1.8, 2.8, 3.0, '#0284c7', '#f0f9ff',
         "• python-docx Kurumsal Antet\n• openpyxl Zebra Izgara Çizgisi\n• ReportLab Vektör PDF Motoru\n• SHA-256 Dijital Mühür"),

        ("4. RESMİ DENETİM BELGELERİ", 9.9, 1.8, 2.6, 3.0, '#0f172a', '#f1f5f9',
         "• Resmi Word (.docx)\n• Formatlı Excel (.xlsx)\n• İstisna Raporu (.xlsx)\n• Değiştirilemez JSON İzi\n• Komiteye Sunuma Hazır")
    ]

    for title, x, y, w, h, border, bg, desc in nodes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.12",
                                      facecolor=bg, edgecolor=border, linewidth=1.8)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.32, title, fontsize=7.8, fontweight='bold', ha='center', color=border)
        ax.text(x + 0.16, y + 0.25, desc, fontsize=7.3, va='bottom', color='#1e293b', linespacing=1.35)

    arrow_props = dict(facecolor='#0f172a', edgecolor='none', width=1.6, headwidth=6, headlength=6)
    ax.annotate('', xy=(3.45, 3.3), xytext=(3.12, 3.3), arrowprops=arrow_props)
    ax.annotate('', xy=(6.65, 3.3), xytext=(6.32, 3.3), arrowprops=arrow_props)
    ax.annotate('', xy=(9.85, 3.3), xytext=(9.52, 3.3), arrowprops=arrow_props)

    # Alt Bilgi
    footer_rect = patches.FancyBboxPatch((0.5, 0.4), 12.0, 0.9, boxstyle="round,pad=0.04,rounding_size=0.08",
                                          facecolor='#0f172a', edgecolor='none')
    ax.add_patch(footer_rect)
    ax.text(6.5, 0.95, "IIA STANDART 2400 VE 2420 RESMİ RAPORLAMA UYUMU", 
            fontsize=8, fontweight='bold', ha='center', color='#ffffff')
    ax.text(6.5, 0.65, "Tüm ihraç edilen belgeler Denetim Komitesi ve Savcılık teftiş dosyalarında doğrudan kullanılabilir standarttadır.", 
            fontsize=7.2, ha='center', color='#cbd5e1')

    ax.set_xlim(0, 13)
    ax.set_ylim(0, 6.2)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("storage/diagrams/diag_07_engine_qa_exporter.png", bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_diagram_1()
    create_diagram_2()
    create_diagram_3()
    create_diagram_4()
    create_diagram_5()
    create_diagram_6()
    create_diagram_7()
    print("✅ 7 Adet Kurumsal Sistem ve Motor Topoloji Diyagramı Başarıyla Oluşturuldu!")
