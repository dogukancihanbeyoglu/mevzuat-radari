"""
Local Audit AI - Çoklu Dosyalı & Ultra Kompleks Stres Testi Koşucusu
Aynı anda birden fazla Word, Excel, CSV ve TXT dosyasını çapraz analiz ederek tüm 10 görevi test eder.
"""
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from modules import AuditOrchestrator

orchestrator = AuditOrchestrator()
massive_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../sample_test_files/massive_test_suite"))
enterprise_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../sample_test_files/enterprise_audit_pack"))

MULTI_FILE_SCENARIOS = [
    {
        "id": "ULTRA-01-UNIVERSE-MULTI",
        "task": "audit_universe",
        "files": [
            os.path.join(enterprise_dir, "holding_yillik_denetim_evreni_ve_yetkinlik_matrisi.xlsx"),
            os.path.join(massive_dir, "hazine_ve_turev_islemler_proseduru.docx")
        ],
        "notes": "Hem 25 süreçlik holding denetim evrenini hem de 14 iştirakin Hazine prosedürünü birleştirerek 2026 yılı önceliklendirilmiş denetim evrenini üret."
    },
    {
        "id": "ULTRA-02-RESOURCE-GAP-MULTI",
        "task": "resource_competency_mapping",
        "files": [
            os.path.join(enterprise_dir, "holding_yillik_denetim_evreni_ve_yetkinlik_matrisi.xlsx"),
            os.path.join(massive_dir, "siber_guvenlik_ve_pam_erisim_loglari.xlsx")
        ],
        "notes": "Siber güvenlik PAM logları ve kadro yetkinlik tablosunu çapraz analiz ederek DevOps denetimi için dış kaynak (co-sourcing) ihtiyacını rasyonalize et."
    },
    {
        "id": "ULTRA-03-RCM-CROSS-DOCX-XLSX",
        "task": "rcm_generation",
        "files": [
            os.path.join(enterprise_dir, "kuresel_tedarik_zinciri_ve_stok_proseduru_kompleks.docx"),
            os.path.join(enterprise_dir, "sap_ap_islemleri_500_satir_kompleks.xlsx")
        ],
        "notes": "Tedarik prosedüründeki 3'lü eşleştirme kuralları ile 500 satırlık SAP işlem tablosundaki limit aşımlarını eşleştirip uçtan uca RCM matrisi oluştur."
    },
    {
        "id": "ULTRA-04-SCOPING-MULTI-ASSET",
        "task": "scoping_document",
        "files": [
            os.path.join(massive_dir, "ik_yonetici_prim_ve_bordro_sureci.docx"),
            os.path.join(massive_dir, "mizan_ve_muhasebe_kayitlari_1000satir.xlsx")
        ],
        "notes": "12.5M TL İcra Kurulu avans primleri ve 1000 satırlık 770/360 mizan hesaplarını birleştiren resmi Denetim Kapsam Dokümanı hazırla."
    },
    {
        "id": "ULTRA-05-TEST-PROCEDURE-MULTI",
        "task": "test_procedure",
        "files": [
            os.path.join(massive_dir, "hazine_ve_turev_islemler_proseduru.docx"),
            os.path.join(massive_dir, "siber_guvenlik_ve_pam_erisim_loglari.xlsx")
        ],
        "notes": "Hazine 2M USD sözlü spot işlem açığı ve mesai dışı root erişimleri için 4 ögeli (Amaç, Test Türü, Kanıt, Örneklem) test prosedürü yaz."
    },
    {
        "id": "ULTRA-06-CONTROL-DEFICIENCY-COMPLEX",
        "task": "control_analysis",
        "files": [os.path.join(massive_dir, "hazine_ve_turev_islemler_proseduru.docx")],
        "notes": "Hazine prosedürü Madde 1 deki 'Piyasa oynaklığı durumunda Hazine Uzmanı sözlü talimatla 2.000.000 USD spot döviz alımı yapabilir ve teyit ertesi gün girilir' kuralının tasarım zafiyetini ve muğlak noktalarını derinlemesine incele."
    },
    {
        "id": "ULTRA-07-EXTRACTION-ECOMMERCE-CSV",
        "task": "data_extraction",
        "files": [os.path.join(massive_dir, "e_ticaret_siparis_ve_iade_anomalileri.csv")],
        "notes": "CSV tablosundaki YONETIM100 ve VIP50 indirim kodları kullanılan, chargeback ve iade yapılan şüpheli siparişleri ayıkla ve tabloya dök."
    },
    {
        "id": "ULTRA-08-FINDING-5C-CROSS-EVIDENCE",
        "task": "finding_5c",
        "files": [
            os.path.join(massive_dir, "adli_sorusturma_mulakat_tutanaklari_ham.txt"),
            os.path.join(enterprise_dir, "kuresel_tedarik_zinciri_ve_stok_proseduru_kompleks.docx")
        ],
        "notes": "Adli mülakat itirafları (Fabrika Müdürü ve Ambar Şefi) ile Tedarik Prosedürü Madde 5'teki hurda satış kurallarını çaprazlayarak Yönetim Kurulu için resmi 5C denetim bulgusu oluştur."
    },
    {
        "id": "ULTRA-09-EXECUTIVE-SUMMARY-MULTI",
        "task": "executive_summary",
        "files": [
            os.path.join(enterprise_dir, "kuresel_tedarik_zinciri_ve_stok_proseduru_kompleks.docx"),
            os.path.join(massive_dir, "hazine_ve_turev_islemler_proseduru.docx")
        ],
        "notes": "Hazine ve Tedarik Zinciri denetimlerinin birleşik sonuçlarını (8.4M TL stok açığı + 2M USD yetkisiz hazine limiti) sentezleyen gösterge panelli Denetim Komitesi Yönetici Özeti yaz."
    },
    {
        "id": "ULTRA-10-ANALYTICS-MULTI-DATASET",
        "task": "data_analytics",
        "files": [
            os.path.join(enterprise_dir, "sap_ap_islemleri_500_satir_kompleks.xlsx"),
            os.path.join(massive_dir, "e_ticaret_siparis_ve_iade_anomalileri.csv")
        ],
        "notes": "Hem 500 satırlık SAP ödeme loglarında (SoD, offshore, split fatura) hem de e-ticaret tablosunda anomali yakalayan çok sekmeli Python analiz betiği üret."
    }
]

