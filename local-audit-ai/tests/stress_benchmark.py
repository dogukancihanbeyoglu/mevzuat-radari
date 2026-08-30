"""
Local Audit AI - Stres ve Kapsamlı Doğrulama Test Koşucusu (Stress & Benchmark Runner)
5 Aşamalı Denetim Yaşam Döngüsündeki 10 Görevin Tamamını Zorlu ve Kompleks Senaryolarla Test Eder.
"""
import os
import sys
import time
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules import AuditOrchestrator

orchestrator = AuditOrchestrator()
sample_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../sample_test_files/massive_test_suite"))
enterprise_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../sample_test_files/enterprise_audit_pack"))

# 10 Görev x Çeşitli Karmaşıklık Senaryoları
BENCHMARK_SCENARIOS = [
    # 1. Yıllık Planlama
    {
        "id": "TC-01-UNIVERSE-COMPLEX",
        "phase": "1. Yıllık Planlama",
        "task": "audit_universe",
        "file": os.path.join(enterprise_dir, "holding_yillik_denetim_evreni_ve_yetkinlik_matrisi.xlsx"),
        "notes": "25 ana süreç ve 8 iştirakin finansal ve regülatif risklerini ağırlıklandırarak 2026 denetim evrenini önceliklendir.",
        "expected_keywords": ["DENETİM EVRENİ", "Doğal Risk", "Öncelik"]
    },
    {
        "id": "TC-02-RESOURCE-COMPETENCY",
        "phase": "1. Yıllık Planlama",
        "task": "resource_competency_mapping",
        "file": os.path.join(enterprise_dir, "holding_yillik_denetim_evreni_ve_yetkinlik_matrisi.xlsx"),
        "notes": "12 kişilik denetim ekibinin yetkinlik matrisini inceleyerek dış kaynak (co-sourcing) ihtiyacı olan projeleri belirle.",
        "expected_keywords": ["YETKİNLİK PLANI", "Dış Kaynak", "Eğitim"]
    },

    # 2. Görev Planlama
    {
        "id": "TC-03-RCM-HAZINE",
        "phase": "2. Görev Planlama",
        "task": "rcm_generation",
        "file": os.path.join(sample_dir, "hazine_ve_turev_islemler_proseduru.docx"),
        "notes": "Hazine, türev ürünler ve 2 milyon USD limit aşımı zayıflığını (W1) içeren detaylı RCM ve 10 mülakat sorusu oluştur.",
        "expected_keywords": ["RİSK VE KONTROL MATRİSİ", "W1", "Walkthrough"]
    },
    {
        "id": "TC-04-SCOPING-SUPPLY-CHAIN",
        "phase": "2. Görev Planlama",
        "task": "scoping_document",
        "file": os.path.join(enterprise_dir, "kuresel_tedarik_zinciri_ve_stok_proseduru_kompleks.docx"),
        "notes": "8.4 milyon TL stok açığı, konsinye stok ve ihale süreçlerini kapsayan resmi denetim kapsam dokümanı hazırla.",
        "expected_keywords": ["KAPSAM DOKÜMANI", "Kapsam İçi", "Zaman Planı"]
    },

    # 3. Saha Çalışması
    {
        "id": "TC-05-TEST-PROCEDURE-PAM",
        "phase": "3. Saha Çalışması",
        "task": "test_procedure",
        "file": os.path.join(sample_dir, "siber_guvenlik_ve_pam_erisim_loglari.xlsx"),
        "notes": "Root hesaplar ve mesai dışı MFA'sız erişimler için 4 ögeli (Amaç, Test Türü, Kanıt, Örneklem) test prosedürü yaz.",
        "expected_keywords": ["TEST PROGRAMI", "Denetim Amacı", "Örneklem"]
    },
    {
        "id": "TC-06-CONTROL-ANALYSIS-DEFICIENCY",
        "phase": "3. Saha Çalışması",
        "task": "control_analysis",
        "file": None,
        "notes": "Kontrol: 'Acil durumlarda Hazine Uzmanı sözlü talimatla 2.000.000 USD tutarında döviz işlemi yapabilir ve teyit mektupları ertesi gün sisteme girilir.' Bu kontrol tanımındaki tasarım eksikliklerini ve muğlak ifadeleri analiz et.",
        "expected_keywords": ["Tasarım Eksiklikleri", "Muğlak", "Önerilen"]
    },
    {
        "id": "TC-07-DATA-EXTRACTION-INVOICES",
        "phase": "3. Saha Çalışması",
        "task": "data_extraction",
        "file": None,
        "notes": "Fatura 1: No: INV-9901, Tarih: 12.06.2026, Satıcı: Alpha Lojistik Ltd, Tutar: 450.000 TL KDV dahil. Fatura 2: No: FAT-8812, Tarih: 14.06.2026, Satıcı: Beta Danışmanlık A.Ş., Tutar: 125.000 EUR net.",
        "expected_keywords": ["İŞLEM LİSTESİ", "Fatura No", "Net"]
    },

    # 4. Denetim Raporlama
    {
        "id": "TC-08-FINDING-5C-FRAUD",
        "phase": "4. Denetim Raporlama",
        "task": "finding_5c",
        "file": os.path.join(sample_dir, "adli_sorusturma_mulakat_tutanaklari_ham.txt"),
        "notes": "Fabrika Müdürünün 8.4 Milyon TL stok açığını usulsüz kapatması ve 3.2 Milyon TL hurda malzemenin gayriresmi satışına dair adli teftiş bulgusu yaz.",
        "expected_keywords": ["Condition", "Criteria", "Cause", "Effect", "Recommendation"]
    },
    {
        "id": "TC-09-EXECUTIVE-SUMMARY-C-LEVEL",
        "phase": "4. Denetim Raporlama",
        "task": "executive_summary",
        "file": None,
        "notes": "Mega Holding 2026 Hazine ve Siber Güvenlik Denetimi tamamlandı. 3 kritik bulgu: Yetkisiz döviz alımı, MFA'sız root erişimleri, 8.4M TL stok açığı. Yönetim 90 gün taahhüt verdi.",
        "expected_keywords": ["YÖNETİCİ ÖZETİ", "Gösterge Paneli", "Needs Improvement"]
    },

    # 5. Sürekli Denetim & Veri Analitiği
    {
        "id": "TC-10-ANALYTICS-500-ROWS",
        "phase": "5. Sürekli Denetim",
        "task": "data_analytics",
        "file": os.path.join(enterprise_dir, "sap_ap_islemleri_500_satir_kompleks.xlsx"),
        "notes": "500 satırlık veride mükerrer ödeme, SoD çakışması, offshore ülkeler (VG, CY), hafta sonu işlemleri ve parçalı split ödemeleri bulan çok sekmeli Python kodu üret.",
        "expected_keywords": ["import pandas", "ExcelWriter", "subset", "created_by"]
    }
]

