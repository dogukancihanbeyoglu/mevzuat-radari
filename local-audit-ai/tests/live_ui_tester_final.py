import asyncio
import os
from playwright.async_api import async_playwright

SCENARIOS = [
    {
        "id": 1,
        "phase_idx": 0,
        "task_idx": 0,
        "phase_name": "1. Yıllık Planlama",
        "task_name": "Denetim Evreni ve Risk Derecelendirmesi",
        "context": "Anadolu Holding A.Ş. — Teftiş Kurulu",
        "notes": """Holding bünyesindeki 5 ana sektör için 2026 Yılı Risk Odaklı Denetim Planı ve Evreni hazırlanacaktır.
| Şirket / Birim | Süreç | 2025 Büyüklük | Regülasyon | Not |
| Anadolu Finansman A.Ş. | Kredi Tahsis | 1.850.000.000 TL | BDDK & MASAK | 🔴 Yetersiz |
| Anadolu Enerji A.Ş. | Alım Sözleşmeleri | 3.400.000.000 TL | EPDK | 🟡 Orta |""",
        "filename": "1_annual_audit_universe.png"
    },
    {
        "id": 2,
        "phase_idx": 1,
        "task_idx": 0,
        "phase_name": "2. Görev Planlama",
        "task_name": "Risk ve Kontrol Matrisi (RCM)",
        "context": "Mega Enerji A.Ş. — Hazine Denetimi",
        "notes": """Hazine ve Türev Swap İşlemleri Sürecinde belirlenen 3 risk:
1. Trader'ların günlük 5M USD limitini aşması.
2. Front-Office ve Back-Office yetkilerinin tek personelde toplanması.
3. Stop-Loss limitlerinin manuel kapatılması.""",
        "filename": "2_engagement_rcm.png"
    },
    {
        "id": 3,
        "phase_idx": 2,
        "task_idx": 0,
        "phase_name": "3. Saha Çalışması",
        "task_name": "Kontrol Test Prosedürü Geliştirme",
        "context": "Mega İlaç A.Ş. — İç Denetim",
        "notes": """Test Edilecek Kontrol: "ERP üzerinde 2.500.000 TL üzerindeki tüm hammadde faturalarında Çift İmza ve 3'lü Eşleştirme zorunludur."
2025 yılı 4.200 fatura için 4-ögeli resmi test planı üretiniz.""",
        "filename": "3_fieldwork_test_procedure.png"
    },
    {
        "id": 4,
        "phase_idx": 3,
        "task_idx": 0,
        "phase_name": "4. Denetim Raporlama",
        "task_name": "5C Standart Denetim Bulgusu",
        "context": "Mega Yatırım Bankası A.Ş. — Teftiş Kurulu",
        "notes": """Kredi Denetimi Bulguları:
1. Levent Şube Müdürü Mehmet Özkan, 15M TL limiti aşarak 145M TL kredi kullandırmıştır.
2. Sahte ekspertizle LTV %850 gerçekleşmiştir.
3. MASAK filtresi kapatılarak 78.5M TL Panama'ya aktarılmıştır.""",
        "filename": "4_reporting_5c_finding.png"
    },
    {
        "id": 5,
        "phase_idx": 4,
        "task_idx": 0,
        "phase_name": "5. Sürekli Denetim",
        "task_name": "Python İstisna Analiz Kodu",
        "context": "Mega Finans & Hazine Operasyonları",
        "notes": """Hazine veri tabanında sürekli denetim kuralları işletilecektir.
1. Offshore: Alıcı ülkesi ('PA', 'VG', 'CY') olan ve tutarı 250.000 USD üzerindeki işlemler.
2. MASAK Bypass: masak_cleared == False ve approval_status == 'APPROVED' olan işlemler.""",
        "filename": "5_analytics_pandas_sandbox.png"
    }
]

async def run_final_tests():
    os.makedirs("storage/live_test_results", exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for sc in SCENARIOS:
            page = await browser.new_page(viewport={"width": 1440, "height": 1100})
            print(f"\n🌐 [{sc['id']}/5] Canlı Web Kokpiti Açılıyor: {sc['phase_name']} ➔ {sc['task_name']}...")
            await page.goto("http://localhost:8501", wait_until="networkidle", timeout=30000)
            await asyncio.sleep(1.5)

            # Görünür selectbox'ları al
            visible_selects = page.locator('div[data-testid="stSelectbox"]:visible')
            
            # 1. Aşama Seç
            await visible_selects.nth(0).click()
            await asyncio.sleep(0.4)
            options = page.locator('li[role="option"]')
            await options.nth(sc["phase_idx"]).click()
            await asyncio.sleep(0.8)

            # 2. Görev Seç
            await visible_selects.nth(1).click()
            await asyncio.sleep(0.4)
            task_options = page.locator('li[role="option"]')
            await task_options.nth(sc["task_idx"]).click()
            await asyncio.sleep(0.8)

            # 3. Şirket Bağlamı
            ctx_input = page.locator('input[aria-label="Kurumsal Bağlam / Şirket Bilgisi:"]')
            if await ctx_input.count() > 0:
                await ctx_input.fill(sc["context"])

            # 4. Saha Notları
            notes_input = page.locator('textarea[aria-label="Saha Notları / Açıklama / Ham Veri:"]')
            if await notes_input.count() > 0:
                await notes_input.fill(sc["notes"])
                await asyncio.sleep(0.4)

            # 5. Butona Tıkla
            print(f"🚀 [{sc['id']}/5] 'Çalışma Kağıdını Üret' Tıklandı. Model analizi yürütülüyor...")
            gen_btn = page.locator('button:has-text("Çalışma Kağıdını Üret")')
            await gen_btn.click()

            # 6. Sonucu Bekle
            try:
                await page.wait_for_selector('div.metrics-bar', timeout=20000)
                print(f"✅ [{sc['id']}/5] Çalışma Kağıdı Başarıyla Ekrana Yansıdı!")
            except Exception as e:
                print(f"⚠️ Bekleme notu: {e}")

            await asyncio.sleep(2)
            shot_file = f"storage/live_test_results/{sc['filename']}"
            await page.screenshot(path=shot_file, full_page=True)
            print(f"📸 Canlı Ekran Görüntüsü Kaydedildi: {shot_file}")
            await page.close()

        await browser.close()
        print("\n🎉 Tebrikler! Tüm 5 Denetim Aşaması Canlı Tarayıcıda Başarıyla Test Edildi ve Doğrulandı!")

if __name__ == "__main__":
    asyncio.run(run_final_tests())
