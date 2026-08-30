import asyncio
import os
import time
from playwright.async_api import async_playwright

SCENARIOS = [
    {
        "id": 1,
        "phase_idx": 0, # 1. Yıllık Planlama
        "task_idx": 0,  # Denetim Evreni
        "phase_name": "1. Yıllık Planlama (Annual Planning)",
        "task_name": "Denetim Evreni ve Risk Derecelendirmesi",
        "context": "Anadolu Holding A.Ş. — Teftiş Kurulu Başkanlığı",
        "notes": """Holding bünyesindeki 5 ana sektör için 2026 Yılı Risk Odaklı Denetim Planı ve Evreni hazırlanacaktır.
| Şirket / Birim | Süreç | 2025 Büyüklük | Regülasyon | Not |
| Anadolu Finansman A.Ş. | Kredi Tahsis | 1.850.000.000 TL | BDDK & MASAK | 🔴 Yetersiz |
| Anadolu Enerji A.Ş. | Alım Sözleşmeleri | 3.400.000.000 TL | EPDK | 🟡 Orta |
| Anadolu Lojistik | Akaryakıt Filo | 620.000.000 TL | Ulaştırma | 🟢 İyi |
| Anadolu Teknoloji | Bulut & PAM | 450.000.000 TL | KVKK & ISO 27001 | 🔴 Yetersiz |""",
        "is_analytics": False
    },
    {
        "id": 2,
        "phase_idx": 1, # 2. Görev Planlama
        "task_idx": 0,  # RCM & Walkthrough
        "phase_name": "2. Görev Planlama (Engagement Planning)",
        "task_name": "Risk ve Kontrol Matrisi (RCM) & Walkthrough",
        "context": "Mega Enerji ve Emtia Ticareti A.Ş. — Hazine Denetimi",
        "notes": """Hazine ve Türev Swap İşlemleri Sürecinde belirlenen 3 kritik operasyonel risk:
1. Trader'ların günlük 5.000.000 USD limitini aşarak yetkisiz pozisyon açması.
2. Front-Office ve Back-Office yetkilerinin tek personelde toplanması (SoD ihlali).
3. Piyasa dalgalandığında Stop-Loss limitlerinin manuel kapatılması.""",
        "is_analytics": False
    },
    {
        "id": 3,
        "phase_idx": 2, # 3. Saha Çalışması
        "task_idx": 0,  # Kontrol Test Prosedürü
        "phase_name": "3. Saha Çalışması (Fieldwork & Testing)",
        "task_name": "Kontrol Test Prosedürü Geliştirme",
        "context": "Mega İlaç ve Sağlık Ürünleri A.Ş. — İç Denetim",
        "notes": """Test Edilecek Kontrol: "ERP üzerinde 2.500.000 TL üzerindeki tüm hammadde satınalma faturalarında Çift Dijital İmza (Satınalma Direktörü + CFO) ve PO-GR-Invoice 3'lü Eşleştirme kuralı zorunludur."
2025 yılı 4.200 fatura için 4-ögeli resmi test planı üretiniz.""",
        "is_analytics": False
    },
    {
        "id": 4,
        "phase_idx": 3, # 4. Denetim Raporlama
        "task_idx": 0,  # 5C Standart Bulgusu
        "phase_name": "4. Denetim Raporlama (Reporting)",
        "task_name": "5C Standart Denetim Bulgusu Yazımı",
        "context": "Mega Yatırım Bankası A.Ş. — Teftiş Kurulu",
        "notes": """Kredi Denetimi Bulguları:
1. Levent Şube Müdürü Mehmet Özkan, 15M TL limiti aşarak 145M TL kredi kullandırmıştır.
2. Sahte ekspertizle Riva taşınmazında LTV %850 gerçekleşmiştir.
3. Kredi sonrası MASAK filtresi kapatılarak 78.5M TL Panama hesabına aktarılmıştır.
4. Şube Müdürünün hesabına Atlas Lojistik tarafından 4.5M TL komisyon yatırılmıştır.""",
        "is_analytics": False
    },
    {
        "id": 5,
        "phase_idx": 4, # 5. Sürekli Denetim & Analitik
        "task_idx": 0,  # Python İstisna Analiz Kodu
        "phase_name": "5. Sürekli Denetim & Analitik (Analytics)",
        "task_name": "Python (Pandas) İstisna Analiz Kodu",
        "context": "Mega Finans & Hazine Operasyonları",
        "notes": """Hazine veri tabanında sürekli denetim kuralları işletilecektir:
1. Offshore: Alıcı ülkesi ('PA', 'VG', 'CY', 'SC') olan ve tutarı 250.000 USD üzerindeki işlemler.
2. MASAK Bypass: masak_cleared == False ve approval_status == 'APPROVED' olan işlemler.
3. Yetkisiz Kredi: transfer_type == 'CREDIT_DISBURSEMENT' ve amount_usd >= 1.000.000 olan işlemler.""",
        "is_analytics": True
    }
]