def run_stress_benchmark():
    print("=" * 80)
    print("🚀 LOCAL AUDIT AI — 10 GÖREV x ÇOKLU FORMAT KAPSAMLI STRES TESTİ BAŞLATILIYOR")
    print("=" * 80)

    results = []
    start_all = time.time()

    for idx, tc in enumerate(BENCHMARK_SCENARIOS, 1):
        print(f"\n[{idx}/10] TEST EDİLİYOR: {tc['id']} ({tc['task']})")
        print(f"     Aşama: {tc['phase']}")
        print(f"     Dosya: {os.path.basename(tc['file']) if tc['file'] else 'Metin Girdisi'}")

        t0 = time.time()
        try:
            res = orchestrator.run_audit_task(
                module_name=tc['task'],
                input_text=tc['notes'],
                file_path=tc['file'],
                custom_context="Mega Holding A.Ş. — 2026 Kurumsal İç Denetimi"
            )
            elapsed = round(time.time() - t0, 2)
            content = res['output_content']

            # Doğrulama Kriterleri
            missing_keywords = [kw for kw in tc['expected_keywords'] if kw.lower() not in content.lower()]
            has_audit_trail = os.path.exists(res['audit_trail_file'])
            is_valid_structure = len(missing_keywords) == 0

            status = "PASSED" if is_valid_structure and has_audit_trail else "WARNING"

            results.append({
                "id": tc['id'],
                "task": tc['task'],
                "status": status,
                "duration_sec": elapsed,
                "model_used": res['dispatched_model']['model_name'],
                "tier": res['dispatched_model']['tier'],
                "missing_keywords": missing_keywords,
                "audit_trail_id": res['audit_trail_id']
            })

            print(f"     Sonuç: {status} ({elapsed}s) | Model: {res['dispatched_model']['model_name']} | Trail: {res['audit_trail_id']}")
            if missing_keywords:
                print(f"     ⚠️ Eksik Anahtar Kelimeler: {missing_keywords}")

        except Exception as e:
            elapsed = round(time.time() - t0, 2)
            print(f"     ❌ HATA: {str(e)} ({elapsed}s)")
            results.append({
                "id": tc['id'],
                "task": tc['task'],
                "status": "FAILED",
                "duration_sec": elapsed,
                "error": str(e)
            })

    total_time = round(time.time() - start_all, 2)
    print("\n" + "=" * 80)
    print(f"🏁 STRES TESTİ VE KIYASLAMA RAPORU (Toplam Süre: {total_time}s)")
    print("=" * 80)

    passed_count = sum(1 for r in results if r['status'] == 'PASSED')
    print(f"Toplam Test: {len(results)} | Başarılı: {passed_count} | Uç/Uyarı: {len(results) - passed_count}")

    for r in results:
        badge = "✅" if r['status'] == "PASSED" else "⚠️" if r['status'] == "WARNING" else "❌"
        print(f"{badge} {r['id']:<28} | {r['task']:<28} | {r.get('status')} ({r.get('duration_sec')}s)")

    return results

if __name__ == "__main__":
    run_stress_benchmark()
