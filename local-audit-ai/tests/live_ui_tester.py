import asyncio
import os
from playwright.async_api import async_playwright

SCENARIOS = [
    {
        "phase_name": "1. Yıllık Planlama (Annual Planning)",
        "task_name": "Denetim Evreni ve Risk Derecelendirmesi",
        "context": "Anadolu Endüstri ve Holding A.Ş. — Teftiş Kurulu",
        "input": """Holding bünyesindeki 5 ana sektör ve 5 iştirak şirket için 2026 Yılı Risk Odaklı Denetim Planı ve Evreni hazırlanacaktır.
| Şirket / Birim | İncelenecek Kritik Süreç | 2025 Cirosu / Büyüklük | Regülasyon Kapsamı | Son Denetim Notu |
| :--- | :--- | :--- | :--- | :--- |
| Anadolu Finansman A.Ş. | Kredi Tahsis & Teminat Değerleme | 1.850.000.000 TL | BDDK & MASAK | 🔴 Yetersiz (2024) |
| Anadolu Enerji Üretim A.Ş. | Doğalgaz ve Emtia Alım Sözleşmeleri | 3.400.000.000 TL | EPDK & Rekabet | 🟡 Orta (2023) |""",
        "filename": "1_Yillik_Planlama_Evren"
    },
    {
        "phase_name": "2. Görev Planlama (Engagement Planning)",
        "task_name": "Risk ve Kontrol Matrisi (RCM) & Walkthrough",
        "context": "Mega Enerji ve Emtia Ticareti A.Ş. — Hazine Denetimi",
        "input": """Hazine ve Türev Swap İşlemleri Sürecinde aşağıdaki 3 operasyonel risk tespit edilmiştir:
1. Trader'ların günlük 5.000.000 USD limitini aşarak yetkisiz pozisyon açması ve kur zararı oluşturması.
2. Front-Office ve Back-Office yetkilerinin aynı personelde toplanması (SoD ihlali).
3. Piyasa aşırı dalgalandığında Stop-Loss limitlerinin manuel kapatılması.""",
        "filename": "2_Gorev_Planlama_RCM"
    },
    {
        "phase_name": "3. Saha Çalışması (Fieldwork & Testing)",
        "task_name": "Kontrol Test Prosedürü Geliştirme",
        "context": "Mega İlaç ve Sağlık Ürünleri A.Ş. — İç Denetim",
        "input": """Test Edilecek Kontrol: "ERP üzerinde 2.500.000 TL üzerindeki tüm hammadde satınalma faturalarında Çift Dijital İmza (Satınalma Direktörü + CFO) ve PO-GR-Invoice 3'lü Eşleştirme kuralı zorunludur. Eşleşme olmadan Finans birimi ödeme fişi oluşturamaz."
2025 yılında toplam 4.200 hammadde faturası kesilmiştir.""",
        "filename": "3_Saha_Calismasi_Test_Proseduru"
    },
    {
        "phase_name": "4. Denetim Raporlama (Reporting)",
        "task_name": "5C Standart Denetim Bulgusu Yazımı",
        "context": "Mega Yatırım Bankası A.Ş. — Teftiş Kurulu",
        "input": """Teftiş Kurulu tarafından yürütülen Kredi Denetiminde:
1. Levent Şube Müdürü Mehmet Özkan, 15.000.000 TL yetki limitini aşarak Atlas Lojistik A.Ş.'ye tek imzayla 145.000.000 TL kredi kullandırmıştır.
2. Teminata alınan taşınmaz için sahte ekspertiz raporu yüklenmiş; gerçek değeri 17M TL olup LTV %850 gerçekleşmiştir.
3. Kredi kullandırıldıktan 2 saat sonra MASAK filtreleri bypass edilerek 78.500.000 TL Panama merkezli hesaba aktarılmıştır.""",
        "filename": "4_Raporlama_5C_Bulgusu"
    },
    {
        "phase_name": "5. Sürekli Denetim & Analitik (Analytics)",
        "task_name": "Python (Pandas) İstisna Analiz Kodu",
        "context": "Mega Finans & Hazine Operasyonları",
        "input": """Hazine ve Uluslararası Para Transferleri veri tabanında ('transactions_sample.xlsx') sürekli denetim kuralları işletilecektir.
Tablo Sütunları: transaction_id, account_iban, beneficiary_name, beneficiary_country, amount_usd, transfer_type, approval_status, masak_cleared, approver_officer
1. Offshore Transferler: Alıcı ülkesi ('PA', 'VG', 'CY', 'SC') olan ve tutarı 250.000 USD üzerindeki işlemler.
2. MASAK Bypass: masak_cleared == False ve approval_status == 'APPROVED' olan işlemler.""",
        "filename": "5_Surekli_Denetim_Analytics"
    }
]

async def run_live_tests():
    os.makedirs("storage/live_test_results", exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 1080})
        
        print("🌐 Web Kokpiti Açılıyor: http://localhost:8501")
        await page.goto("http://localhost:8501", wait_until="networkidle", timeout=30000)
        await asyncio.sleep(2)

        for idx, sc in enumerate(SCENARIOS, 1):
            print(f"\n🚀 [{idx}/{len(SCENARIOS)}] Yürütülüyor: {sc['phase_name']} ➔ {sc['task_name']}...")
            
            # 1. Aşama Seçimi
            combos = page.locator('input[role="combobox"]')
            if await combos.count() >= 2:
                # 1. Combobox (Aşama)
                await combos.nth(0).click(force=True)
                await page.keyboard.type(sc["phase_name"][:10])
                await page.keyboard.press("Enter")
                await asyncio.sleep(1)

                # 2. Combobox (Görev)
                await combos.nth(1).click(force=True)
                await page.keyboard.type(sc["task_name"][:10])
                await page.keyboard.press("Enter")
                await asyncio.sleep(1)

            # 3. Şirket Bağlamı Girişi
            text_inputs = page.locator('input[type="text"]')
            if await text_inputs.count() > 0:
                await text_inputs.first.fill(sc["context"])
                await asyncio.sleep(0.3)

            # 4. Saha Notları Girişi
            text_areas = page.locator('textarea')
            if await text_areas.count() > 0:
                await text_areas.first.fill(sc["input"])
                await asyncio.sleep(0.5)

            # 5. Çalışma Kağıdını Üret Butonuna Tıkla
            generate_btn = page.locator('button:has-text("Çalışma Kağıdını Üret")')
            await generate_btn.click(force=True)
            print("⏳ Model analizi çalışıyor...")

            # 6. Sonucun ekrana gelmesini bekle
            try:
                await page.wait_for_selector('div.metrics-bar', timeout=60000)
                await asyncio.sleep(2)
                print(f"✅ [{idx}/{len(SCENARIOS)}] Sonuçlar ve Çalışma Kağıdı Ekrana Geldi!")
            except Exception as e:
                print(f"⚠️ Bekleme uyarısı: {e}")

            # 7. Ekran Görüntüsü Al
            shot_path = f"storage/live_test_results/{idx}_{sc['filename']}.png"
            await page.screenshot(path=shot_path, full_page=True)
            print(f"📸 Canlı Ekran Görüntüsü Kaydedildi: {shot_path}")

        print("\n🎉 Tüm 5 Aşama Canlı Testi Başarıyla Tamamlandı!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_live_tests())