async def run_patient_chrome_tests():
    print("\n🖥️ Google Chrome Penceresi Açılıyor (Kusursuz Canlı İnceleme Modu)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=200,
            args=["--start-maximized", "--window-size=1440,950"]
        )
        context = await browser.new_context(viewport={"width": 1440, "height": 950})
        page = await context.new_page()

        for sc in SCENARIOS:
            print(f"\n======================================================================")
            print(f"🚀 [{sc['id']}/5] BAŞLATILIYOR: {sc['phase_name']} ➔ {sc['task_name']}")
            print(f"======================================================================")

            print("🌐 Web Kokpiti Yükleniyor: http://localhost:8501")
            await page.goto("http://localhost:8501", wait_until="networkidle", timeout=60000)
            await asyncio.sleep(1.5)

            # Görünür selectbox'ları al
            visible_selects = page.locator('div[data-testid="stSelectbox"]:visible')
            
            # 1. Aşama Seç
            print(f"📌 1. Aşama Seçiliyor: {sc['phase_name']}")
            await visible_selects.nth(0).click()
            await asyncio.sleep(0.4)
            options = page.locator('li[role="option"]')
            await options.nth(sc["phase_idx"]).click()
            await asyncio.sleep(0.8)

            # 2. Görev Seç
            print(f"📌 2. Görev Türü Seçiliyor: {sc['task_name']}")
            await visible_selects.nth(1).click()
            await asyncio.sleep(0.4)
            task_options = page.locator('li[role="option"]')
            await task_options.nth(sc["task_idx"]).click()
            await asyncio.sleep(0.8)

            # 3. Şirket Bağlamı Girişi
            print(f"✍️ 3. Şirket Bağlamı Giriliyor: {sc['context']}")
            ctx_input = page.locator('input[aria-label="Kurumsal Bağlam / Şirket Bilgisi:"]')
            if await ctx_input.count() > 0:
                await ctx_input.fill(sc["context"])
                await asyncio.sleep(0.4)

            # 4. Saha Notları Girişi
            print(f"✍️ 4. Saha Notları ve Tablo Giriliyor...")
            notes_input = page.locator('textarea[aria-label="Saha Notları / Açıklama / Ham Veri:"]')
            if await notes_input.count() > 0:
                await notes_input.fill(sc["notes"])
                await asyncio.sleep(0.5)

            # 5. Çalışma Kağıdını Üret Butonuna Tıkla
            print(f"⚡ 5. 'Çalışma Kağıdını Üret' Butonuna Tıklanıyor...")
            gen_btn = page.locator('button:has-text("Çalışma Kağıdını Üret")')
            await gen_btn.click()

            # 6. MODEL YANITI DÖNENE KADAR SABIRLA BEKLE (180 Saniyeye Kadar)
            print("⏳ Model analizi çalışıyor... Sonuçların ekrana tam olarak yansıması bekleniyor...")
            
            start_wait = time.time()
            # Hem Kalite Skoru barının gelmesini hem spinner'ın bitmesini bekle
            await page.wait_for_selector('div.metrics-bar', timeout=180000)
            elapsed_wait = round(time.time() - start_wait, 1)
            print(f"✅ 6. MODEL ÇIKTISI EKRANA TAM OTURDU! (Bekleme Süresi: {elapsed_wait} sn)")

            # 7. Sayfayı Sonuçlara Doğru Yavaşça Kaydır
            print("📜 7. Çalışma Kağıdı ve RAG Kartları İnceleniyor...")
            await page.evaluate("window.scrollBy(0, 480)")
            await asyncio.sleep(3)

            # 8. Alttaki 3 Sekmeyi Teker Teker Açıp Doğrula
            print("🔍 8.1. [Model & Akıllı Yönlendirme Analizi] Sekmesi Açılıyor...")
            tab_model = page.locator('button[role="tab"]:has-text("Model & Akıllı Yönlendirme")')
            if await tab_model.count() > 0:
                await tab_model.click()
                await asyncio.sleep(3.5)

            print("🔒 8.2. [Güvenlik, PII & Audit Trail JSON] Sekmesi Açılıyor...")
            tab_sec = page.locator('button[role="tab"]:has-text("Güvenlik & Denetim İzi")')
            if await tab_sec.count() > 0:
                await tab_sec.click()
                await asyncio.sleep(3.5)

            print("📄 8.3. [IIA Çalışma Kağıdı] Ana Sekmesine Geri Dönülüyor...")
            tab_wp = page.locator('button[role="tab"]:has-text("IIA Çalışma Kağıdı")')
            if await tab_wp.count() > 0:
                await tab_wp.click()
                await asyncio.sleep(2)

            # 9. Analitik Görevi İse: Sandbox'ta Koştur ve Sonucu Bekle
            if sc["is_analytics"]:
                print("⚡ 9. Python Sandbox Yürütme Butonuna Basılıyor...")
                sandbox_btn = page.locator('button:has-text("Kodu Sandbox\'ta Çalıştır")')
                if await sandbox_btn.count() > 0:
                    await sandbox_btn.click()
                    print("   ⏳ Python kodu izole sandbox'ta koşturuluyor...")
                    await page.wait_for_selector('text=Python analitik kodu izole sandbox\'ta başarıyla çalıştırıldı', timeout=60000)
                    print("   🎉 SANDBOX BAŞARIYLA ÇALIŞTI VE audit_exceptions.xlsx ÜRETİLDİ!")
                    await asyncio.sleep(4)

            # 10. Sonuç Ekran Görüntüsünü Kaydet
            os.makedirs("storage/screenshots", exist_ok=True)
            shot_file = f"storage/screenshots/task_{sc['id']:02d}_{sc['phase_idx']}_{sc['task_idx']}_live.png"
            await page.screenshot(path=shot_file, full_page=True)
            print(f"📸 [%100 TAM SONUÇLU] Ekran Görüntüsü Kaydedildi: {shot_file}")

            # Kullanıcının ekranda rahatça inceleyebilmesi için canlı bekleme
            print(f"👀 [{sc['id']}/5] {sc['task_name']} Sonuçları Ekranda İnceleniyor (6 saniye canlı bekleme)...")
            await asyncio.sleep(6)

        print("\n🎉🎉🎉 TEBRİKLER! TÜM 5 DENETİM AŞAMASININ CANLI SONUÇLARI, MODEL ANALİZLERİ VE SANDBOX TESTLERİ EKSİKSİZ TAMAMLANDI!")
        await asyncio.sleep(4)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_patient_chrome_tests())
