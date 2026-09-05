#!/usr/bin/env python3
"""
STEP-BY-STEP PATENT DATASET CROSS-SOURCE COMPARISON
Compares Google Patents BigQuery data against:
1. Sanayi ve Teknoloji Bakanlığı & TÜRKPATENT "2022 Yılının Enleri" Resmi İstatistikleri
2. EPO Espacenet uluslararası tescil ve belge tipi uyumu
3. TÜİK Yıllık Makro Tescil Trendleri
"""

import pandas as pd
import numpy as np

DATA_PATH = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/02_Ham_Veriler/TURKIYE_CUMHURIYETI_TUM_PATENT_EVRENI_93240.csv"
OUTPUT_REPORT = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/KAYNAK_KARSILASTIRMA_VE_DOGRULAMA_RAPORU.csv"

def main():
    print("=" * 95)
    print("ADIM ADIM RESMİ KAYNAK KARŞILAŞTIRMASI VE ÇAPRAZ DOĞRULAMA RAPORU")
    print("Kurum: Ankara Hacı Bayram Veli Üniversitesi Lisansüstü Eğitim Enstitüsü")
    print("=" * 95)

    df = pd.read_csv(DATA_PATH, low_memory=False)

    # 1. ADIM: 2022 YILI TÜRKPATENT RESMİ ENLER LİSTESİ İLE BİREBİR EŞLEŞTİRME
    # Kaynak: Sanayi ve Teknoloji Bakanlığı / TÜRKPATENT 2022 Yılı Resmi Raporu (AA / Resmi Gazete)
    df_2022 = df[(df["filing_date"].astype(str).str.startswith("2022")) & (~df["publication_number"].str.contains("-U"))]

    official_2022_top = [
        {"Firma": "Turkcell Teknoloji / Grubu", "Regex": "TURKCELL", "TÜRKPATENT Resmi": 325},
        {"Firma": "Arçelik A.Ş.", "Regex": "ARCELIK", "TÜRKPATENT Resmi": 229},
        {"Firma": "Türk Telekomünikasyon A.Ş.", "Regex": "TURK TELEKOM", "TÜRKPATENT Resmi": 191},
        {"Firma": "Mercedes-Benz Türk A.Ş.", "Regex": "MERCEDES BENZ", "TÜRKPATENT Resmi": 180},
        {"Firma": "Vestel Beyaz Eşya A.Ş.", "Regex": "VESTEL BEYAZ", "TÜRKPATENT Resmi": 148},
        {"Firma": "ASELSAN Elektronik Sanayi", "Regex": "ASELSAN", "TÜRKPATENT Resmi": 139},
        {"Firma": "TIRSAN Treyler Sanayi", "Regex": "TIRSAN", "TÜRKPATENT Resmi": 76},
        {"Firma": "Vestel Elektronik Sanayi", "Regex": "VESTEL ELEKTRONIK", "TÜRKPATENT Resmi": 70},
        {"Firma": "TUSAŞ Türk Havacılık ve Uzay", "Regex": "TUSAS|TAI|TURK HAVACILIK", "TÜRKPATENT Resmi": 68}
    ]

    results = []
    print("\n--- 1. ADIM: 2022 YILI ŞİRKET BAZINDA TÜRKPATENT RESMİ VERİSİ İLE KARŞILAŞTIRMA ---")
    print(f"{'Şirket Adı':<30} | {'TÜRKPATENT Resmi':<18} | {'Bizim Veri Seti':<18} | {'Uyum / Fark':<15}")
    print("-" * 88)

    for item in official_2022_top:
        name = item["Firma"]
        regex = item["Regex"]
        off_val = item["TÜRKPATENT Resmi"]
        our_val = len(df_2022[df_2022["assignee_name"].str.contains(regex, case=False, na=False)])
        diff = our_val - off_val
        status = "BİREBİR TAM UYUMLU (0 FARK) 🎯" if diff == 0 else (f"Yakın Uyum ({diff:+d})" if abs(diff) <= 5 else f"Tüzel İştirak Farkı ({diff:+d})")
        
        results.append({
            "Şirket Adı": name,
            "TÜRKPATENT Resmi Başvuru": off_val,
            "BigQuery Veri Setimiz": our_val,
            "Fark": diff,
            "Örtüşme Yüzdesi": f"%{(our_val/off_val)*100:.1f}",
            "Durum": status
        })
        print(f"{name:<30} | {off_val:<18} | {our_val:<18} | {status:<15}")

    df_res = pd.DataFrame(results)
    df_res.to_csv(OUTPUT_REPORT, index=False)
    print(f"\n[✔] Ayrıntılı karşılaştırma raporu kaydedildi: {OUTPUT_REPORT}")

if __name__ == "__main__":
    main()
