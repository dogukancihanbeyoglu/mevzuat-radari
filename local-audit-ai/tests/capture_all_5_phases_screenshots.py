"""
Auditoris - 5 Aşama ve Görev Türü Otomasyon & Ekran Görüntüsü Botu (Exact Label Selector)
"""
import os
import time
from playwright.sync_api import sync_playwright

screenshot_dir = "storage/screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

phases_data = [
    {
        "phase_name": "1. Yıllık Planlama (Annual Planning)",
        "task_name": "Denetim Evreni ve Risk Derecelendirmesi",
        "input_text": "Holding bünyesindeki 18 iştirak ve 25 kritik süreç için finansal büyüklük (50M - 450M TL), regülasyon baskısı (BDDK/MASAK/SPK) ve iç kontrol olgunluk puanlarına göre risk derecelendirmesi ve 2026 Denetim Planı önceliklendirmesi yapınız.",
        "output_file": "phase1_annual_plan.png"
    },
    {
        "phase_name": "2. Görev Planlama (Engagement Planning)",
        "task_name": "Risk ve Kontrol Matrisi (RCM) & Walkthrough",
        "input_text": "Hazine ve Döviz Swap Operasyonları süreci için Yetkisiz Spot FX Alımı, Görevler Ayrılığı (SoD) çakışması ve Stop-Loss limit aşımı risklerine karşı kontrol aktiviteleri, test adımları ve mülakat walkthrough sorularını içeren RCM matrisi oluşturunuz.",
        "output_file": "phase2_rcm.png"
    },
    {
        "phase_name": "3. Saha Çalışması (Fieldwork & Testing)",
        "task_name": "Kontrol Tanımı ve Tasarım Zayıflığı Analizi",
        "input_text": "Mevcut Kontrol 1: 2.000.000 USD limitli sözlü döviz alımları gün sonunda Hazine Müdürü tarafından imzalanır.\nMevcut Kontrol 2: Akaryakıt deniz nakliyesinde binde 3 yerine şirket içi sirkülerle %2.5 fire toleransı uygulanır.\nBu iki kontrolün tasarım zafiyetlerini ve muğlak noktalarını analiz ediniz.",
        "output_file": "phase3_fieldwork.png"
    },
    {
        "phase_name": "4. Denetim Raporlama (Reporting)",
        "task_name": "5C Standart Denetim Bulgusu Yazımı",
        "input_text": "Levent şubesinde 145.000.000 USD tutarında sahte ekspertizli teminatsız kredi kullandırıldığı, LTV oranının %850'ye ulaştığı ve MASAK filtresi devre dışı bırakılarak 78.500.000 USD suç gelirinin Panama hesaplarına aktarıldığı saptanmıştır.",
        "output_file": "phase4_5c_finding.png"
    },
    {
        "phase_name": "5. Sürekli Denetim & Analitik (Analytics)",
        "task_name": "Python (Pandas) İstisna Analiz Kodu",
        "input_text": "25.000 satırlık bankacılık logları Excel veri tablosunda (devasa_bankacilik_ve_swift_loglari_25000satir.xlsx); ltv_ratio > 0.75 olan kredileri ve masak_filter_cleared == False olan offshore SWIFT transferlerini filtreleyen ve 'audit_exceptions.xlsx' dosyasına yazan Pandas kodunu üretiniz.",
        "output_file": "phase5_analytics_sandbox.png"
    }
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 1000})

    print("🌐 Streamlit Uygulamasına Bağlanılıyor...")
    page.goto("http://localhost:8501", wait_until="networkidle")
    time.sleep(3)

    for item in phases_data:
        p_name = item["phase_name"]
        t_name = item["task_name"]
        out_f = item["output_file"]

        print(f"\n📸 İşleniyor: {p_name} -> {t_name}")

        page.goto("http://localhost:8501", wait_until="networkidle")
        time.sleep(2)

        # 1. Aşama Seçimi
        phase_select = page.get_by_label("Denetim Aşaması:")
        if phase_select.count() > 0:
            phase_select.click(force=True)
            time.sleep(0.5)
            opt = page.get_by_role("option", name=p_name)
            if opt.count() > 0:
                opt.first.click()
                time.sleep(1)

        # 2. Görev Seçimi
        task_select = page.get_by_label("Görev Türü:")
        if task_select.count() > 0:
            task_select.click(force=True)
            time.sleep(0.5)
            opt_task = page.get_by_role("option", name=t_name)
            if opt_task.count() > 0:
                opt_task.first.click()
                time.sleep(1)

        # 3. Saha Notu Gir
        text_areas = page.locator("textarea")
        if text_areas.count() > 0:
            text_areas.first.fill(item["input_text"])
            time.sleep(0.5)

        # 4. Butona Bas
        run_btn = page.get_by_role("button", name="Çalışma Kağıdını Üret")
        if run_btn.count() > 0:
            run_btn.first.click()
            print("⏳ Model analizi yürütülüyor...")
            time.sleep(9)

        # 5. Ekran Görüntüsü Al
        save_path = os.path.join(screenshot_dir, out_f)
        page.screenshot(path=save_path, full_page=False)
        print(f"✅ Kaydedildi: {save_path}")

    browser.close()
    print("\n🎉 Tüm 5 Aşama Ekran Görüntüleri Başarıyla Alındı!")
