import os
import shutil
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def create_proposal_document():
    doc = docx.Document()

    # 1. Page Margins: 2.5 cm everywhere (as per AHBV Guidelines)
    for s in doc.sections:
        s.top_margin = Cm(2.5)
        s.bottom_margin = Cm(2.5)
        s.left_margin = Cm(2.5)
        s.right_margin = Cm(2.5)

    # Normal Style
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    def set_para(p, text="", align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=6, space_after=6, line_spacing=1.5, indent=1.0, bold=False, italic=False, font_size=12):
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if indent > 0:
            p.paragraph_format.first_line_indent = Cm(indent)
        else:
            p.paragraph_format.first_line_indent = Cm(0)
        if text:
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)
            r.bold = bold
            r.italic = italic
            return r
        return None

    # ==========================================
    # SAYFA 1: KAPAK SAYFASI (EK 1 BİREBİR)
    # ==========================================
    p = doc.add_paragraph()
    set_para(p, "T.C.", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=20, space_after=2, indent=0, bold=True, font_size=14)
    p = doc.add_paragraph()
    set_para(p, "ANKARA HACI BAYRAM VELİ ÜNİVERSİTESİ", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2, indent=0, bold=True, font_size=14)
    p = doc.add_paragraph()
    set_para(p, "LİSANSÜSTÜ EĞİTİM ENSTİTÜSÜ", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=4, indent=0, bold=True, font_size=13)
    p = doc.add_paragraph()
    set_para(p, "İKTİSAT ANABİLİM DALI", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2, indent=0, bold=True, font_size=12)
    p = doc.add_paragraph()
    set_para(p, "İKTİSAT TEZLİ YÜKSEK LİSANS PROGRAMI", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=24, indent=0, bold=True, font_size=12)

    p = doc.add_paragraph()
    set_para(p, "YÜKSEK LİSANS TEZ ÖNERİSİ", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=20, indent=0, bold=True, font_size=13)

    # Tez Başlığı
    p = doc.add_paragraph()
    set_para(p, "SAVUNMA SANAYİİ AR-GE HARCAMALARININ SİVİL SEKTÖRLERDEKİ PATENT KALİTESİNE YAYILMA ETKİSİ (SPILLOVER): PATENT ATIF AĞLARIYLA AMPİRİK BİR İNCELEME", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=20, space_after=10, indent=0, bold=True, font_size=13)

    p = doc.add_paragraph()
    set_para(p, "(Spillover Effects of Defense R&D Expenditures on Civilian Patent Quality: An Empirical Investigation Through Patent Citation Networks)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=30, indent=0, italic=True, font_size=11)

    # Aday ve Danışman
    p = doc.add_paragraph()
    set_para(p, "Adayın Adı Soyadı: Doğukan CİHANBEYOĞLU", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=3, indent=0, bold=True, font_size=12)
    p = doc.add_paragraph()
    set_para(p, "Öğrenci Numarası: [Öğrenci No]", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=3, indent=0, font_size=11)
    p = doc.add_paragraph()
    set_para(p, "Tez Danışmanı: [Unvanı, Adı SOYADI]", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=3, space_after=20, indent=0, bold=True, font_size=12)

    # Danışman Onay Kutusu (Kılavuz Şartı: "Danışmanın el yazısıyla 'Uygundur' ibaresi ile birlikte tarih ve imza bulunacaktır")
    tbl_approval = doc.add_table(rows=1, cols=2)
    tbl_approval.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_approval.autofit = False

    cell_00 = tbl_approval.cell(0, 0)
    cell_00.width = Cm(8.0)
    p0 = cell_00.paragraphs[0]
    set_para(p0, "Tez Danışmanı Değerlendirmesi:\n[  ] UYGUNDUR\n[  ] UYGUN DEĞİLDİR", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=4, indent=0, font_size=10)

    cell_01 = tbl_approval.cell(0, 1)
    cell_01.width = Cm(8.0)
    p1 = cell_01.paragraphs[0]
    set_para(p1, "Danışman İmza ve Tarih:\n\nTarih: ..... / ..... / 2026\nİmza: .......................................", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=4, space_after=4, indent=0, font_size=10)

    for cell in tbl_approval.rows[0].cells:
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            r'''<w:tcBorders {}>
                <w:top w:val="single" w:sz="4" w:space="0" w:color="A0A0A0"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="A0A0A0"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="A0A0A0"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="A0A0A0"/>
            </w:tcBorders>'''.format(nsdecls("w"))
        )
        tcPr.append(borders)

    p = doc.add_paragraph()
    set_para(p, "Ankara, 2026", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=30, space_after=0, indent=0, bold=True, font_size=12)

    # ==========================================
    # SAYFA 2: İÇİNDEKİLER
    # ==========================================
    doc.add_page_break()

    p = doc.add_paragraph()
    set_para(p, "İÇİNDEKİLER", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=12, space_after=18, indent=0, bold=True, font_size=13)

    toc_items = [
        ("1. GİRİŞ", "1"),
        ("   1.1. Tezin Adı", "1"),
        ("   1.2. Tezin Konusu", "1"),
        ("   1.3. Tezin Amacı", "1"),
        ("   1.4. Tezin Önemi", "2"),
        ("2. YÖNTEM", "3"),
        ("   2.1. Kuramsal Çerçeve", "3"),
        ("   2.2. Varsayımlar", "4"),
        ("   2.3. Kapsam ve Sınırlılıklar", "4"),
        ("   2.4. Veri Toplama Tekniği", "4"),
        ("   2.5. Verilerin Analizi", "5"),
        ("3. ÇALIŞMA PLANI (EK 2)", "6"),
        ("4. ZAMANLAMA (EK 3)", "7"),
        ("5. KAYNAKÇA (EK 4)", "8")
    ]

    for title, pg in toc_items:
        p = doc.add_paragraph()
        set_para(p, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=3, space_after=3, line_spacing=1.15, indent=0)
        r1 = p.add_run(title)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(11)
        if not title.startswith("   "):
            r1.bold = True
        r2 = p.add_run(f" {' . ' * 20} {pg}")
        r2.font.name = "Times New Roman"
        r2.font.size = Pt(10)

    # ==========================================
    # SAYFA 3: 1. GİRİŞ
    # ==========================================
    doc.add_page_break()

    p = doc.add_paragraph()
    set_para(p, "1. GİRİŞ", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=12, indent=0, bold=True, font_size=13)

    # 1.1. Tezin Adı
    p = doc.add_paragraph()
    set_para(p, "1.1. Tezin Adı", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=4, indent=0, bold=True, font_size=12)
    p = doc.add_paragraph()
    set_para(p, "Tezin Adı: \"Savunma Sanayii Ar-Ge Harcamalarının Sivil Sektörlerdeki Patent Kalitesine Yayılma Etkisi (Spillover): Patent Atıf Ağlarıyla Ampirik Bir İnceleme\"", indent=1.0)

    # 1.2. Tezin Konusu
    p = doc.add_paragraph()
    set_para(p, "1.2. Tezin Konusu", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4, indent=0, bold=True, font_size=12)
    p = doc.add_paragraph()
    set_para(p, "Türkiye’de 2005-2025 döneminde kamu kaynakları ve stratejik yerlileşme hedefleriyle genişleyen savunma sanayii Ar-Ge harcamalarının, sivil sektörlerde (özellikle otomotiv, haberleşme teknolojileri, yapay zekâ/yazılım ve malzeme sanayii) faaliyet gösteren firmaların patent kalitesi ve aldığı atıflar üzerindeki teknolojik yayılma (knowledge spillover) etkisinin patent atıf ağları ve mikro panel sayma verisi ekonometrisiyle incelenmesidir.", indent=1.0)
    p = doc.add_paragraph()
    set_para(p, "Savunma sanayiinde üretilen tescilli teknolojilerin sivil sektörler tarafından ne ölçüde benimsendiği ve çift kullanımlı (dual-use) kanallarla sivil inovasyonu nasıl beslediği, Türk Patent ve Marka Kurumu (TÜRKPATENT) ile Google Patents mikro atıf kayıtları üzerinden ilk kez sayısallaştırılmaktadır.", indent=1.0)

    # 1.3. Tezin Amacı
    p = doc.add_paragraph()
    set_para(p, "1.3. Tezin Amacı", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4, indent=0, bold=True, font_size=12)
    p = doc.add_paragraph()
    set_para(p, "Bu araştırmanın temel amacı; savunma sanayii ana sistem entegratörlerinin (ASELSAN, TUSAŞ, ROKETSAN, BAYKAR, HAVELSAN, STM) Ar-Ge yatırımları sonucunda ortaya çıkan patentlerin, sivil imalat sanayiinin patent kalitesi (aldığı ileriye dönük sivil atıf sayısı) üzerinde istatistiki olarak anlamlı bir yayılma etkisi (spillover) yaratıp yaratmadığını ampirik olarak test etmektir.", indent=1.0)
    p = doc.add_paragraph()
    set_para(p, "Tezin alt amaçları şunlardır:\n"
              "1. Savunma patentlerinin aldığı ileriye dönük atıflar (forward citations) içerisindeki sivil sektör payını ve teknoloji difüzyon hızını mikro düzeyde haritalandırmak,\n"
              "2. Savunma teknolojisi ile sivil sektörlerin IPC sınıfları arasındaki Jaffe (1993) teknolojik mesafe indeksini hesaplayarak, yakınlığın yayılma esnekliğine etkisini belirlemek,\n"
              "3. Savunma Ar-Ge bütçelerinin sivil Ar-Ge yatırımlarını tetikleyen bir kaldıraç mı (crowding-in / spillover) yoksa nitelikli işgücü ve sermayeyi kendine çekerek sivil üretkenliği zayıflatan bir dışlama mekanizması mı (crowding-out) yarattığını ampirik olarak ayrıştırmaktır.", indent=1.0)

    # 1.4. Tezin Önemi
    p = doc.add_paragraph()
    set_para(p, "1.4. Tezin Önemi", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4, indent=0, bold=True, font_size=12)
    p = doc.add_paragraph()
    set_para(p, "İktisat yazınında savunma harcamalarının ekonomik büyümeye etkisi uzun yıllar Benoit (1973) ile Deger ve Sen (1983) ekseninde salt makroekonomik seriler üzerinden tartışılmış; mikro düzeydeki inovasyon kanalları ihmal edilmiştir. Son dönemde Moretti, Steinwender ve Van Reenen (2023) tarafından OECD ülkeleri için ortaya konulan yeni nesil ampirik iktisat yazını, savunma Ar-Ge’sinin üretkenlik etkisinin doğrudan patent atıfları ve bilgi difüzyonu kanalıyla ölçülmesi gerektiğini kanıtlamıştır.", indent=1.0)
    p = doc.add_paragraph()
    set_para(p, "Türkiye savunma sanayii bütçesi son yirmi yılda kayda değer bir büyüme kaydetmesine rağmen, askeri Ar-Ge’nin sivil inovasyona geçişkenliği bugüne kadar mikro ekonometrik düzeyde hiç incelenmemiştir. Bu tez çalışması üç temel alanda literatüre ve uygulamaya somut katkı sağlayacaktır:\n"
              "1. Metodolojik Katkı: Türkiye’de ilk kez savunma patentleri ile sivil sektörler arasındaki atıf bağı, Jaffe (1986, 1993) ve Hall, Jaffe ve Trajtenberg (2001) metodolojisiyle mikro düzeyde haritalandırılacaktır.\n"
              "2. Ampirik Katkı: Gelişmiş OECD ülkeleri için doğrulanan savunma Ar-Ge yayılma modelleri, gelişmekte olan ve yapısal yerlileşme sıçraması yaşayan Türkiye ekonomisi bağlamında ilk kez Poisson Pseudo-Maximum Likelihood (PPML) ve Negative Binomial panel sayma modelleriyle tahmin edilecektir.\n"
              "3. Sanayi Politikası Katkısı: Sanayi ve Teknoloji Bakanlığı ile Savunma Sanayii Başkanlığı’nın (SSB) çift kullanımlı teknoloji transferi hedefleri için kanıta dayalı somut politika girdisi ve çarpan katsayısı sunulacaktır.", indent=1.0)

    # ==========================================
    # SAYFA 4: 2. YÖNTEM
    # ==========================================
    doc.add_page_break()

    p = doc.add_paragraph()
    set_para(p, "2. YÖNTEM", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=12, indent=0, bold=True, font_size=13)

    # 2.1. Kuramsal Çerçeve
    p = doc.add_paragraph()
    set_para(p, "2.1. Kuramsal Çerçeve", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=4, indent=0, bold=True, font_size=12)
    p = doc.add_paragraph()
    set_para(p, "Araştırmanın kuramsal temeli; içsel büyüme modelleri (Romer, 1990; Aghion & Howitt, 1992), teknolojik bilgi yayılması çerçevesi (Griliches, 1979, 1992) ve kamu savunma Ar-Ge’sinin sivil inovasyona difüzyonunu modelleyen Moretti, Steinwender ve Van Reenen (2023) yaklaşımına dayanmaktadır. Bilgi kamusal mal niteliğine sahip olduğundan, bir sektörde üretilen tescilli buluş diğer sektörlerin araştırma maliyetlerini düşürür. Jaffe (1993) yaklaşımına göre teknolojik yayılma uzayda serbestçe dağılmaz; firmaların sahip olduğu teknolojik portföyün benzerliği (Jaffe Yakınlık İndeksi) difüzyonun etkinliğini belirler.", indent=1.0)

    # 2.2. Varsayımlar
    p = doc.add_paragraph()
    set_para(p, "2.2. Varsayımlar", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4, indent=0, bold=True, font_size=12)
    p = doc.add_paragraph()
    set_para(p, "1. Patent başvuru ve tescil verilerinin, firmaların teknoloji üretme kapasitesi ve inovasyon çabası için geçerli ve tarafsız bir gösterge (proxy) olduğu kabul edilmiştir (Griliches, 1990).\n"
              "2. İleriye dönük patent atıflarının (forward citations), tescilli buluşun iktisadi ve teknik kalitesini yansıttığı varsayılmıştır (Hall, Jaffe & Trajtenberg, 2005).\n"
              "3. TÜRKPATENT ve Google Patents veritabanlarındaki tescil ve atıf kayıtlarının tarafsız ve eksiksiz tutulduğu varsayılmıştır.", indent=1.0)

    # 2.3. Kapsam ve Sınırlılıklar
    p = doc.add_paragraph()
    set_para(p, "2.3. Kapsam ve Sınırlılıklar", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4, indent=0, bold=True, font_size=12)
    p = doc.add_paragraph()
    set_para(p, "Araştırmanın zaman kapsamı 2005-2024 yılları arasındaki 20 yıllık panel veri setidir. Kurumsal kapsam, Savunma Sanayii Başkanlığı ekosisteminde yer alan ve SASAD sektör cirosunun %80’inden fazlasını temsil eden 6 ana yüklenici (ASELSAN, TUSAŞ, ROKETSAN, BAYKAR, HAVELSAN, STM) ve bu firmaların tescilli patentlerine atıfta bulunan sivil NACE Rev.2 kodlu imalat ve teknoloji şirketleridir.", indent=1.0)
    p = doc.add_paragraph()
    set_para(p, "Sınırlılıklar: 6769 sayılı Sınai Mülkiyet Kanunu’nun 124. maddesi uyarınca 'Milli Savunma Menfaatleri Gereği Gizli Tutulan Buluşlar' kamuya açık veri tabanlarında yer almadığından araştırmaya dahil edilememiştir; analiz kamuya tescilli açık patentlerle sınırlıdır.", indent=1.0)

    # 2.4. Veri Toplama Tekniği
    p = doc.add_paragraph()
    set_para(p, "2.4. Veri Toplama Tekniği", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4, indent=0, bold=True, font_size=12)
    p = doc.add_paragraph()
    set_para(p, "Veri toplama sürecinde birden fazla birincil veri tabanı çapraz sorgulama yöntemiyle birleştirilecektir:\n"
              "1. Mikro Patent ve Atıf Verileri: Google Patents Public Datasets (BigQuery üzerinde barındırılan küresel patent havuzu), Türk Patent ve Marka Kurumu (TÜRKPATENT) Sicil Bültenleri ve Avrupa Patent Ofisi (EPO PATSTAT / Espacenet) kayıtları,\n"
              "2. Savunma Ar-Ge ve Finansal Göstergeler: SASAD Sektör Performans Raporları (2010-2024), Savunma Sanayii Başkanlığı Faaliyet Raporları ve Borsa İstanbul (BIST) KAP finansal dipnotları,\n"
              "3. Makro Kontrol Değişkenleri: TÜİK Ar-Ge Harcamaları Bültenleri ve Dünya Bankası göstergeleri.", indent=1.0)

    # 2.5. Verilerin Analizi
    p = doc.add_paragraph()
    set_para(p, "2.5. Verilerin Analizi", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=10, space_after=4, indent=0, bold=True, font_size=12)
    p = doc.add_paragraph()
    set_para(p, "Patent atıf sayıları negatif değer almayan, yoğun sıfır içeren ve aşırı yayılımlı (overdispersed) tamsayı sayma verisi niteliğindedir. Bu tür verilerde klasik En Küçük Kareler (OLS) veya log alınmış modeller sapmalı ve tutarsız sonuçlar verir (Santos Silva & Tenreyro, 2006). Bu nedenle model, Poisson Pseudo-Maximum Likelihood (PPML) ve Negative Binomial panel teknikleriyle tahmin edilecektir.", indent=1.0)
    p = doc.add_paragraph()
    set_para(p, "Tahmin Edilecek Temel Ekonometrik Model:\n"
              "E[Cites_ijt | X_it, Z_jt] = exp( a_i + g_j + l_t + b_1 * ln(Def_R&D_{i, t-k}) + b_2 * Jaffe_ij + b_3 * (ln(Def_R&D_{i, t-k}) * Jaffe_ij) + X_jt * d )\n\n"
              "Burada Cites_ijt, t yılında i savunma firmasının patentlerine j sivil firması tarafından yapılan atıf sayısıdır. Jaffe_ij, firmaların IPC teknoloji sınıfları vektörlerinin kosinüs açısıyla hesaplanan 0 ile 1 arasındaki teknolojik yakınlık katsayısıdır. a_i, g_j ve l_t sırasıyla firma, sektör ve zaman sabit etkileridir. Analizler Python (statsmodels) ve Stata yazılımları kullanılarak kümelenmiş dirençli standart hatalarla (clustered robust SE) koşturulacaktır.", indent=1.0)

    # ==========================================
    # SAYFA 5: 3. ÇALIŞMA PLANI (EK 2)
    # ==========================================
    doc.add_page_break()

    p = doc.add_paragraph()
    set_para(p, "3. ÇALIŞMA PLANI (EK 2)", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=12, indent=0, bold=True, font_size=13)

    plan_text = (
        "Tez çalışması için öngörülen taslak çalışma planı ve içindekiler yapısı aşağıda sunulmuştur:\n\n"
        "BÖLÜM 1: GİRİŞ\n"
        "  1.1. Araştırmanın Arka Planı ve Problemi\n"
        "  1.2. Tezin Amacı, Kapsamı ve Literatüre Katkıları\n"
        "  1.3. Türkiye Savunma Sanayiinin Tarihsel Gelişimi ve Kurumsal Yapısı\n\n"
        "BÖLÜM 2: KURAMSAL ÇERÇEVE VE LİTERATÜR TARAMASI\n"
        "  2.1. İnovasyon Kuramları ve Bilgi Yayılması (Knowledge Spillover)\n"
        "  2.2. Savunma Harcamaları ve İktisadi Büyüme: Crowding-In ve Crowding-Out Tartışmaları\n"
        "  2.3. Çift Kullanımlı (Dual-Use) Teknoloji Difüzyonu\n"
        "  2.4. Patent Atıf Ağları ve Teknolojik Mesafe Yazını (Jaffe, Hall, Trajtenberg Yaklaşımları)\n"
        "  2.5. Dünyada ve Türkiye’de Yapılmış Ampirik Çalışmaların Eleştirel Sentezi\n\n"
        "BÖLÜM 3: VERİ SETİ VE METODOLOJİK YAKLAŞIM\n"
        "  3.1. Türkiye Patent Evreni ve Veri Derleme Süreci (Google Patents & TÜRKPATENT)\n"
        "  3.2. Jaffe (1993) Teknolojik Yakınlık İndeksinin Hesaplanması\n"
        "  3.3. Patent Atıf Ağının Topolojik Özellikleri ve Ağ Merkezilik Ölçütleri\n"
        "  3.4. Ekonometrik Model: Sayma Verisi Analizi (Poisson QML ve Negatif Binom)\n"
        "  3.5. İçsellik Sorunu ve Araç Değişken (IV) Tanı Testleri\n\n"
        "BÖLÜM 4: AMPİRİK BULGULAR VE TARTIŞMA\n"
        "  4.1. Tanımlayıcı İstatistikler ve Sektörel Dağılımlar\n"
        "  4.2. Savunma-Sivil Patent Atıf Ağı Haritası ve Difüzyon Kanalları\n"
        "  4.3. Panel Sayma Modeli Regresyon Tahmin Sonuçları\n"
        "  4.4. Teknolojik Yakınlık ve Etkileşim Katsayılarının Yorumlanması\n"
        "  4.5. Sağlamlık (Robustness) Sınamaları ve Alternatif Model Spesifikasyonları\n\n"
        "BÖLÜM 5: SONUÇ VE SANAYİ POLİTİKASI ÖNERİLERİ\n"
        "  5.1. Temel Bulguların Özeti\n"
        "  5.2. Türkiye Savunma ve Sanayi Politikaları Açısından Çıkarımlar\n"
        "  5.3. Araştırmanın Kısıtları ve Gelecek Çalışmalar İçin Öneriler"
    )
    p = doc.add_paragraph()
    set_para(p, plan_text, indent=0, line_spacing=1.15)

    # ==========================================
    # SAYFA 6: 4. ZAMANLAMA (EK 3 TABLOSU BİREBİR)
    # ==========================================
    doc.add_page_break()

    p = doc.add_paragraph()
    set_para(p, "4. ZAMANLAMA (EK 3)", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=12, indent=0, bold=True, font_size=13)

    p = doc.add_paragraph()
    set_para(p, "Tez çalışmasının normal süre içerisinde tamamlanabilmesi için öngörülen iş-zaman tablosu Enstitü formatında aşağıda düzenlenmiştir:", indent=1.0)

    # Table as mandated by EK 3: "Planlanan | Tarih (GG.AA.YYYY - GG.AA.YYYY)"
    tbl = doc.add_table(rows=7, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    headers = ["Planlanan Çalışma / Aşama", "Tarih (GG.AA.YYYY - GG.AA.YYYY)"]
    row_0 = tbl.rows[0]
    for idx, text in enumerate(headers):
        cell = row_0.cells[idx]
        cell.width = Cm(10.0 if idx == 0 else 6.0)
        shading = parse_xml(r'<w:shd {} w:fill="E0E0E0"/>'.format(nsdecls('w')))
        cell._tc.get_or_add_tcPr().append(shading)
        p = cell.paragraphs[0]
        set_para(p, text, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=4, space_after=4, indent=0, bold=True, font_size=11)

    timeline_data = [
        ("Literatür Taraması ve Kuramsal Çerçevenin Oluşturulması", "01.10.2025 - 30.11.2025"),
        ("Verilerin Toplanması (Google Patents, TÜRKPATENT, SASAD)", "01.12.2025 - 31.01.2026"),
        ("Birinci ve İkinci Bölümün Yazılması (Giriş ve Literatür)", "01.02.2026 - 31.03.2026"),
        ("Jaffe Mesafe Hesaplamaları ve Ağ Topolojisi Analizi", "01.04.2026 - 30.04.2026"),
        ("Ekonometrik Modelleme ve Üçüncü-Dördüncü Bölümün Yazımı", "01.05.2026 - 30.06.2026"),
        ("Sonuç Bölümünün Yazılması, Biçim Denetimi ve Savunma Sınavı", "01.07.2026 - 30.09.2026")
    ]

    for r_idx, (task, dates) in enumerate(timeline_data, start=1):
        row = tbl.rows[r_idx]
        cell_task = row.cells[0]
        cell_task.width = Cm(10.0)
        p = cell_task.paragraphs[0]
        set_para(p, task, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=3, space_after=3, line_spacing=1.15, indent=0, font_size=10)
        
        cell_dates = row.cells[1]
        cell_dates.width = Cm(6.0)
        p = cell_dates.paragraphs[0]
        set_para(p, dates, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=3, space_after=3, line_spacing=1.15, indent=0, font_size=10)

    # Borders for table
    for row in tbl.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            borders = parse_xml(
                r'''<w:tcBorders {}>
                    <w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
                    <w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
                    <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
                    <w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
                </w:tcBorders>'''.format(nsdecls("w"))
            )
            tcPr.append(borders)

    # ==========================================
    # SAYFA 7: 5. KAYNAKÇA (EK 4 - APA 7)
    # ==========================================
    doc.add_page_break()

    p = doc.add_paragraph()
    set_para(p, "5. KAYNAKÇA (EK 4)", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=12, space_after=12, indent=0, bold=True, font_size=13)

    p = doc.add_paragraph()
    set_para(p, "(Kılavuz Notu: Kaynakça listesi APA 7. Basım esaslarına uygun olarak asılı girintili ve alfabetik sırada düzenlenmiştir.)", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=12, indent=0, italic=True, font_size=10)

    references = [
        ("Aghion, P., & Howitt, P. (1992). A model of growth through creative destruction. Econometrica, 60(2), 323–351. https://doi.org/10.2307/2951599"),
        ("Benoit, E. (1973). Defense and economic growth in developing countries. D.C. Heath and Company."),
        ("Bloom, N., Schankerman, M., & Van Reenen, J. (2013). Identifying technology spillovers and product market rivalry. Econometrica, 81(4), 1347–1393. https://doi.org/10.3982/ecta9466"),
        ("Deger, S., & Sen, S. (1983). Military expenditure, spin-off and economic development. Journal of Development Economics, 13(1–2), 67–83. https://doi.org/10.1016/0304-3878(83)90050-4"),
        ("Dunne, J. P., & Smith, R. P. (1990). Military expenditure and unemployment in the OECD. Defence Economics, 1(1), 57–73. https://doi.org/10.1080/10430719008404651"),
        ("Griliches, Z. (1979). Issues in assessing the contribution of research and development to productivity growth. The Bell Journal of Economics, 10(1), 92–116. https://doi.org/10.2307/3003321"),
        ("Griliches, Z. (1990). Patent statistics as economic indicators: A survey. Journal of Economic Literature, 28(4), 1661–1707."),
        ("Hall, B. H., Jaffe, A. B., & Trajtenberg, M. (2001). The NBER patent citation data file: Lessons, insights and methodological tools (NBER Working Paper No. 8498). National Bureau of Economic Research. https://doi.org/10.3386/w8498"),
        ("Hall, B. H., Jaffe, A., & Trajtenberg, M. (2005). Market value and patent citations. RAND Journal of Economics, 36(1), 16–38."),
        ("Hausman, J., Hall, B. H., & Griliches, Z. (1984). Econometric models for count data with an application to the patents-R&D relationship. Econometrica, 52(4), 909–938. https://doi.org/10.2307/1911191"),
        ("Jaffe, A. B. (1986). Technological opportunity and spillovers of R&D: Evidence from firms\' patents, profits, and market value. American Economic Review, 76(5), 984–1001."),
        ("Jaffe, A. B. (1993). Geographic localization of knowledge spillovers as evidenced by patent citations. Quarterly Journal of Economics, 108(3), 577–598. https://doi.org/10.2307/2118401"),
        ("Moretti, E., Steinwender, C., & Van Reenen, J. (2023). The intellectual spoils of war? Defense R&D, productivity and international spillovers. The Economic Journal, 133(656), 2824–2858. https://doi.org/10.1093/ej/uead052"),
        ("Mowery, D. C. (2010). Military R&D and innovation. In B. H. Hall & N. Rosenberg (Eds.), Handbook of the Economics of Innovation (Vol. 2, pp. 1219–1256). North-Holland. https://doi.org/10.1016/S0169-7218(10)02013-7"),
        ("Romer, P. M. (1990). Endogenous technological change. Journal of Political Economy, 98(5, Part 2), S71–S102. https://doi.org/10.1086/261725"),
        ("Ruttan, V. W. (2006). Is war necessary for economic growth? Military procurement and technology development. Oxford University Press."),
        ("Santos Silva, J. M. C., & Tenreyro, S. (2006). The log of gravity. The Review of Economics and Statistics, 88(4), 641–658. https://doi.org/10.1162/rest.88.4.641"),
        ("Wooldridge, J. M. (2010). Econometric analysis of cross section and panel data (2nd ed.). MIT Press.")
    ]

    for ref in references:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Cm(1.25)
        p.paragraph_format.first_line_indent = Cm(-1.25)
        r = p.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    target_docx = "/Users/dogukancihanbeyoglu/Gemini/TEZ_ONERI_FORMU_AHBV.docx"
    doc.save(target_docx)

    desktop_target = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/01_Tez_Oneri_Formu/TEZ_ONERI_FORMU_AHBV.docx"
    shutil.copyfile(target_docx, desktop_target)
    print("SUCCESS: 100% exact document built and synced!")

if __name__ == "__main__":
    create_proposal_document()
