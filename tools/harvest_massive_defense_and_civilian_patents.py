#!/usr/bin/env python3
"""
MASSIVE REAL TURKISH PATENT HARVESTER (DEFENSE & CIVILIAN)
Automates Google Chrome to harvest thousands of genuine patent records from official registries:
Defense: ASELSAN, TUSAŞ, HAVELSAN, ROKETSAN, STM, BAYKAR, FNSS, MKE
Civilian: FORD OTOSAN, TOFAŞ, ARÇELİK, VESTEL, TURKCELL
"""

import time
import subprocess
import re
import os
import pandas as pd

OUTPUT_MASTER = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/TURKIYE_SAVUNMA_VE_SIVIL_DEV_PATENT_VERISI_MASTER.csv"

# Target specifications: (Category, FirmName, QueryParam, MaxPages)
TARGETS = [
    # --- SİVİL SANAYİ DEVLERİ ---
    ("SIVIL", "FORD_OTOSAN", "Ford+Otomotiv+Sanayi", 11),       # ~1,100 patent
    ("SIVIL", "TOFAS", "Tofas+Turk+Otomobil", 5),               # ~500 patent
    ("SIVIL", "ARCELIK", "Arcelik", 10),                        # ~1,000 patent
    ("SIVIL", "VESTEL", "Vestel+Elektronik", 10),               # ~1,000 patent
    ("SIVIL", "TURKCELL", "Turkcell", 10),                      # ~1,000 patent
    
    # --- SAVUNMA SANAYİİ EKOSİSTEMİ ---
    ("SAVUNMA", "FNSS", "FNSS+Savunma", 2),                     # Zırhlı Kara Araçları
    ("SAVUNMA", "MKE", "Makina+ve+Kimya+Endustrisi", 2)         # Mühimmat ve Ağır Silah
]

def harvest_target(category, firm, query, max_pages):
    print(f"\n========================================================")
    print(f"[*] {category} -> {firm} TARANIYOR (Hedef: {max_pages} sayfa)...")
    print(f"========================================================")
    
    recs = []
    for p in range(max_pages):
        url = f"https://patents.google.com/?assignee={query}&country=TR&num=100&page={p}"
        print(f"[*] {firm} Sayfa {p+1}/{max_pages} yükleniyor...")
        
        # Load URL in Chrome
        subprocess.run(["osascript", "-e", f'tell application "Google Chrome" to set URL of active tab of front window to "{url}"'], check=True)
        time.sleep(2.6)
        
        # Copy content
        subprocess.run(["osascript", "-e", 'tell application "Google Chrome" to activate\ndelay 0.2\ntell application "System Events"\nkeystroke "a" using command down\ndelay 0.2\nkeystroke "c" using command down\ndelay 0.2\nend tell'], check=True)
        
        raw = subprocess.check_output(["pbpaste"]).decode("utf-8", errors="ignore")
        
        # Regex to parse
        blocks = re.findall(
            r'(?P<title>[^\n]+)\n(?P<ids>(?:WO|EP|US|TR|DE|GB|CN)[^\n]+)\s+(?P<inventor>[^\n]+?)\s+(?P<assignee>[^\n]+)\nPriority\s+(?P<priority>\d{4}-\d{2}-\d{2})\s+•\s+Filed\s+(?P<filed>\d{4}-\d{2}-\d{2})',
            raw
        )
        
        if not blocks:
            print(f"    [-] Sayfa {p+1}'de yeni patent bulunamadı, bu firma tamamlandı.")
            break
            
        for b in blocks:
            title, ids, inventor, assignee, priority, filed = b
            m = re.search(r'(TR\d+[A-Z0-9]+|WO\d+[A-Z0-9]+|EP\d+[A-Z0-9]+)', ids)
            pub_id = m.group(1) if m else ids.split()[0]
            recs.append({
                "category": category,
                "firm_name": firm,
                "publication_number": pub_id,
                "title": title.strip(),
                "filing_date": filed,
                "filing_year": int(filed.split("-")[0]),
                "priority_date": priority,
                "inventor": inventor.strip()
            })
            
        print(f"    -> Bu sayfada {len(blocks)} patent ayrıştırıldı. Kümülatif: {len(recs)}")
        
    df = pd.DataFrame(recs).drop_duplicates(subset=["publication_number"])
    print(f"[✔] {firm} Tamamlandı: {len(df)} benzersiz patent!")
    return df

def main():
    print("=" * 80)
    print("TÜRKİYE BÜYÜK SAVUNMA VE SİVİL PATENT VERİ DERLEME MOTORU")
    print("=" * 80)

    # 1. Mevcut savunma havuzunu yükle (1.658 patent)
    existing_def_path = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/TURK_SAVUNMA_SANAYII_TUM_PATENTLERI_YUZDE_100.csv"
    df_existing_def = pd.read_csv(existing_def_path)
    df_existing_def["category"] = "SAVUNMA"

    all_dfs = [df_existing_def]

    # 2. Yeni sivil ve savunma hedeflerini tara
    for cat, firm, query, pages in TARGETS:
        try:
            df_res = harvest_target(cat, firm, query, pages)
            if len(df_res) > 0:
                all_dfs.append(df_res)
        except Exception as e:
            print(f"[!] {firm} taranırken hata: {e}")

    # 3. Hepsini birleştir ve tekilleştir
    master_df = pd.concat(all_dfs, ignore_index=True).drop_duplicates(subset=["publication_number"])
    
    # Masaüstüne kaydet
    master_df.to_csv(OUTPUT_MASTER, index=False)
    
    print("\n" + "=" * 80)
    print("🏆 TÜRKİYE SAVUNMA VE SİVİL DEV PATENT VERİ TABANI OLUŞTURULDU!")
    print(f"Toplam Benzersiz Gerçek Patent Sayısı: {len(master_df)}")
    print("\nKategori Dağılımı:")
    print(master_df["category"].value_counts())
    print("\nFirma Dağılımı:")
    print(master_df["firm_name"].value_counts())
    print(f"\nDosya Konumu: {OUTPUT_MASTER}")
    print("=" * 80)

if __name__ == "__main__":
    main()
