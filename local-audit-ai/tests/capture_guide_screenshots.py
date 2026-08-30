"""
Auditoris - Gerçek Ekran Görüntüsü Yakalayıcı (Playwright Screenshot Bot)
Kullanıcı kılavuzu için sistemin gerçek arayüzünden ekran görüntüleri yakalar.
"""
import os
import time
from playwright.sync_api import sync_playwright

screenshot_dir = "storage/screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 900})

    print("🌐 1. Streamlit Uygulamasına Bağlanılıyor...")
    page.goto("http://localhost:8501", wait_until="networkidle")
    time.sleep(3)

    # 1. Ana Ekran ve Görev Seçimi
    print("📸 2. Ana Ekran & Görev Seçimi Ekran Görüntüsü Alınıyor...")
    page.screenshot(path=os.path.join(screenshot_dir, "01_main_cockpit.png"), full_page=False)

    # 2. Saha Notları Girişi Yap
    print("✍️ 3. Örnek Saha Notu Giriliyor...")
    text_areas = page.locator("textarea")
    if text_areas.count() > 0:
        text_areas.first.fill(
            "Levent şubesinde 145.000.000 USD teminatsız kredi kullandırıldığı ve "
            "MASAK filtresi devre dışı bırakılarak 78.500.000 USD Panama transferi yapıldığı tespit edilmiştir."
        )

    time.sleep(1)
    page.screenshot(path=os.path.join(screenshot_dir, "02_data_and_notes_input.png"), full_page=False)

    # 3. Butona Bas ve Çıktıyı Bekle
    print("🚀 4. 'Çalışma Kağıdını Üret' Butonuna Basılıyor...")
    run_btn = page.get_by_role("button", name="Çalışma Kağıdını Üret")
    if run_btn.count() > 0:
        run_btn.first.click()
        time.sleep(6) # Model yanıtını bekle

    print("📸 5. 5C Çıktı, QA Kalite Paneli ve RAG Kartları Ekran Görüntüsü Alınıyor...")
    page.screenshot(path=os.path.join(screenshot_dir, "03_audit_result_and_quality.png"), full_page=False)

    browser.close()
    print("🎉 Tüm Ekran Görüntüleri Başarıyla Kaydedildi:", os.listdir(screenshot_dir))
