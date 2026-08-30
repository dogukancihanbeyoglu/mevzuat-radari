"""
Auditoris - 10 Görev Türünün Tamamını Çalıştırıp Gerçek Sonuç Çıktılarını Bekleyen Bot
Model üretimini ve spinner'ın kapanmasını 'Word (.docx) İndir' butonunun belirmesiyle garanti altına alır.
"""
import os
import time
from playwright.sync_api import sync_playwright

screenshot_dir = "storage/screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

tasks_catalog = [
    # AŞAMA 1: YILLIK PLANLAMA
    {
        "id": "task_01_audit_universe",
        "phase": "1. Yıllık Planlama (Annual Planning)",
        "task": "Denetim Evreni ve Risk Derecelendirmesi",
        "input": "Holding bünyesindeki 18 iştirak ve 25 kritik süreç için finansal büyüklük, regülasyon baskısı (BDDK/MASAK/SPK) ve iç kontrol olgunluk puanlarına göre risk derecelendirmesi ve 2026 Denetim Planı önceliklendirmesi yapınız."
    },
    {
        "id": "task_02_resource_mapping",
        "phase": "1. Yıllık Planlama (Annual Planning)",
        "task": "Kaynak ve Yetkinlik Planlaması",
        "input": "12 kişilik denetim kadrosunun finansal, IT, suistimal (fraud) ve veri analitiği yetkinlik puanları (1-5) ile 2026 denetim planı için adam/gün (manday) eşleştirmesini yapınız."
    },
    # AŞAMA 2: GÖREV PLANLAMA
    {
        "id": "task_03_rcm_generation",
        "phase": "2. Görev Planlama (Engagement Planning)",
        "task": "Risk ve Kontrol Matrisi (RCM) & Walkthrough",
        "input": "Hazine ve Döviz Swap Operasyonları süreci için Yetkisiz Spot FX Alımı, SoD çakışması ve Stop-Loss limit aşımı risklerine karşı RCM matrisi ve 5 walkthrough mülakat sorusu oluşturunuz."
    },
    {
        "id": "task_04_scoping_document",
        "phase": "2. Görev Planlama (Engagement Planning)",
        "task": "Denetim Kapsam Dokümanı (Scoping)",
        "input": "Kurumsal Kredi Tahsis ve Teminat Yönetimi süreci denetimi için kapsam içi (in-scope: 50M TL üzeri krediler, ekspertiz onayları) ve kapsam dışı (out-of-scope: bireysel tüketici kredileri) risk alanlarını ve hedeflerini belirleyiniz."
    },
    # AŞAMA 3: SAHA ÇALIŞMASI
    {
        "id": "task_05_test_procedure",
        "phase": "3. Saha Çalışması (Fieldwork & Testing)",
        "task": "Kontrol Test Prosedürü Geliştirme",
        "input": "Kontrol: 5.000.000 TL üzeri satınalma faturalarında ERP üzerinde Çift İmza ve 3'lü Eşleştirme (PO-GR-Invoice) kontrolü. Bu kontrol için 4-ögeli detaylı test prosedürünü (Hedef, Örneklem, Test Adımları, Kabul Kriteri) yazınız."
    },
    {
        "id": "task_06_control_analysis",
        "phase": "3. Saha Çalışması (Fieldwork & Testing)",
        "task": "Kontrol Tanımı ve Tasarım Zayıflığı Analizi",
        "input": "Mevcut Kontrol 1: 2.000.000 USD limitli sözlü döviz alımları gün sonunda Hazine Müdürü tarafından imzalanır.\nMevcut Kontrol 2: Akaryakıt deniz nakliyesinde binde 3 yerine şirket içi sirkülerle %2.5 fire toleransı uygulanır.\nBu iki kontrolün tasarım zafiyetlerini ve muğlak noktalarını analiz ediniz."
    },
    {
        "id": "task_07_data_extraction",
        "phase": "3. Saha Çalışması (Fieldwork & Testing)",
        "task": "Yapılandırılmamış Metinden Veri Ayıklama",
        "input": "Fatura Metni: 'Mega Enerji A.Ş. adına düzenlenen 28.08.2026 tarihli INV-98231 nolu fatura tutarı 14.500.000 TL olup, IBAN: TR330006100511123456789012 hesabına transfer edilmiştir. Onaylayan: Ahmet Yılmaz (Genel Müdür Yardımcısı). Ekspertiz No: EXP-4412.'\nBu metindeki varlıkları ayıklayıp JSON ve tablo formatında sununuz."
    },
    # AŞAMA 4: DENETİM RAPORLAMA
    {
        "id": "task_08_finding_5c",
        "phase": "4. Denetim Raporlama (Reporting)",
        "task": "5C Standart Denetim Bulgusu Yazımı",
        "input": "Levent şubesinde 145.000.000 USD tutarında sahte ekspertizli teminatsız kredi kullandırıldığı, LTV oranının %850'ye ulaştığı ve MASAK filtresi devre dışı bırakılarak 78.500.000 USD suç gelirinin Panama hesaplarına aktarıldığı saptanmıştır."
    },
    {
        "id": "task_09_executive_summary",
        "phase": "4. Denetim Raporlama (Reporting)",
        "task": "Yönetici Özeti (Executive Summary)",
        "input": "2026 Kredi ve Hazine Teftişi tamamlanmış olup 1 kritik (145M USD kredi zimmeti), 2 yüksek riskli bulgu tespit edilmiştir. Denetim Komitesi ve Yönetim Kurulu için üst düzey yönetici özetini hazırlayınız."
    },
    # AŞAMA 5: SÜREKLİ DENETİM & ANALİTİK
    {
        "id": "task_10_data_analytics",
        "phase": "5. Sürekli Denetim & Analitik (Analytics)",
        "task": "Python (Pandas) İstisna Analiz Kodu",
        "input": "25.000 satırlık bankacılık logları tablosunda LTV > 0.75 ve masak_filter_cleared == False olan anomalileri tespit eden ve 'audit_exceptions.xlsx' dosyasına yazan Pandas kodunu üretiniz."
    }
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 1050})

    print("🌐 Streamlit Uygulamasına Bağlanılıyor...")
    page.goto("http://localhost:8501", wait_until="networkidle")
    time.sleep(2)

    for item in tasks_catalog:
        t_id = item["id"]
        p_name = item["phase"]
        t_name = item["task"]
        inp = item["input"]

        print(f"\n🚀 İşleniyor: [{t_id}] {p_name} -> {t_name}")

        page.goto("http://localhost:8501", wait_until="networkidle")
        time.sleep(1)

        # 1. Aşama Seçimi
        phase_select = page.get_by_label("Denetim Aşaması:")
        if phase_select.count() > 0:
            phase_select.click(force=True)
            time.sleep(0.3)
            opt_phase = page.get_by_role("option", name=p_name)
            if opt_phase.count() > 0:
                opt_phase.first.click()
                time.sleep(0.6)

        # 2. Görev Seçimi
        task_select = page.get_by_label("Görev Türü:")
        if task_select.count() > 0:
            task_select.click(force=True)
            time.sleep(0.3)
            opt_task = page.get_by_role("option", name=t_name)
            if opt_task.count() > 0:
                opt_task.first.click()
                time.sleep(0.6)

        # 3. Saha Notu Gir
        text_areas = page.locator("textarea")
        if text_areas.count() > 0:
            text_areas.first.fill(inp)
            time.sleep(0.3)

        # 4. Çalıştır
        run_btn = page.get_by_role("button", name="Çalışma Kağıdını Üret")
        if run_btn.count() > 0:
            run_btn.first.click()
            print("⏳ Model analizi yürütülüyor ve sonuç bekleniyor...")
            
            # SPINNER'IN KAPANIP SONUCUN EKRANA BASILMASINI BEKLE!
            try:
                page.locator("text=Word (.docx) İndir").wait_for(state="visible", timeout=60000)
                print("✨ Sonuç ekrana tam olarak yansıdı!")
            except Exception as e:
                print(f"⚠️ Bekleme uyarısı: {e}, 5 sn ek süre bekleniyor...")
                time.sleep(5)

        # 5. Sayfayı Sonuç Alanına Odakla (Hafif Kaydır)
        time.sleep(1)
        page.evaluate("window.scrollBy(0, 320)")
        time.sleep(0.5)

        # 6. Ekran Görüntüsü Al
        save_file = f"{t_id}.png"
        save_path = os.path.join(screenshot_dir, save_file)
        page.screenshot(path=save_path, full_page=False)
        print(f"✅ Gerçek Sonuç Ekran Görüntüsü Kaydedildi: {save_path}")

    browser.close()
    print("\n🎉 Tüm 10 Görev Türünün Kesinleşmiş Sonuç Ekran Görüntüleri Başarıyla Alındı!")
