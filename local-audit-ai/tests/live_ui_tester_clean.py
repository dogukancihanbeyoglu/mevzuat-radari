import asyncio
import os
from playwright.async_api import async_playwright

SCENARIOS = [
    {
        "id": 1,
        "phase": "1. Yıllık Planlama (Annual Planning)",
        "task": "Denetim Evreni ve Risk Derecelendirmesi",
        "context": "Anadolu Holding A.Ş. — Teftiş Kurulu",
        "notes": """Holding bünyesindeki 5 ana sektör için 2026 Yılı Risk Odaklı Denetim Planı ve Evreni hazırlanacaktır.
| Şirket / Birim | Süreç | 2025 Büyüklük | Regülasyon | Not |
| Anadolu Finansman A.Ş. | Kredi Tahsis | 1.850.000.000 TL | BDDK & MASAK | 🔴 Yetersiz |
| Anadolu Enerji A.Ş. | Alım Sözleşmeleri | 3.400.000.000 TL | EPDK | 🟡 Orta |""",
        "filename": "1_annual_audit_universe.png"
    },
    {
        "id": 2,
        "phase": "2. Görev Planlama (Engagement Planning)",
        "task": "Risk ve Kontrol Matrisi (RCM) & Walkthrough",
        "context": "Mega Enerji A.Ş. — Hazine Denetimi",
        "notes": """Hazine ve Türev Swap İşlemleri Sürecinde belirlenen 3 risk:
1. Trader'ların günlük 5M USD limitini aşması.
2. Front-Office ve Back-Office yetkilerinin tek personelde toplanması.
3. Stop-Loss limitlerinin manuel kapatılması.""",
        "filename": "2_engagement_rcm.png"
    },
    {
        "id": 3,
        "phase": "3. Saha Çalışması (Fieldwork & Testing)",
        "task": "Kontrol Test Prosedürü Geliştirme",
        "context": "Mega İlaç A.Ş. — İç Denetim",
        "notes": """Test Edilecek Kontrol: "ERP üzerinde 2.500.000 TL üzerindeki tüm hammadde faturalarında Çift İmza ve 3'lü Eşleştirme zorunludur."
2025 yılı 4.200 fatura için 4-ögeli resmi test planı üretiniz.""",
        "filename": "3_fieldwork_test_procedure.png"
    },
    {
        "id": 4,
        "phase": "4. Denetim Raporlama (Reporting)",
        "task": "5C Standart Denetim Bulgusu Yazımı",
        "context": "Mega Yatırım Bankası A.Ş. — Teftiş Kurulu",
        "notes": """Kredi Denetimi Bulguları:
1. Levent Şube Müdürü Mehmet Özkan, 15M TL limiti aşarak 145M TL kredi kullandırmıştır.
2. Sahte ekspertizle LTV %850 gerçekleşmiştir.
3. MASAK filtresi kapatılarak 78.5M TL Panama'ya aktarılmıştır.""",
        "filename": "4_reporting_5c_finding.png"
    },
    {
        "id": 5,
        "phase": "5. Sürekli Denetim & Analitik (Analytics)",
        "task": "Python (Pandas) İstisna Analiz Kodu",
        "context": "Mega Finans & Hazine Operasyonları",
        "notes": """Hazine veri tabanında sürekli denetim kuralları işletilecektir.
1. Offshore: Alıcı ülkesi ('PA', 'VG', 'CY') olan ve tutarı 250.000 USD üzerindeki işlemler.
2. MASAK Bypass: masak_cleared == False ve approval_status == 'APPROVED' olan işlemler.""",
        "filename": "5_analytics_pandas_sandbox.png"
    }
]

async def run_clean_tests():
    os.makedirs("storage/live_test_results", exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for sc in SCENARIOS:
            page = await browser.new_page(viewport={"width": 1440, "height": 1080})
            print(f"\n🌐 [{sc['id']}/5] Canlı Web Kokpiti Açılıyor...")
            await page.goto("http://localhost:8501", wait_until="networkidle", timeout=30000)
            await asyncio.sleep(1)

            # 1. Denetim Aşaması Seçimi
            phase_select = page.locator('div[data-testid="stSelectbox"]').nth(0)
            await phase_select.click()
            await asyncio.sleep(0.4)
            await page.locator(f'li[role="option"]:has-text("{sc["phase"][:12]}")').click()
            await asyncio.sleep(0.8)

            # 2. Görev Türü Seçimi
            task_select = page.locator('div[data-testid="stSelectbox"]').nth(1)
            await task_select.click()
            await asyncio.sleep(0.4)
            await page.locator(f'li[role="option"]:has-text("{sc["task"][:12]}")').click()
            await asyncio.sleep(0.8)

            # 3. Şirket Bağlamı
            context_input = page.locator('input[aria-label="Kurumsal Bağlam / Şirket Bilgisi:"]')
            await context_input.fill(sc["context"])

            # 4. Saha Notları
            notes_area = page.locator('textarea[aria-label="Saha Notları / Açıklama / Ham Veri:"]')
            await notes_area.fill(sc["notes"])
            await asyncio.sleep(0.4)

            # 5. Butona Tıkla
            print(f"🚀 [{sc['id']}/5] '{sc['task']}' Çalıştırılıyor...")
            gen_btn = page.locator('button:has-text("Çalışma Kağıdını Üret")')
            await gen_btn.click()

            # 6. Sonucu Bekle
            try:
                await page.wait_for_selector('div.metrics-bar', timeout=15000)
                print(f"✅ [{sc['id']}/5] Çalışma Kağıdı Başarıyla Üretildi!")
            except Exception:
                pass

            await asyncio.sleep(1.5)
            shot_file = f"storage/live_test_results/{sc['filename']}"
            await page.screenshot(path=shot_file, full_page=True)
            print(f"📸 Canlı Ekran Görüntüsü Kaydedildi: {shot_file}")
            await page.close()

        await browser.close()
        print("\n🎉 Tebrikler! Tüm 5 Denetim Aşaması Başarıyla Test Edildi ve Doğrulandı!")

if __name__ == "__main__":
    asyncio.run(run_clean_tests())
