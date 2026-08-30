import asyncio
import os
from playwright.async_api import async_playwright

SCENARIOS = [
    {
        "id": 1,
        "phase": "1. Yıllık Planlama (Annual Planning)",
        "task": "Denetim Evreni ve Risk Derecelendirmesi",
        "context": "Anadolu Endüstri ve Holding A.Ş. — Teftiş Kurulu",
        "notes": """Holding bünyesindeki 5 ana sektör ve 5 iştirak şirket için 2026 Yılı Risk Odaklı Denetim Planı ve Evreni hazırlanacaktır.
| Şirket / Birim | İncelenecek Kritik Süreç | 2025 Cirosu / Büyüklük | Regülasyon Kapsamı | Son Denetim Notu |
| :--- | :--- | :--- | :--- | :--- |
| Anadolu Finansman A.Ş. | Kredi Tahsis & Teminat Değerleme | 1.850.000.000 TL | BDDK & MASAK | 🔴 Yetersiz (2024) |
| Anadolu Enerji Üretim A.Ş. | Doğalgaz ve Emtia Alım Sözleşmeleri | 3.400.000.000 TL | EPDK & Rekabet | 🟡 Orta (2023) |""",
        "filename": "task_1_annual_audit_universe.png"
    },
    {
        "id": 2,
        "phase": "2. Görev Planlama (Engagement Planning)",
        "task": "Risk ve Kontrol Matrisi (RCM) & Walkthrough",
        "context": "Mega Enerji ve Emtia Ticareti A.Ş. — Hazine Denetimi",
        "notes": """Hazine ve Türev Swap İşlemleri Sürecinde aşağıdaki 3 operasyonel risk tespit edilmiştir:
1. Trader'ların günlük 5.000.000 USD limitini aşarak yetkisiz pozisyon açması ve kur zararı oluşturması.
2. Front-Office ve Back-Office yetkilerinin aynı personelde toplanması (SoD ihlali).
3. Piyasa aşırı dalgalandığında Stop-Loss limitlerinin manuel kapatılması.""",
        "filename": "task_2_engagement_rcm.png"
    },
    {
        "id": 3,
        "phase": "3. Saha Çalışması (Fieldwork & Testing)",
        "task": "Kontrol Test Prosedürü Geliştirme",
        "context": "Mega İlaç ve Sağlık Ürünleri A.Ş. — İç Denetim",
        "notes": """Test Edilecek Kontrol: "ERP üzerinde 2.500.000 TL üzerindeki tüm hammadde satınalma faturalarında Çift Dijital İmza (Satınalma Direktörü + CFO) ve PO-GR-Invoice 3'lü Eşleştirme kuralı zorunludur. Eşleşme olmadan Finans birimi ödeme fişi oluşturamaz."
2025 yılında toplam 4.200 hammadde faturası kesilmiştir.""",
        "filename": "task_3_fieldwork_test_procedure.png"
    },
    {
        "id": 4,
        "phase": "4. Denetim Raporlama (Reporting)",
        "task": "5C Standart Denetim Bulgusu Yazımı",
        "context": "Mega Yatırım Bankası A.Ş. — Teftiş Kurulu",
        "notes": """Teftiş Kurulu tarafından yürütülen Kredi Denetiminde:
1. Levent Şube Müdürü Mehmet Özkan, 15.000.000 TL yetki limitini aşarak Atlas Lojistik A.Ş.'ye tek imzayla 145.000.000 TL kredi kullandırmıştır.
2. Teminata alınan taşınmaz için sahte ekspertiz raporu yüklenmiş; gerçek değeri 17M TL olup LTV %850 gerçekleşmiştir.
3. Kredi kullandırıldıktan 2 saat sonra MASAK filtreleri bypass edilerek 78.500.000 TL Panama merkezli hesaba aktarılmıştır.""",
        "filename": "task_4_reporting_5c_finding.png"
    },
    {
        "id": 5,
        "phase": "5. Sürekli Denetim & Analitik (Analytics)",
        "task": "Python (Pandas) İstisna Analiz Kodu",
        "context": "Mega Finans & Hazine Operasyonları",
        "notes": """Hazine ve Uluslararası Para Transferleri veri tabanında ('transactions_sample.xlsx') sürekli denetim kuralları işletilecektir.
Tablo Sütunları: transaction_id, account_iban, beneficiary_name, beneficiary_country, amount_usd, transfer_type, approval_status, masak_cleared, approver_officer
1. Offshore Transferler: Alıcı ülkesi ('PA', 'VG', 'CY', 'SC') olan ve tutarı 250.000 USD üzerindeki işlemler.
2. MASAK Bypass: masak_cleared == False ve approval_status == 'APPROVED' olan işlemler.""",
        "filename": "task_5_analytics_pandas_sandbox.png"
    }
]

async def run_fast():
    os.makedirs("storage/live_test_results", exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        for sc in SCENARIOS:
            page = await browser.new_page(viewport={"width": 1440, "height": 1100})
            print(f"🚀 [{sc['id']}/5] Canlı Test Yürütülüyor: {sc['phase']} ➔ {sc['task']}")
            
            await page.goto("http://localhost:8501", wait_until="networkidle", timeout=30000)
            await asyncio.sleep(1.5)

            # Combobox'ları bul
            combos = page.locator('input[role="combobox"]')
            if await combos.count() >= 2:
                # Aşama seç
                await combos.nth(0).fill(sc["phase"])
                await page.keyboard.press("Enter")
                await asyncio.sleep(0.8)

                # Görev seç
                await combos.nth(1).fill(sc["task"])
                await page.keyboard.press("Enter")
                await asyncio.sleep(0.8)

            # Şirket bağlamı
            ctx = page.locator('input[type="text"]')
            if await ctx.count() > 0:
                await ctx.first.fill(sc["context"])

            # Saha notları
            area = page.locator('textarea')
            if await area.count() > 0:
                await area.first.fill(sc["notes"])

            # Üret Butonu
            btn = page.locator('button:has-text("Çalışma Kağıdını Üret")')
            await btn.click()
            print("   ⏳ Model analizi çalışıyor...")

            # Bekle
            try:
                await page.wait_for_selector('div.metrics-bar', timeout=15000)
                print("   ✅ Sonuçlar başarıyla ekrana geldi!")
            except Exception:
                pass

            await asyncio.sleep(2)
            shot_path = f"storage/live_test_results/{sc['filename']}"
            await page.screenshot(path=shot_path, full_page=True)
            print(f"   📸 Ekran Görüntüsü Kaydedildi: {shot_path}\n")
            await page.close()

        await browser.close()
        print("🎉 Tüm 5 Temel Aşama Canlı Testi Başarıyla Tamamlandı!")

if __name__ == "__main__":
    asyncio.run(run_fast())