def run_ultra_benchmark():
    print("=" * 85)
    print("🔥 LOCAL AUDIT AI — ÇOKLU DOSYALI & ULTRA KOMPLEKS BENCHMARK TESTİ BAŞLADI")
    print("=" * 85)

    start_all = time.time()
    for idx, sc in enumerate(MULTI_FILE_SCENARIOS, 1):
        print(f"\n[{idx}/10] KOŞULUYOR: {sc['id']} ({sc['task']})")
        print(f"     Yüklenen Dosya Sayısı: {len(sc['files'])}")
        for f in sc['files']:
            print(f"      📄 {os.path.basename(f)} ({round(os.path.getsize(f)/1024, 1)} KB)")

        t0 = time.time()
        try:
            res = orchestrator.run_audit_task(
                module_name=sc['task'],
                input_text=sc['notes'],
                file_paths=sc['files'],
                custom_context="Mega Holding A.Ş. — 2026 Kurumsal Çoklu Denetim"
            )
            elapsed = round(time.time() - t0, 2)
            print(f"     ✅ Başarılı ({elapsed}s) | Model: {res['dispatched_model']['model_name']} | Trail: {res['audit_trail_id']}")
        except Exception as e:
            elapsed = round(time.time() - t0, 2)
            print(f"     ❌ Hata: {str(e)} ({elapsed}s)")

    print("\n" + "=" * 85)
    print(f"🏁 TÜM ÇOKLU DOSYA BENCHMARK TESTLERİ TAMAMLANDI (Süre: {round(time.time()-start_all, 2)}s)")
    print("=" * 85)

if __name__ == "__main__":
    run_ultra_benchmark()
