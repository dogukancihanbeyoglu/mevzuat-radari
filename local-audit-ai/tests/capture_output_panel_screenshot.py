"""
Auditoris - Çıktı ve İhraç Paneli Ekran Görüntüsü Yakalayıcı
Word, Excel, Sandbox indirme butonları ve denetim izi alanını yakalar.
"""
import os
import time
from playwright.sync_api import sync_playwright

screenshot_dir = "storage/screenshots"
os.makedirs(screenshot_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 1100})

    print("🌐 Streamlit Uygulamasına Bağlanılıyor...")
    page.goto("http://localhost:8501", wait_until="networkidle")
    time.sleep(2)

    # 4. Aşama 5C Seç
    phase_select = page.get_by_label("Denetim Aşaması:")
    if phase_select.count() > 0:
        phase_select.click(force=True)
        time.sleep(0.5)
        page.get_by_role("option", name="4. Denetim Raporlama (Reporting)").click()
        time.sleep(1)

    # Saha Notu Gir
    text_areas = page.locator("textarea")
    if text_areas.count() > 0:
        text_areas.first.fill(
            "Levent şubesinde 145.000.000 USD tutarında sahte ekspertizli teminatsız kredi kullandırıldığı, "
            "LTV oranının %850'ye ulaştığı ve MASAK filtresi devre dışı bırakılarak 78.500.000 USD suç gelirinin Panama hesaplarına aktarıldığı saptanmıştır."
        )

    # Butona Bas
    run_btn = page.get_by_role("button", name="Çalışma Kağıdını Üret")
    if run_btn.count() > 0:
        run_btn.first.click()
        print("⏳ Model analizi bekleniyor...")
        time.sleep(8)

    # Çıktı ve İndirme Butonlarının Görünümünü Yakala
    save_path = os.path.join(screenshot_dir, "outputs_and_export_panel.png")
    page.screenshot(path=save_path, full_page=False)
    print(f"✅ Çıktı Paneli Kaydedildi: {save_path}")

    browser.close()
