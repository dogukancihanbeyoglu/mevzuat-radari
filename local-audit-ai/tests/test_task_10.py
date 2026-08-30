import asyncio
import json
import os
import time
from playwright.async_api import async_playwright

async def run_task_10():
    with open("storage/test_scenarios_library.json", "r", encoding="utf-8") as f:
        scenarios = json.load(f)
    sc = scenarios[9] # Task 10

    print(f"🚀 [10/10] TEST EDİLİYOR: {sc['phase_name']} ➔ {sc['task_name']}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=200)
        page = await browser.new_page(viewport={"width": 1440, "height": 950})
        await page.goto("http://localhost:8501", wait_until="networkidle")
        await asyncio.sleep(1.5)

        visible_selects = page.locator('div[data-testid="stSelectbox"]:visible')
        await visible_selects.nth(0).click()
        await asyncio.sleep(0.4)
        await page.locator('li[role="option"]').nth(sc["phase_idx"]).click()
        await asyncio.sleep(0.8)

        await visible_selects.nth(1).click()
        await asyncio.sleep(0.4)
        await page.locator('li[role="option"]').nth(sc["task_idx"]).click()
        await asyncio.sleep(0.8)

        ctx_input = page.locator('input[aria-label="Kurumsal Bağlam / Şirket Bilgisi:"]')
        if await ctx_input.count() > 0:
            await ctx_input.fill(sc["context"])

        notes_input = page.locator('textarea[aria-label="Saha Notları / Açıklama / Ham Veri:"]')
        if await notes_input.count() > 0:
            await notes_input.fill(sc["input_data"])

        gen_btn = page.locator('button:has-text("Çalışma Kağıdını Üret")')
        await gen_btn.click()
        print("⏳ Model analizi çalışıyor...")

        await page.wait_for_selector('div.metrics-bar', timeout=180000)
        print("✅ Çalışma Kağıdı Ekrana Geldi!")

        await page.evaluate("window.scrollBy(0, 480)")
        await asyncio.sleep(2)

        print("⚡ [SANDBOX] 'Kodu Sandbox\'ta Çalıştır' Tıklanıyor...")
        sandbox_btn = page.locator('button:has-text("Kodu Sandbox\'ta Çalıştır")')
        if await sandbox_btn.count() > 0:
            await sandbox_btn.click()
            await page.wait_for_selector('text=Python analitik kodu izole sandbox\'ta başarıyla çalıştırıldı', timeout=60000)
            print("🎉 Sandbox başarıyla çalıştı!")
            await asyncio.sleep(3)

        shot_file = f"storage/screenshots/task_10_{sc['task_key']}.png"
        await page.screenshot(path=shot_file, full_page=True)
        print(f"📸 10. Ekran Görüntüsü Kaydedildi: {shot_file}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_task_10())
