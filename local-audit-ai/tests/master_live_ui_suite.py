import asyncio
import json
import os
import time
from playwright.async_api import async_playwright

async def run_master_suite():
    with open("storage/test_scenarios_library.json", "r", encoding="utf-8") as f:
        scenarios = json.load(f)

    os.makedirs("storage/screenshots", exist_ok=True)
    print("\n" + "="*80)
    print("🌟 AUDITORIS 2026 — 10 GÖREV TÜRÜ MASTER CANLI UI & FONKSİYON TEST SUITE BAŞLADI")
    print("="*80)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=200,
            args=["--start-maximized", "--window-size=1440,950"]
        )
        context = await browser.new_context(viewport={"width": 1440, "height": 950})
        page = await context.new_page()

        for sc in scenarios:
            print(f"\n----------------------------------------------------------------------")
            print(f"🚀 [{sc['id']}/10] TEST EDİLİYOR: {sc['phase_name']} ➔ {sc['task_name']}")
            print(f"----------------------------------------------------------------------")

            await page.goto("http://localhost:8501", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(1.5)

            # Görünür selectbox'ları al (Ana sayfa selectbox'ları)
            visible_selects = page.locator('div[data-testid="stSelectbox"]:visible')

            # 1. Denetim Aşaması Seçimi
            print(f"📌 [1/4] Aşama Seçiliyor: {sc['phase_name']}")
            await visible_selects.nth(0).click()
            await asyncio.sleep(0.4)
            options = page.locator('li[role="option"]')
            await options.nth(sc["phase_idx"]).click()
            await asyncio.sleep(0.8)

            # 2. Görev Türü Seçimi
            print(f"📌 [2/4] Görev Türü Seçiliyor: {sc['task_name']}")
            await visible_selects.nth(1).click()
            await asyncio.sleep(0.4)
            task_options = page.locator('li[role="option"]')
            await task_options.nth(sc["task_idx"]).click()
            await asyncio.sleep(0.8)

            # 3. Kurumsal Bağlam Girişi
            print(f"✍️ [3/4] Kurumsal Bağlam: {sc['context']}")
            ctx_input = page.locator('input[aria-label="Kurumsal Bağlam / Şirket Bilgisi:"]')
            if await ctx_input.count() > 0:
                await ctx_input.fill(sc["context"])
                await asyncio.sleep(0.3)

            # 4. Saha Notları Girişi
            print(f"✍️ [4/4] Saha Notları ve Tablo Giriliyor...")
            notes_input = page.locator('textarea[aria-label="Saha Notları / Açıklama / Ham Veri:"]')
            if await notes_input.count() > 0:
                await notes_input.fill(sc["input_data"])
                await asyncio.sleep(0.5)

            # 5. Çalışma Kağıdını Üret Butonuna Tıkla
            print(f"⚡ [İŞLEM] 'Çalışma Kağıdını Üret' Tıklandı. Model analizi yürütülüyor...")
            gen_btn = page.locator('button:has-text("Çalışma Kağıdını Üret")')
            await gen_btn.click()

            # 6. MODEL ÇIKTISININ EKRANA TAM OLARAK GELMESİNİ BEKLE
            start_t = time.time()
            await page.wait_for_selector('div.metrics-bar', timeout=180000)
            elapsed_t = round(time.time() - start_t, 1)
            print(f"✅ [SONUÇ GELDİ] Çalışma Kağıdı ve Kalite Skoru Ekrana Oturdu! ({elapsed_t} sn)")

            # 7. Sayfayı Sonuçlara Doğru Kaydır
            await page.evaluate("window.scrollBy(0, 480)")
            await asyncio.sleep(2)

            # 8. Alttaki Fonksiyonel Sekmeleri Canlı Test Et
            # 8.1 Model Sekmesi
            tab_model = page.locator('button[role="tab"]:has-text("Model & Akıllı Yönlendirme")')
            if await tab_model.count() > 0:
                await tab_model.click()
                await asyncio.sleep(2.5)

            # 8.2 Güvenlik & Audit Trail JSON Sekmesi
            tab_sec = page.locator('button[role="tab"]:has-text("Güvenlik & Denetim İzi")')
            if await tab_sec.count() > 0:
                await tab_sec.click()
                await asyncio.sleep(2.5)

            # 8.3 Ana Çalışma Kağıdı Sekmesine Dönüş
            tab_wp = page.locator('button[role="tab"]:has-text("IIA Çalışma Kağıdı")')
            if await tab_wp.count() > 0:
                await tab_wp.click()
                await asyncio.sleep(1.5)

            # 9. Analitik Görevi İse: Sandbox'ta Koştur
            if sc["is_analytics"]:
                print("⚡ [SANDBOX] 'Kodu Sandbox\'ta Çalıştır' Tıklanıyor...")
                sandbox_btn = page.locator('button:has-text("Kodu Sandbox\'ta Çalıştır")')
                if await sandbox_btn.count() > 0:
                    await sandbox_btn.click()
                    await page.wait_for_selector('text=Python analitik kodu izole sandbox\'ta başarıyla çalıştırıldı', timeout=60000)
                    print("   🎉 SANDBOX KODU ÇALIŞTI VE audit_exceptions.xlsx ÜRETİLDİ!")
                    await asyncio.sleep(3)

            # 10. %100 DOLU VE ÇALIŞIR DURUMDAKİ EKRAN GÖRÜNTÜSÜNÜ KAYDET
            shot_file = f"storage/screenshots/task_{sc['id']:02d}_{sc['task_key']}.png"
            await page.screenshot(path=shot_file, full_page=True)
            print(f"📸 [KANIT KAYDEDİLDİ] Ekran Görüntüsü Alındı: {shot_file}")

            # Kullanıcının ekranda rahatça görmesi için duraklama
            await asyncio.sleep(4)

        print("\n" + "="*80)
        print("🎉🎉🎉 TEBRİKLER! 10 GÖREVİN TAMAMININ CANLI UI TESTİ VE SS ALIMI BAŞARIYLA BİTTİ!")
        print("="*80)
        await asyncio.sleep(3)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_master_suite())
