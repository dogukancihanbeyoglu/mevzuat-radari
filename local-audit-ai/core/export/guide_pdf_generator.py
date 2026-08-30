"""
Auditoris — 10 Görev Türünün Tamamını Kapsayan Master Kullanıcı Kılavuzu & Sistem Çıktı Rehberi
7 Adet Yüksek Çözünürlüklü Mimari & Motor Topoloji Diyagramı, 10 Canlı UI Ekran Görüntüsü, 4 Somut Sistem Çıktı Örneği ve Ham Veri Erişim Kılavuzu
%100 Türkçe Karakter Desteği (Arial TTF) ve Profesyonel A4 Tipografi Mimarisi
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Türkçe Arial TTF Fontlarını Yükleme
try:
    pdfmetrics.registerFont(TTFont('Arial', '/System/Library/Fonts/Supplemental/Arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Italic', '/System/Library/Fonts/Supplemental/Arial Italic.ttf'))
    FONT_NORMAL = 'Arial'
    FONT_BOLD = 'Arial-Bold'
    FONT_ITALIC = 'Arial-Italic'
except Exception as e:
    print(f"TTF Font yüklenemedi, varsayılana geçiliyor: {e}")
    FONT_NORMAL = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'
    FONT_ITALIC = 'Helvetica-Oblique'

class NumberedCanvas(canvas.Canvas):
    """Her sayfanın altına dinamik 'Sayfa X / Y' bilgisi basar."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont(FONT_NORMAL, 8)
        self.setFillColor(colors.HexColor('#64748b'))
        self.setStrokeColor(colors.HexColor('#e2e8f0'))
        self.setLineWidth(0.5)
        self.line(30, 24, A4[0] - 30, 24)
        
        footer_text = f"Auditoris Enterprise AI — Master Kullanıcı Kılavuzu & Sistem Çıktı Rehberi | Sayfa {self._pageNumber} / {page_count}"
        self.drawString(30, 13, footer_text)
        self.drawRightString(A4[0] - 30, 13, "Geliştirici & Sistem Mimarı: Doğukan Cihanbeyoğlu")
        self.restoreState()

