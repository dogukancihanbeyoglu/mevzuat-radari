#!/usr/bin/env python3
"""
MASSIVE EXPANSION HARVESTER (Reaching ~10,000 Real Turkish Patents)
Expands the patent dataset across key high-tech Turkish industries:
- TÜRK TELEKOM (Telekom / 5G / Ağ Altyapısı)
- OTOKAR (Otomotiv & Ağır Ticari / Zırhlı Taşıtlar)
- KORDSA (İleri Kompozit & Malzeme Teknolojileri)
- ŞİŞECAM (İleri Malzeme & Cam Teknolojileri)
- TÜBİTAK (SAGE, BİLGEM Savunma Araştırma Enstitüleri)
- TURKCELL (Kalan 10 Sayfa: +1,000 Patent)
- ARÇELİK (Kalan 10 Sayfa: +1,000 Patent)
"""

import time
import subprocess
import re
import os
import pandas as pd

EXISTING_MASTER = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/TURKIYE_SAVUNMA_VE_SIVIL_DEV_PATENT_VERISI_MASTER.csv"
EXPANDED_MASTER = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/TURKIYE_DEV_PATENT_EKOSISTEMI_10000_PATENT.csv"

# Targets: (Category, FirmName, QueryParam, StartPage, MaxPages)
EXPANSION_TARGETS = [
    # 1. Yeni Sivil ve Çift Kullanımlı Devler
    ("SIVIL", "TURK_TELEKOM", "Turk+Telekomunikasyon", 0, 8),      # ~800 patent
    ("SIVIL", "OTOKAR", "Otokar+Otomotiv", 0, 5),                  # ~500 patent
    ("SIVIL", "KORDSA", "Kordsa+Teknik+Tekstil", 0, 5),            # ~500 patent
    ("SIVIL", "SISECAM", "Turkiye+Sise+ve+Cam", 0, 5),             # ~500 patent
    
    # 2. Savunma Araştırma Enstitüleri
    ("SAVUNMA", "TUBITAK", "Turkiye+Bilimsel+ve+Teknolojik+Arastirma+Kurumu", 0, 6), # ~600 patent
    
    # 3. Kalan Derin Sayfalar (Turkcell ve Arçelik)
    ("SIVIL", "TURKCELL", "Turkcell", 10, 8),                      # +800 patent
    ("SIVIL", "ARCELIK", "Arcelik", 10, 8)                         # +800 patent
]

def harvest_batch(category, firm, query, start_page, num_pages):
    print(f"\n========================================================")
    print(f"[*] {category} -> {firm} TARANIYOR (Sayfa {start_page+1} - {start_page+num_pages})...")
    print(f"========================================================")
    
    records = []
    for p in range(start_page, start_page + num_pages):
        url = f"https://patents.google.com/?assignee={query}&country=TR&num=100&page={p}"
        print(f"[*] {firm} Sayfa {p+1} taranıyor...")
        
        # Load in Chrome
        subprocess.run(["osascript", "-e", f'tell application "Google Chrome" to set URL of active tab of front window to "{url}"'], check=True)
        time.sleep(2.4)
        
        # Copy
        subprocess.run(["osascript", "-e", 'tell application "Google Chrome" to activate\ndelay 0.2\ntell application "System Events"\nkeystroke "a" using command down\ndelay 0.2\nkeystroke "c" using command down\ndelay 0.2\nend tell'], check=True)
        
        raw = subprocess.check_output(["pbpaste"]).decode("utf-8", errors="ignore")
        
        blocks = re.findall(
            r'(?P<title>[^\n]+)\n(?P<ids>(?:WO|EP|US|TR|DE|GB|CN)[^\n]+)\s+(?P<inventor>[^\n]+?)\s+(?P<assignee>[^\n]+)\nPriority\s+(?P<priority>\d{4}-\d{2}-\d{2})\s+•\s+Filed\s+(?P<filed>\d{4}-\d{2}-\d{2})',
            raw
        )
        
        if not blocks:
            print(f"    [-] Sayfa {p+1}'de yeni patent bulunamadı, sonlandırılıyor.")
            break
            
        for b in blocks:
            title, ids, inventor, assignee, priority, filed = b
            m = re.search(r'(TR\d+[A-Z0-9]+|WO\d+[A-Z0-9]+|EP\d+[A-Z0-9]+)', ids)
            pub_id = m.group(1) if m else ids.split()[0]
            records.append({
                "category": category,
                "firm_name": firm,
                "publication_number": pub_id,
                "title": title.strip(),
                "filing_date": filed,
                "filing_year": int(filed.split("-")[0]),
                "priority_date": priority,
                "inventor": inventor.strip()
            })
            
        print(f"    -> Bu sayfada {len(blocks)} patent ayrıştırıldı. Toplam: {len(records)}")
        
    df = pd.DataFrame(records).drop_duplicates(subset=["publication_number"])
    print(f"[✔] {firm} Batch Tamamlandı: {len(df)} benzersiz patent!")
    return df

def main():
    print("=" * 80)
    print("TÜRKİYE DEV PATENT VERİ TABANI GENİŞLETME OPERASYONU (10.000 HEDEFİ)")
    print("=" * 80)

    # 1. Mevcut 5.348 patenti yükle
    df_existing = pd.read_csv(EXISTING_MASTER)
    print(f"[*] Mevcut Master Veri Tabanı Yüklendi: {len(df_existing)} patent")

    new_dfs = [df_existing]

    # 2. Yeni partileri çek
    for cat, firm, query, start_p, n_pages in EXPANSION_TARGETS:
        try:
            df_batch = harvest_batch(cat, firm, query, start_p, n_pages)
            if len(df_batch) > 0:
                new_dfs.append(df_batch)
        except Exception as e:
            print(f"[!] {firm} taranırken hata: {e}")

    # 3. Birleştir ve tekilleştir
    final_master = pd.concat(new_dfs, ignore_index=True).drop_duplicates(subset=["publication_number"])
    final_master.to_csv(EXPANDED_MASTER, index=False)

    print("\n" + "=" * 80)
    print("🏆 TÜRKİYE 10.000 PATENT DEV VERİ SETİ TAMAMLANDI!")
    print(f"Toplam Benzersiz Gerçek Patent Sayısı: {len(final_master)}")
    print("\nKategori Dağılımı:")
    print(final_master["category"].value_counts())
    print("\nFirma Dağılımı:")
    print(final_master["firm_name"].value_counts())
    print(f"\nNihai Dosya Konumu: {EXPANDED_MASTER}")
    print("=" * 80)

if __name__ == "__main__":
    main()