def generate_user_guide_pdf(output_pdf_path: str = "storage/Auditoris_Kullanici_Kilavuzu_2026.pdf") -> str:
    """
    10 Görev Türünü, 7 Ayrı Mimari ve Motor Topoloji Diyagramını,
    Tüm Canlı Sonuç Ekran Görüntülerini ve Somut Sistem Çıktı Örneklerini Kapsayan Master PDF Kılavuzu.
    """
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    screenshot_dir = "storage/screenshots"
    diagram_dir = "storage/diagrams"

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        rightMargin=28,
        leftMargin=28,
        topMargin=26,
        bottomMargin=34
    )

    styles = getSampleStyleSheet()

    # Tipografi Stilleri
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName=FONT_BOLD,
        fontSize=15,
        leading=18.5,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=2
    )
    
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName=FONT_NORMAL,
        fontSize=7.6,
        leading=10.8,
        textColor=colors.HexColor('#475569'),
        spaceAfter=5
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName=FONT_BOLD,
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=4,
        spaceAfter=3,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName=FONT_BOLD,
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=3,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName=FONT_NORMAL,
        fontSize=7.2,
        leading=9.8,
        textColor=colors.HexColor('#334155'),
        spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName=FONT_NORMAL,
        fontSize=7.1,
        leading=9.8,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=8,
        firstLineIndent=-5,
        spaceAfter=2
    )

    table_header_style = ParagraphStyle(
        'TH_Style',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=6.6,
        leading=9,
        textColor=colors.HexColor('#ffffff')
    )

    table_cell_style = ParagraphStyle(
        'TC_Style',
        parent=styles['Normal'],
        fontName=FONT_NORMAL,
        fontSize=6.6,
        leading=9,
        textColor=colors.HexColor('#1e293b')
    )

    caption_style = ParagraphStyle(
        'Caption_Style',
        parent=styles['Normal'],
        fontName=FONT_ITALIC,
        fontSize=6.6,
        leading=8.5,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_CENTER,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Style',
        parent=styles['Normal'],
        fontName=FONT_NORMAL,
        fontSize=6.3,
        leading=8.5,
        textColor=colors.HexColor('#0f172a'),
        leftIndent=4,
        rightIndent=4,
        spaceBefore=2,
        spaceAfter=2
    )

    elements = []

    # =========================================================================
    # BÖLÜM 1: GENEL SİSTEM MİMARİ VE GÜVENLİK TOPOLOJİSİ
    # =========================================================================
    elements.append(Paragraph("🏛️ AUDİTORİS 2026 — MASTER KULLANICI KILAVUZU & SİSTEM ÇIKTI REHBERİ", title_style))
    elements.append(Paragraph("<b>Sürüm:</b> 2026.1 Enterprise AI | <b>Metodoloji:</b> IIA Küresel Standartları (2026 Evolution) & COSO ERM<br/><b>Geliştirici & Sistem Mimarı:</b> Doğukan Cihanbeyoğlu | <b>Güvenlik Modeli:</b> %100 Yerel / Çevrimdışı (Air-Gapped)", meta_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0f172a'), spaceAfter=4))

    elements.append(Paragraph("1. GENEL SİSTEM TOPOLOJİSİ VE HAVA BOŞLUKLU (AIR-GAPPED) ÇALIŞMA PRENSİBİ", h1_style))
    elements.append(Paragraph(
        "Auditoris; hassas kurumsal finans, teftiş ve müşteri verilerinin hiçbir şekilde harici bulut sunucularına "
        "aktarılmadığı, tamamen kurum içi yerel donanımda çalışan profesyonel bir İç Denetim Yapay Zeka İşletim Sistemidir. "
        "Sistem, 6 bağımsız güvenlik ve analiz katmanının senkronize çalışmasıyla resmi denetim çalışma kağıdı çıktılarını üretir:",
        body_style
    ))

    diag1_p = os.path.join(diagram_dir, "diag_01_system_topology.png")
    if os.path.exists(diag1_p):
        elements.append(Image(diag1_p, width=540, height=210))
        elements.append(Paragraph("Diyagram 1.1: Auditoris Hava Boşluklu (Air-Gapped) Uçtan Uca Sistem ve Güvenlik Topolojisi", caption_style))

    engine_summary = [
        [Paragraph("Katman / Motor", table_header_style), Paragraph("Teknik İşlevi (Arka Planda Ne Çalışır?)", table_header_style), Paragraph("Denetçiye ve Kuruma Sağladığı Güvence", table_header_style)],
        [Paragraph("1. Client UI & Kokpit", table_cell_style), Paragraph("5 aşama ve 10 görev türü için optimize edilmiş reaktif Streamlit kokpiti.", table_cell_style), Paragraph("Kullanıcı dostu, hızlı ve hatasız görev seçimi.", table_cell_style)],
        [Paragraph("2. PII Masker (KVKK/GDPR)", table_cell_style), Paragraph("TCKN, IBAN, Kredi Kartı ve e-postaları deterministik olarak şifreler.", table_cell_style), Paragraph("Sıfır veri sızıntısı güvencesi (%100 yerel koruma).", table_cell_style)],
        [Paragraph("3. Model Router (Tiering)", table_cell_style), Paragraph("Görev türüne göre Tier 1 (3B), Tier 2 (7B-8B) veya Tier 3 (14B) atar.", table_cell_style), Paragraph("Doğru göreve en optimum yerel modelin atanması.", table_cell_style)],
        [Paragraph("4. Offline Vektör RAG", table_cell_style), Paragraph("ChromaDB ile BDDK, MASAK, SPK, TTK ve IIA mevzuatını tarar.", table_cell_style), Paragraph("Bulgulara tartışmasız resmi yasal dayanak (Criteria).", table_cell_style)],
        [Paragraph("5. Local Python Sandbox", table_cell_style), Paragraph("Modelin ürettiği Pandas kodlarını izole subprocess içinde koşturur.", table_cell_style), Paragraph("25.000+ satırlık tablolardan hatasız Excel istisna dökümü.", table_cell_style)],
        [Paragraph("6. Audit Trail & Çıktı Motoru", table_cell_style), Paragraph("SHA-256 kriptografik imza üretir; Word, Excel ve JSON üretir.", table_cell_style), Paragraph("Değiştirilemez denetim kanıtı ve resmi sistem çıktı formatları.", table_cell_style)]
    ]

    t_summary = Table(engine_summary, colWidths=[110, 250, 180])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
    ]))
    elements.append(t_summary)

    # =========================================================================
    # BÖLÜM 2: 5 AŞAMA VE 10 GÖREV İŞ AKIŞI TOPOLOJİSİ
    # =========================================================================
    elements.append(PageBreak())
    elements.append(Paragraph("2. 5 DENETİM AŞAMASI VE 10 GÖREV TÜRÜ İŞ AKIŞ TOPOLOJİSİ", h1_style))
    elements.append(Paragraph(
        "Auditoris, Uluslararası İç Denetçiler Enstitüsü (IIA) Küresel Standartları ve COSO İç Kontrol Çerçevesi "
        "tarafından tanımlanan 5 temel aşama ve 10 spesifik denetim görevini uçtan uca kapsar:",
        body_style
    ))

    diag2_p = os.path.join(diagram_dir, "diag_02_five_phase_lifecycle.png")
    if os.path.exists(diag2_p):
        elements.append(Image(diag2_p, width=540, height=210))
        elements.append(Paragraph("Diyagram 1.2: IIA Uyumlu 5 Denetim Aşaması ve 10 Görev Türü Uçtan Uca Süreç Döngüsü", caption_style))

    phase_table = [
        [Paragraph("Aşama No & Adı", table_header_style), Paragraph("Kapsanan Görev Türleri", table_header_style), Paragraph("Temel Çıktı ve Standart Hedefi", table_header_style)],
        [
            Paragraph("<b>1. Yıllık Planlama</b><br/>(Annual Planning)", table_cell_style),
            Paragraph("• Görev 01: Denetim Evreni & Risk Derecelendirmesi<br/>• Görev 02: Kaynak ve Yetkinlik Planlaması (Competency)", table_cell_style),
            Paragraph("Risk odaklı 1 yıllık teftiş takvimi ve denetçi adam/gün bütçesi (IIA Standart 2010/2030).", table_cell_style)
        ],
        [
            Paragraph("<b>2. Görev Planlama</b><br/>(Engagement Planning)", table_cell_style),
            Paragraph("• Görev 03: Risk Kontrol Matrisi (RCM) & Walkthrough<br/>• Görev 04: Görev Kapsam Dokümanı (Engagement Scoping)", table_cell_style),
            Paragraph("Süreç bazlı risk ve kontrol envanteri, mülakat soruları ve kapsam sınırları memosu (IIA Standart 2200).", table_cell_style)
        ],
        [
            Paragraph("<b>3. Saha Çalışması</b><br/>(Fieldwork & Testing)", table_cell_style),
            Paragraph("• Görev 05: Kontrol Test Prosedürü Geliştirme<br/>• Görev 06: Kontrol Tanımı ve Tasarım Zayıflığı Analizi<br/>• Görev 07: Serbest Metinden Veri Ayıklama", table_cell_style),
            Paragraph("Örneklem metotlu test programları, SoD tasarım analizleri ve dağınık saha notlarından yapılandırılmış veri üretimi (IIA 2300).", table_cell_style)
        ],
        [
            Paragraph("<b>4. Denetim Raporlama</b><br/>(Audit Reporting)", table_cell_style),
            Paragraph("• Görev 08: 5C Standart Denetim Bulgusu Yazımı<br/>• Görev 09: Yönetim Kurulu & Denetim Komitesi Özeti", table_cell_style),
            Paragraph("IIA 5C Kuralında (Condition, Criteria, Cause, Effect, Recommendation) resmi bulgular ve üst yönetim brifingi (IIA 2400).", table_cell_style)
        ],
        [
            Paragraph("<b>5. Sürekli Analitik</b><br/>(Continuous Analytics)", table_cell_style),
            Paragraph("• Görev 10: Python (Pandas) İstisna Kodu & Canlı Sandbox", table_cell_style),
            Paragraph("Milyonlarca satırlık ham bankacılık/muhasebe verisinde otomatik anomali tespiti ve çok sekmeli Excel üretimi.", table_cell_style)
        ]
    ]

    t_phase = Table(phase_table, colWidths=[105, 235, 200])
    t_phase.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
    ]))
    elements.append(t_phase)

    # =========================================================================
    # BÖLÜM 3.1: MOTOR 1 & 2 — SMART EVIDENCE EXTRACTOR VE PII MASKELEME
    # =========================================================================
    elements.append(PageBreak())
    elements.append(Paragraph("3. ÇEKİRDEK MOTORLARIN TEKNİK ÇALIŞMA TOPOLOJİLERİ", h1_style))
    elements.append(Paragraph("3.1 Motor 1 & 2: Smart Evidence Extractor ve PII Maskeleme Motoru Topolojisi", h2_style))
    elements.append(Paragraph(
        "Denetçinin sisteme yüklediği 25.000+ satırlık büyük tablolarda modelin token sınırını aşmaması ve "
        "müşteri sırrı / kişisel verilerin (KVKK/GDPR) korunması için iki aşamalı süzme ve maskeleme uygulanır:",
        body_style
    ))

    diag3_p = os.path.join(diagram_dir, "diag_03_engine_pii_security.png")
    if os.path.exists(diag3_p):
        elements.append(Image(diag3_p, width=540, height=205))
        elements.append(Paragraph("Diyagram 2.1: Deterministik Regex PII Maskeleme ve Smart Evidence Süzme Motoru Akışı", caption_style))

    pii_details = [
        "<b>Smart Evidence Süzgeci:</b> Büyük veri setlerinden yalnızca limit aşımı, SoD çakışması ve MASAK şüpheli işlem kriterlerine uyan satırları çekerek token tüketimini %85 oranında azaltır.",
        "<b>Deterministik Regex Masker:</b> TCKN (11 hane), IBAN (TR+24 hane), Kredi Kartı (16 hane), e-posta ve telefon numaraları yerel bellekte <code>[TCKN_1]</code>, <code>[IBAN_1]</code> şeklinde şifrelenir.",
        "<b>Ters Eşleme Bellek Sözlüğü:</b> Çıktı üretildiğinde çalışma kağıdının denetçi tarafından okunabilmesi için eşleme sadece yerel oturum belleğinde tutulur; diske asla şifresiz veri yazılmaz."
    ]
    for pd in pii_details:
        elements.append(Paragraph(f"• {pd}", bullet_style))

    # =========================================================================
    # BÖLÜM 3.2: MOTOR 3 — DİNAMİK ÇEVRİMDIŞI VEKTÖR RAG
    # =========================================================================
    elements.append(PageBreak())
    elements.append(Paragraph("3.2 Motor 3: Dinamik Çevrimdışı Vektör RAG ve Mevzuat Eşleme Topolojisi", h2_style))
    elements.append(Paragraph(
        "Auditoris, üretilen tüm çalışma kağıtları ve bulguların resmi dayanağını (Criteria) oluşturmak için "
        "ChromaDB vektör kütüphanesini ve TF-IDF hibrit arama motorunu kullanır:",
        body_style
    ))

    diag4_p = os.path.join(diagram_dir, "diag_04_engine_rag_vector.png")
    if os.path.exists(diag4_p):
        elements.append(Image(diag4_p, width=540, height=205))
        elements.append(Paragraph("Diyagram 2.2: Çevrimdışı Vektör RAG, MiniLM Embedding ve Hibrit Mevzuat Eşleme Motoru", caption_style))

    rag_details = [
        "<b>Hiyerarşik Vektör İndeksleme:</b> BDDK, MASAK, SPK, TTK, KVKK ve IIA mevzuat dokümanları maddeler ve fıkralar halinde bölünerek yerel ChromaDB vektör kütüphanesine kaydedilmiştir.",
        "<b>Hibrit Arama (Cosine + TF-IDF):</b> Saha notlarındaki terimler (örneğin 'kredi zimmeti', 'LTV aşımı', 'yetkisiz işlem') hem anlamsal (vektör) hem de tam anahtar kelime eşleşmesiyle taranır.",
        "<b>Halüsinasyon Engelleme (Grounding):</b> Model mevzuat uyduramaz; yalnızca RAG tarafından getirilen doğrulanmış kanun metinlerini çalışma kağıdına aktarır."
    ]
    for rd in rag_details:
        elements.append(Paragraph(f"• {rd}", bullet_style))

    # =========================================================================
    # BÖLÜM 3.3: MOTOR 4 — OTONOM KARMAŞIKLIK YÖNLENDİRİCİ (AUTO-TIERING)
    # =========================================================================
    elements.append(PageBreak())
    elements.append(Paragraph("3.3 Motor 4: Otonom Model Yönlendirici (Auto-Tiering) ve Model Havuzu", h2_style))
    elements.append(Paragraph(
        "Auditoris, yerel donanımda kurulu modelleri otonom olarak analiz eder ve seçilen görevin mantıksal "
        "karmaşıklığına göre en ideal Tier ve model eşleştirmesini dinamik olarak gerçekleştirir:",
        body_style
    ))

    diag5_p = os.path.join(diagram_dir, "diag_05_engine_router_dispatcher.png")
    if os.path.exists(diag5_p):
        elements.append(Image(diag5_p, width=540, height=205))
        elements.append(Paragraph("Diyagram 2.3: Complexity Router Karar Ağacı, Auto-Tiering ve Model Havuzu Koordinasyonu", caption_style))

    router_details = [
        "<b>Tier 1 (Hafif / Veri Ayıklama):</b> <code>llama3.2:3b</code> veya <code>qwen2.5:3b</code> modelleri atanır. Görev 07 gibi serbest metinden tablo çıkarma işlerinde 20 saniyenin altında ultra hızlı çalışır.",
        "<b>Tier 2 (Standart / 5C & Muhakeme):</b> <code>qwen2.5-coder:7b</code> veya <code>deepseek-r1:8b</code> modelleri atanır. RCM, test prosedürü ve 5C bulgu yazımı gibi yüksek mantık gerektiren görevlerde çalışır.",
        "<b>Tier 3 (İleri Düzey / Python & Analitik):</b> <code>qwen2.5-coder:14b</code> gibi uzman kodlama modellerine atanır. 25.000 satırlık veri analitiğinde ve Python kod üretiminde çalışır.",
        "<b>Otonom Fallback Motoru:</b> Model yanıt veremez veya zaman aşımına girerse, sistem deterministik fallback motorunu devreye sokarak denetçiyi asla cevapsız bırakmaz."
    ]
    for rd in router_details:
        elements.append(Paragraph(f"• {rd}", bullet_style))

    # =========================================================================
    # BÖLÜM 3.4 & 3.5: MOTOR 5 & 6 — PYTHON SANDBOX VE KALİTE DEĞERLENDİRİCİ
    # =========================================================================
    elements.append(PageBreak())
    elements.append(Paragraph("3.4 Motor 5: İzole Python Sandbox ve Sürekli Analitik Motoru Topolojisi", h2_style))
    elements.append(Paragraph(
        "Sürekli denetim aşamasında (Görev 10) üretilen Python analiz kodlarının güvenle icra edilebilmesi için "
        "AST denetimli ve geçici subprocess tabanlı izole bir Sandbox ortamı kullanılır:",
        body_style
    ))

    diag6_p = os.path.join(diagram_dir, "diag_06_engine_sandbox_analytics.png")
    if os.path.exists(diag6_p):
        elements.append(Image(diag6_p, width=540, height=195))
        elements.append(Paragraph("Diyagram 2.4: İzole Python Sandbox, AST Güvenlik Filtresi ve İstisna Raporlama Akışı", caption_style))

    elements.append(Spacer(1, 4))
    elements.append(Paragraph("3.5 Motor 6: IIA 5C Kalite Değerlendirici ve Sistem Çıktı Motoru", h2_style))
    diag7_p = os.path.join(diagram_dir, "diag_07_engine_qa_exporter.png")
    if os.path.exists(diag7_p):
        elements.append(Image(diag7_p, width=540, height=195))
        elements.append(Paragraph("Diyagram 2.5: IIA 5C Kalite Kontrolü, SHA-256 Dijital İmzası ve Sistem Çıktı Formatları", caption_style))

    # =========================================================================
    # BÖLÜM 4: 10 GÖREVİN CANLI UI EKRANLARI VE OPERASYONEL KULLANIMI
    # =========================================================================
    tasks_guide_info = [
        {
            "num": "1",
            "phase": "1. YILLIK PLANLAMA",
            "title": "Görev 01: Denetim Evreni ve Risk Derecelendirmesi (Audit Universe)",
            "img": "task_01_audit_universe.png",
            "caption": "Ekran Görüntüsü 1.1: Denetim Evreni — 5 İştirak Risk Skorlama ve Denetim Frekans Dağılımı",
            "desc": "Holding bünyesindeki 5 ana sektör ve 5 iştirak şirketin (Finansman, Enerji, Teknoloji, GYO, Lojistik) ciroları, regülasyon baskısı ve kontrol olgunluğuna göre risk derecelendirmesi.",
            "backend": "Tier 2 (`qwen2.5-coder:7b`) modeli; COSO ERM matrisini ve IIA Standart 2010 kurallarını Offline RAG ile birleştirerek 5 iştirak için Birleşik Risk Skoru hesaplar.",
            "action": "Arayüzde 1. Aşama ve Görev seçilip holding finansal verileri girildi; 'Çalışma Kağıdını Üret' butonuna basıldı.",
            "result": "95/100 Kalite Skoru, 94-45 puan arası iştirak risk skorları, Denetim Frekans Tablosu ve Word/Excel indirme butonları ekrana yansıdı."
        },
        {
            "num": "2",
            "phase": "1. YILLIK PLANLAMA",
            "title": "Görev 02: Kaynak ve Yetkinlik Planlaması (Resource Mapping)",
            "img": "task_02_resource_competency_mapping.png",
            "caption": "Ekran Görüntüsü 1.2: Kaynak Planlama — Ekip Yetkinlik Matrisi ve Dış Kaynak (Outsource) Stratejisi",
            "desc": "12 kişilik denetim kadrosunun Finans, IT, ESG ve Operasyonel yetkinlik puanlarına göre 2026 yılı 18 projesinin adam/gün ve uzmanlık açığı planlaması.",
            "backend": "IIA Standart 2030 (Kaynak Yönetimi) ve Standart 2050 (Koordinasyon) yönergeleri kullanılarak yetkinlik açığı optimizasyonu yapılır.",
            "action": "Ekip üyelerinin uzmanlık skorları girildi; modelin kaynak açığı analizi yapması sağlandı.",
            "result": "ESG alanındaki 1.2/5.0 kritik yetkinlik açığı için %100 Outsourcing, Bulut Güvenliği için Co-sourcing önerisi ve adam/gün dağılım tablosu üretildi."
        },
        {
            "num": "3",
            "phase": "2. GÖREV PLANLAMA",
            "title": "Görev 03: Risk ve Kontrol Matrisi (RCM) & Walkthrough",
            "img": "task_03_rcm_generation.png",
            "caption": "Ekran Görüntüsü 1.3: RCM — Hazine & Swap Operasyonları Risk Kontrol Matrisi ve Mülakat Soruları",
            "desc": "Hazine ve Swap işlemlerinde 5M USD yetkisiz limit aşımı, SoD çakışması ve Stop-Loss manuel bypass risklerine karşı 6 sütunlu RCM ve walkthrough soruları.",
            "backend": "Tier 2 muhakeme modeli BDDK Hazine İlkeleri ve Basel III kurallarını vektör kütüphaneden çekerek kontrol tasarımını oluşturur.",
            "action": "Hazine masası risk senaryoları yapıştırıldı; model RCM matrisi oluşturdu.",
            "result": "Risk No, Kontrol Faaliyeti, Tür (Önleyici/Tespit Edici), Sıklık, Test Adımları ve Süreç Sahibine Yöneltilecek 3 adet Walkthrough sorusu üretildi."
        },
        {
            "num": "4",
            "phase": "2. GÖREV PLANLAMA",
            "title": "Görev 04: Görev Kapsam Dokümanı (Engagement Scoping Memo)",
            "img": "task_04_scoping_document.png",
            "caption": "Ekran Görüntüsü 1.4: Scoping — E-Ticaret ve Pazaryeri Operasyonları Kapsam İçi / Dışı Sınırları",
            "desc": "E-Ticaret ve Sanal POS operasyonları denetiminde fraud, kargo mutabakatı ve KVKK kapsam içine alınırken fiziki mağaza sayımları kapsam dışı bırakılmıştır.",
            "backend": "IIA Standart 2200 (Görev Planlama) yönergeleriyle hedefler, kilit paydaşlar, riskli alanlar ve zaman planı resmi memo formatında derlenir.",
            "action": "E-ticaret saha parametreleri girildi; kapsam sınırları belirlendi.",
            "result": "Kapsam İçi / Kapsam Dışı açık tablosu, denetim hedefleri ve 3 haftalık saha takvimi üretildi."
        },
        {
            "num": "5",
            "phase": "3. SAHA ÇALIŞMASI",
            "title": "Görev 05: Kontrol Test Prosedürü Geliştirme",
            "img": "task_05_test_procedure.png",
            "caption": "Ekran Görüntüsü 1.5: Test Prosedürü — 2.5M TL Üzeri Faturalarda 3'lü Eşleştirme ve Çift İmza Test Planı",
            "desc": "4.200 satınalma faturasından Parasal Birim Örneklemesi (MUS) ile seçilen yüksek tutarlı işlemlerde SAP ME23N/MIGO/MT-103 kontrol adımları.",
            "backend": "IIA 2300 gereğince 4-Ögeli Standart Test Planı (Amaç, Örneklem, Test Adımları, Hata Kriteri) formüle edilir.",
            "action": "Satınalma fatura parametreleri girildi; test prosedürü üretildi.",
            "result": "%95 Güven Düzeyinde 25 adet yüksek tutarlı fatura örneklemi, adım adım SAP ekran testleri ve sapma değerlendirme kriteri oluşturuldu."
        },
        {
            "num": "6",
            "phase": "3. SAHA ÇALIŞMASI",
            "title": "Görev 06: Kontrol Tanımı ve Tasarım Zayıflığı Analizi",
            "img": "task_06_control_analysis.png",
            "caption": "Ekran Görüntüsü 1.6: Tasarım Zafiyeti — Sözlü Talimat ve Gevşek Limit Kontrol Açığı Değerlendirmesi",
            "desc": "Hazine uzmanının telefonla sözlü talimatla 500.000 EUR döviz alımı yapabilmesine izin veren gevşek kontrolün tasarım zafiyetleri ve sağlamlaştırılması.",
            "backend": "COSO Kontrol Faaliyetleri ve SoD (Görevler Ayrılığı) matrisi taranarak tasarım açığı eleştirilir.",
            "action": "Gevşek kontrol tanımı girildi; tasarım açıkları analiz ettirildi.",
            "result": "SoD eksikliği ve muğlak volatilite eşiği eleştirildi; FIDO2 MFA onaylı sağlamlaştırılmış alternatif kontrol tanımı üretildi."
        },
        {
            "num": "7",
            "phase": "3. SAHA ÇALIŞMASI",
            "title": "Görev 07: Yapılandırılmamış Metinden Veri Ayıklama (Data Extraction)",
            "img": "task_07_data_extraction.png",
            "caption": "Ekran Görüntüsü 1.7: Veri Ayıklama — Serbest Metin Saha Notlarından 7 Sütunlu Temiz Tablo Üretimi",
            "desc": "Dağınık fatura numaraları (OFF-INV-088), offshore ülkeleri (BVI, Cyprus), tutarlar ve MASAK şüphe durumlarının serbest metinden temiz tabloya dönüştürülmesi.",
            "backend": "Tier 1 Hızlı Çıkarım Modeli (`llama3.2:3b`) deterministik regex ve varlık tanıma ile çalışır. Süre: 20.9 sn.",
            "action": "Serbest metin saha notları yapıştırıldı; veri ayıklama çalıştırıldı.",
            "result": "7 sütunlu yapılandırılmış tablo üretildi; şüpheli offshore transferler kırmızı uyarı rozetleriyle ayrıştırıldı."
        },
        {
            "num": "8",
            "phase": "4. DENETİM RAPORLAMA",
            "title": "Görev 08: 5C Standart Denetim Bulgusu Yazımı (Finding 5C)",
            "img": "task_08_finding_5c.png",
            "caption": "Ekran Görüntüsü 1.8: 5C Bulgu — 145M TL Kredi Zimmeti ve 78.5M TL Panama Kaçakçılığı Raporu",
            "desc": "145M TL teminatsız yetkisiz kredi tahsisi, sahte ekspertiz (%850 LTV) ve Panama'ya aktarılan 78.5M TL MASAK kaçakçılığı için resmi 5C bulgu yazımı.",
            "backend": "5411 Sayılı Bankacılık Kanunu Madde 160 (Zimmet) ve 5549 Sayılı MASAK Kanunu Madde 8/13 mevzuat kuralları enjekte edilir.",
            "action": "Saha tespitleri ve mevzuat maddeleri girildi; 5C bulgu üretildi.",
            "result": "Condition (Durum), Criteria (Kriter), Cause (Kök Neden), Effect (Etki), Recommendation (Öneri) eksiksiz üretildi; Savcılık suç duyurusu maddesi bağlandı."
        },
        {
            "num": "9",
            "phase": "4. DENETİM RAPORLAMA",
            "title": "Görev 09: Yönetim Kurulu ve Denetim Komitesi Özeti",
            "img": "task_09_executive_summary.png",
            "caption": "Ekran Görüntüsü 1.9: Yönetici Özeti — Denetim Komitesi Brifingi ve Aksiyon Takip Matrisi",
            "desc": "Tamamlanan 6 denetim görevinde tespit edilen 14 bulgu (3 Kritik, 6 Yüksek, 5 Orta) ve 210M TL toplam maruziyetin Yönetim Kurulu için özetlenmesi.",
            "backend": "Teknik saha ayrıntıları stratejik risk, regülasyon cezası ve finansal zarar boyutuna indirgenir.",
            "action": "Dönem bulgu listesi girildi; yönetici brifingi üretildi.",
            "result": "Genel Güvence Görüşü: 🔴 OLUMSUZ (Kritik İç Kontrol Zaafiyeti) ve Üst Yönetim Aksiyon Takip Tablosu oluşturuldu."
        },
        {
            "num": "10",
            "phase": "5. SÜREKLİ DENETİM & ANALİTİK",
            "title": "Görev 10: Python (Pandas) İstisna Analiz Kodu & Canlı Sandbox",
            "img": "task_10_data_analytics.png",
            "caption": "Ekran Görüntüsü 1.10: Sürekli Analitik — Python İstisna Kodu ve İzole Sandbox Çalıştırma Paneli",
            "desc": "Hazine veri tabanındaki Offshore para transferleri ve MASAK bypass işlemlerini filtreleyen Python kodu ve izole sandbox'ta canlı çalıştırılması.",
            "backend": "Tier 3 Coder modeli Pandas scripti üretir; izole subprocess sandbox'ta çalıştırılarak `audit_exceptions.xlsx` oluşturulur.",
            "action": "'Çalışma Kağıdını Üret' sonrası '⚡ Kodu Sandbox'ta Çalıştır' butonuna basıldı.",
            "result": "Python kodu başarıyla çalıştı; ekrana yeşil başarı kartı, terminal logları ve 'audit_exceptions.xlsx İndir' butonu yansıdı."
        }
    ]

    for t in tasks_guide_info:
        elements.append(PageBreak())
        elements.append(Paragraph(f"4.{t['num']} {t['phase']} — {t['title']}", h1_style))
        elements.append(Paragraph(f"<b>Görev Amacı & Senaryo:</b> {t['desc']}", body_style))

        img_p = os.path.join(screenshot_dir, t["img"])
        if os.path.exists(img_p):
            elements.append(Image(img_p, width=540, height=210))
            elements.append(Paragraph(t["caption"], caption_style))

        task_tbl_data = [
            [Paragraph("İşlem Boyutu", table_header_style), Paragraph("Saha Uygulaması ve Teknik İşleyiş Detayları", table_header_style)],
            [Paragraph("<b>Arka Planda Ne Çalıştı?</b>", table_cell_style), Paragraph(t["backend"], table_cell_style)],
            [Paragraph("<b>Arayüzde Ne Yapıldı?</b>", table_cell_style), Paragraph(t["action"], table_cell_style)],
            [Paragraph("<b>Ekranda Görülen Sonuç:</b>", table_cell_style), Paragraph(t["result"], table_cell_style)]
        ]
        t_tbl = Table(task_tbl_data, colWidths=[120, 420])
        t_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
            ('TOPPADDING', (0, 0), (-1, -1), 2.2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
        ]))
        elements.append(t_tbl)

    # =========================================================================
    # BÖLÜM 5: RESMİ SİSTEM ÇIKTI FORMATLARI VE ÇIKTI ÖRNEKLERİ
    # =========================================================================
    elements.append(PageBreak())
    elements.append(Paragraph("5. RESMİ SİSTEM ÇIKTI FORMATLARI VE SOMUT ÇIKTI ÖRNEKLERİ", h1_style))
    elements.append(Paragraph(
        "Auditoris tarafından üretilen denetim çalışma kağıtları, Denetim Komitesi, Yönetim Kurulu ve "
        "bağımsız düzenleyici otoriteler (BDDK, SPK, MASAK) nezdinde resmi delil niteliğine sahip 4 farklı sistem çıktısı olarak sunulur:",
        body_style
    ))

    out_table_data = [
        [Paragraph("Sistem Çıktı Formatı", table_header_style), Paragraph("Teknik Standart & Görsel Düzen", table_header_style), Paragraph("Kullanım Amacı & Yasal Statü", table_header_style)],
        [
            Paragraph("<b>1. Word (.docx) Çalışma Kağıdı Çıktısı</b>", table_cell_style),
            Paragraph("• Kurumsal lacivert antet başlığı (#0f172a)<br/>• Denetçi, Tarih ve Görev meta bilgi kutusu<br/>• IIA 5C Hiyerarşik Bölümleri<br/>• SHA-256 Kriptografik Denetim İzi Mührü.", table_cell_style),
            Paragraph("Denetim Komitesi, Teftiş Kurulu ve Cumhuriyet Savcılığı teftiş dosyaları.", table_cell_style)
        ],
        [
            Paragraph("<b>2. Formatlı Excel (.xlsx) Tablo Çıktısı</b>", table_cell_style),
            Paragraph("• Koyu lacivert (#0f172a) kalın başlık satırı<br/>• Alternatif açık gri zebra satırları<br/>• İnce kenarlıklar ve otomatik sütun genişliği.", table_cell_style),
            Paragraph("Risk ve Kontrol Matrisleri (RCM), Denetim Evreni ve sayısal kontrol listeleri.", table_cell_style)
        ],
        [
            Paragraph("<b>3. Sandbox İstisna Raporu (.xlsx) Çıktısı</b>", table_cell_style),
            Paragraph("• Pandas ile 25.000 satırdan filtrelenen anomaliler<br/>• Çok sekmeli (Multi-Sheet) istisna listesi<br/>• Anomali tutar toplamları ve satır referansları.", table_cell_style),
            Paragraph("Sürekli denetim, fraud inceleme ve veri analitiği saha operasyonları.", table_cell_style)
        ],
        [
            Paragraph("<b>4. Kriptografik Audit Trail (JSON) Çıktısı</b>", table_cell_style),
            Paragraph("• Girdi ve çıktı SHA-256 hash imzaları<br/>• Kullanılan model, tier, süre ve zaman damgası<br/>• IIA Standardı 2026 Uyum Deklarasyonu.", table_cell_style),
            Paragraph("Kalite Güvence Gözden Geçirmeleri (QAR) ve bağımsız regülasyon denetimleri.", table_cell_style)
        ]
    ]

    t_out = Table(out_table_data, colWidths=[115, 245, 180])
    t_out.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
    ]))
    elements.append(t_out)
    elements.append(Spacer(1, 4))

    # Somut Çıktı Örnekleri Tablosu
    elements.append(Paragraph("SOMUT SİSTEM ÇIKTI ÖRNEKLERİ (WORD VE EXCEL ŞABLONLARI)", h2_style))

    sample_outputs_data = [
        [Paragraph("Çıktı Türü", table_header_style), Paragraph("Sistem Tarafından Otomatik Üretilen Çıktı Örneği İçeriği", table_header_style)],
        [
            Paragraph("<b>Word (.docx)<br/>Çalışma Kağıdı<br/>Metin Çıktısı Örneği</b>", table_cell_style),
            Paragraph(
                "<b>KURUMSAL ANTET:</b> MEGA YATIRIM BANKASI A.Ş. — TEFTİŞ KURULU BAŞKANLIĞI<br/>"
                "<b>GÖREV NO:</b> ENG-2026-044 &nbsp;|&nbsp; <b>TARİH:</b> 30.08.2026 &nbsp;|&nbsp; <b>DENETÇİ:</b> Kıdemli Müfettiş<br/>"
                "---------------------------------------------------------------------------------------------------------<br/>"
                "<b>1. DURUM (CONDITION):</b> Levent Şubesi kredi tahsis kayıtlarında, yetki limiti 15.000.000 TL olan Şube Müdürü tarafından 145.000.000 TL kredi tek imza ile onaylanmış; teminat ekspertiz raporunda %850 LTV şişirmesi tespit edilmiştir. Kredinin 78.500.000 TL'lik kısmı Panama offshore hesabına aktarılmıştır.<br/>"
                "<b>2. KRİTER (CRITERIA):</b> 5411 Sayılı Bankacılık Kanunu Madde 160 (Banka Zimmeti) ve 5549 Sayılı MASAK Kanunu Madde 8 (Şüpheli İşlem Bildirimi Zorunluluğu).<br/>"
                "<b>3. KÖK NEDEN (CAUSE):</b> Teminat ekspertiz kontrolünün şube inisiyatifinde bırakılması ve Core Banking sisteminde SoD limit blokajının bulunmaması.<br/>"
                "<b>4. ETKİ (EFFECT):</b> Bankanın 145.000.000 TL doğrudan batık kredi riski ve MASAK tarafından uygulanacak 50.000.000 TL idari para cezası maruziyeti.<br/>"
                "<b>5. ÖNERİ (RECOMMENDATION):</b> İlgili personel hakkında derhal Cumhuriyet Savcılığı'na suç duyurusunda bulunulması, MASAK STR bildiriminin yapılması ve sisteme FIDO2 çoklu onay kuralı getirilmesi.<br/>"
                "---------------------------------------------------------------------------------------------------------<br/>"
                "<b>KRİPTOGRAFİK MÜHÜR:</b> SHA-256: <code>e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855</code>",
                code_style
            )
        ],
        [
            Paragraph("<b>Formatlı Excel<br/>(.xlsx) RCM Tablosu<br/>Çıktısı Örneği</b>", table_cell_style),
            Paragraph(
                "<b>[SEKME: Risk_Kontrol_Matrisi]</b> (Koyu Lacivert Başlıklar, Alternatif Açık Gri Satırlar)<br/>"
                "• <b>Risk No:</b> R-TRS-01 &nbsp;|&nbsp; <b>Risk:</b> Yetkisiz Spot FX ve Swap Limit Aşımı (5M USD)<br/>"
                "• <b>Kontrol Faaliyeti:</b> Bloomberg/Reuters terminalinde işlem anında otomatik Limit Kontrolörü onayı<br/>"
                "• <b>Kontrol Türü:</b> Önleyici (Preventive) &nbsp;|&nbsp; <b>Sıklık:</b> Gerçek Zamanlı (Real-Time)<br/>"
                "• <b>Test Adımı:</b> Son 3 ayda 1M USD üzeri 25 adet swap biletinin çift onay logları ME23N üzerinden incelenir.<br/>"
                "---------------------------------------------------------------------------------------------------------<br/>"
                "<b>[SEKME: Walkthrough_Sorulari]</b><br/>"
                "• Soru 1: Piyasa volatilitesinde Stop-Loss limitleri manuel olarak esnetilebilir mi?<br/>"
                "• Soru 2: Hazine uzmanı ile Limit kontrolörünün şifre paylaşımını engelleyen kontrol nedir?",
                code_style
            )
        ]
    ]

    t_sample_out = Table(sample_outputs_data, colWidths=[115, 425])
    t_sample_out.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    elements.append(t_sample_out)
    elements.append(Spacer(1, 4))

    elements.append(Paragraph("DİNAMİK MEVZUAT KÜTÜPHANESİ (OFFLINE RAG) MEVZUAT MADDELERİ", h2_style))
    regs = [
        "<b>BDDK:</b> 5411 Sayılı Kanun Madde 160 (Zimmet), Madde 50 (Kredi Sınırları), Kredi Karşılıkları Yönetmeliği (%75 LTV), Bilgi Sistemleri Tebliği (PAM & Log Yönetimi).",
        "<b>MASAK:</b> 5549 Sayılı Kanun Madde 8 (STR Şüpheli İşlem Bildirimi), Madde 13 (İdari Para Cezaları), Sıra No: 5 Tebliği (Gerçek Faydalanıcı UBO ve PEP Tespiti).",
        "<b>SPK & KVKK:</b> SPK Madde 106 (İçeriden Öğrenenlerin Ticareti), SPK Madde 107 (Piyasa Dolandırıcılığı), 6698 Sayılı KVKK Madde 12 (72 Saatlik İhlal Bildirimi) ve Madde 18.",
        "<b>TTK & TCK:</b> TTK Madde 18/2 (Basiretli Tacir Sorumluluğu), TTK Madde 369 (Yönetim Kurulu Sadakat Borcu), TCK Madde 158 (Nitelikli Dolandırıcılık), TCK Madde 204 (Resmi Belgede Sahtecilik).",
        "<b>Uluslararası Standartlar:</b> Sarbanes-Oxley (SOX) Section 404, ISO/IEC 27001:2022 Madde A.8 ve IIA Küresel Standartları (2026 Evolution)."
    ]
    for r in regs:
        elements.append(Paragraph(f"• {r}", bullet_style))

    # =========================================================================
    # BÖLÜM 6: DENETİM İZİ, HAM JSON VE SİSTEMİN ÜRETTİĞİ SAF PROMPT ÇIKTILARI
    # =========================================================================
    elements.append(PageBreak())
    elements.append(Paragraph("6. DENETİM İZİ, HAM JSON VE SİSTEMİN ÜRETTİĞİ SAF PROMPT ÇIKTILARI", h1_style))
    elements.append(Paragraph(
        "<b>Arayüzden Ham Verilere ve Sistemin Ürettiği Prompta Erişim Kolaylığı:</b> Auditoris, tam şeffaflık ve "
        "denetlenebilirlik ilkesi gereğince modelin arkasında dönen hiçbir süreci gizlemez. Denetçiler ve Bağımsız "
        "Kalite Denetçileri (QAR ekipleri), üretilen çalışma kağıdının hemen altındaki 3 fonksiyonel sekmeden ham verilere doğrudan erişebilir:",
        body_style
    ))

    ui_tabs_guide = [
        "<b>🔍 Model & Akıllı Yönlendirme Analizi Sekmesi:</b> Model adı, çıkarım süresi, sıcaklık parametresi ve <b>Sistemin Otomatik Olarak Derleyip Genişlettiği Saf Model Promptu (Prompt Generator Payload)</b> bu sekmede 'Akıllı Prompt & Yönerge Detayları' açılır kutusu altında tam metin olarak görüntülenir ve kopyalanabilir.",
        "<b>🔒 Güvenlik & Denetim İzi (Audit Trail) Sekmesi:</b> PII maskeleme raporu, sıfır bulut sızıntısı güvencesi ve <b>Kriptografik SHA-256 İmzalı Ham JSON Nesnesi</b> bu sekmede canlı JSON ağacı olarak sunulur ve tek tıkla indirilebilir.",
        "<b>📄 IIA Çalışma Kağıdı Sekmesi:</b> Nihai resmi çalışma kağıdı, kalite skoru ve Word/Excel indirme butonları yer alır."
    ]
    for ut in ui_tabs_guide:
        elements.append(Paragraph(f"• {ut}", bullet_style))

    elements.append(Spacer(1, 4))
    elements.append(Paragraph("ÖRNEK 1: SİSTEMİN OTOMATİK DERLEDİĞİ AKILLI DENETİM PROMPTU (PROMPT GENERATOR)", h2_style))
    elements.append(Paragraph(
        "Denetçi sadece kısa saha notlarını girdiğinde, sistem arka planda IIA Rolünü, RAG Mevzuat Maddelerini ve Çıktı Şablonunu birleştirerek aşağıdaki tam kapsamlı Saf Promptu üretir ve modele iletir:",
        body_style
    ))

    sample_prompt_text = """[ROLE & PERSONA]:
Sen, IIA Küresel Standartları (2026 Evolution) ve BDDK/MASAK mevzuatına tam hakim Kıdemli İç Denetim Başmüfettişisin.

[GÖREV KAPSAMI & FAZ]:
Aşama: 4. Denetim Raporlama (Reporting)  |  Görev Türü: 5C Standart Denetim Bulgusu Yazımı (Finding 5C)
Kurumsal Bağlam: Mega Yatırım Bankası A.Ş. — Teftiş Kurulu Başkanlığı

[ENJEKTE EDİLEN MEVZUAT BİLGİSİ (OFFLINE RAG CRITERIA)]:
1. 5411 Sayılı Bankacılık Kanunu Madde 160 (Zimmet): "Banka kaynaklarını hileli yollarla zimmetine geçiren, yetkisiz kullandıran veya sahte teminatla kredi tahsis edenler..."
2. 5549 Sayılı MASAK Kanunu Madde 8 & 13: "Yükümlüler, şüpheli işlem bildirimini (STR) ivedilikle Başkanlığa iletmek zorundadır."
3. IIA Küresel Standartları (2026) Standart 2400: "Denetim bulgusu Condition, Criteria, Cause, Effect, Recommendation yapısında olmalıdır."

[MASKELENMİŞ VE DOĞRULANMIŞ SAHA BULGUSU]:
Kurum: Mega Yatırım Bankası A.Ş. — Levent Şubesi
Saha Tespiti: Şube Müdürü [KISI_1] tarafından yetki limiti 15.000.000 TL aşılarak 145.000.000 TL kredi tek imza ile onaylanmış; teminat ekspertizinde %850 LTV şişirmesi tespit edilmiştir. Tahsisin 78.500.000 TL'lik kısmı [HESAP_1] üzerinden Panama'daki offshore hesabına aktarılmıştır.

[ZORUNLU ÇIKTI ŞABLONU]:
1. Durum (Condition)  2. Kriter (Criteria)  3. Kök Neden (Cause)  4. Etki (Effect)  5. Öneri (Recommendation)  6. SHA-256 Mührü"""

    prompt_table = Table([[Paragraph(f"<pre>{sample_prompt_text}</pre>", code_style)]], colWidths=[540])
    prompt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#2563eb')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(prompt_table)
    elements.append(Spacer(1, 4))

    elements.append(Paragraph("ÖRNEK 2: KRİPTOGRAFİK AUDIT TRAIL HAM JSON ÇIKTISI (GÜVENLİK İZİ)", h2_style))
    elements.append(Paragraph(
        "Her görev tamamlandığında üretilen ve arayüzün 3. sekmesinden canlı olarak kopyalanabilen değiştirilemez Denetim İzi JSON nesnesi:",
        body_style
    ))
    
    sample_json_text = """{
  "timestamp": "2026-08-30T18:35:12.482Z",
  "audit_integrity_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "task_metadata": {
    "phase": "4. Denetim Raporlama (Reporting)",
    "task_type": "5C Standart Denetim Bulgusu Yazımı",
    "engagement_id": "ENG-2026-BANK-044",
    "auditor": "Kıdemli İç Denetçi"
  },
  "privacy_and_security": {
    "pii_sanitization_applied": true,
    "masked_entities_count": 4,
    "masked_types": ["TCKN", "IBAN", "CREDIT_CARD", "PERSON"],
    "cloud_leak_risk": "0.0% (Zero Cloud Leak / Air-Gapped)"
  },
  "model_execution": {
    "tier": "Tier 2 (Standart Analiz & RCM)",
    "dispatched_model": "qwen2.5-coder:7b",
    "inference_duration_sec": 119.1,
    "quality_score": 95,
    "quality_badge": "IIA Standartlarında Mükemmel"
  }
}"""
    
    json_table = Table([[Paragraph(f"<pre>{sample_json_text}</pre>", code_style)]], colWidths=[540])
    json_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#0f172a')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(json_table)

    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"✅ Güncellenmiş Master Kılavuz PDF Başarıyla Derlendi: {output_pdf_path} (Boyut: {os.path.getsize(output_pdf_path)/1024:.1f} KB)")
    return output_pdf_path

if __name__ == "__main__":
    generate_user_guide_pdf("storage/Auditoris_Kullanici_Kilavuzu_2026.pdf")
