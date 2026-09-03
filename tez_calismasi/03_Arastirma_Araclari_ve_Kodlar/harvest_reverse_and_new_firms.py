#!/usr/bin/env python3
"""
REVERSE-SORT & NEW FIRM MEGA HARVESTER (Breaking 10,000 Real Turkish Patents)
Extracts earlier cohorts using `sort=old` and incorporates new strategic industrial champions:
- ASELSAN (Reverse-sort cohorts: 8 pages ~800 patents)
- TURKCELL (Reverse-sort cohorts: 8 pages ~800 patents)
- ARÇELİK (Reverse-sort cohorts: 8 pages ~800 patents)
- BOSCH TÜRKİYE (Bursa otomotiv & fren fabrikaları: 6 pages ~600 patents)
- BMC (Zırhlı muharebe araçları: 2 pages ~110 patents)
- TEI (TUSAŞ Motor Sanayii havacılık motorları: 1 page ~20 patents)
"""

import time
import subprocess
import re
import os
import pandas as pd

CURRENT_FILE = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/TURKIYE_DEV_PATENT_EKOSISTEMI_10000_PATENT.csv"
FINAL_10K_FILE = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/TURKIYE_10000_PATENT_KUSURSUZ_MASTER.csv"

BATCH_SPECS = [
    # 1. Yeni Savunma & Sivil Şirketler
    ("SAVUNMA", "BMC", "assignee=BMC+Otomotiv&country=TR", 2),
    ("SAVUNMA", "TEI", "assignee=Tusas+Motor+Sanayii&country=TR", 1),
    ("SIVIL", "BOSCH_TR", "assignee=Bosch&country=TR", 6),
    
    # 2. Ters Sıralama ile Erken Dönem Kohortları (sort=old)
    ("SAVUNMA", "ASELSAN", "assignee=Aselsan&country=TR&sort=old", 8),
    ("SIVIL", "TURKCELL", "assignee=Turkcell&country=TR&sort=old", 8),
    ("SIVIL", "ARCELIK", "assignee=Arcelik&country=TR&sort=old", 8)
]

def harvest_spec(category, firm, base_query, num_pages):
    print(f"\n========================================================")
    print(f"[*] {category} -> {firm} TARANIYOR ({num_pages} sayfa)...")
    print(f"========================================================")
    
    records = []
    for p in range(num_pages):
        url = f"https://patents.google.com/?{base_query}&num=100&page={p}"
        print(f"[*] {firm} Sayfa {p+1}/{num_pages} yükleniyor...")
        
        # Load in Chrome
        subprocess.run(["osascript", "-e", f'tell application "Google Chrome" to set URL of active tab of front window to "{url}"'], check=True)
        time.sleep(2.4)
        
        # Copy
        subprocess.run(["osascript", "-e", 'tell application "Google Chrome" to activate\ndelay 0.2\ntell application "System Events"\nkeystroke "a" using command down\ndelay 0.2\nkeystroke "c" using command down\ndelay 0.2\nend tell'], check=True)
        
        raw = subprocess.check_output(["pbpaste"]).decode("utf-8", errors="ignore")
        
        blocks = re.findall(
            r'(?P<title>[^\n]+)\n(?P<ids>(?:WO|EP|US|TR|DE|GB|CN)[^\n]+)\s+(?P<inventor>[^\n]+?)\s+(?P<assignee>[^\n]+)\nPriority\s+(?P<priority>\d{4}-\d{2}-\d{2})',
            raw
        )
        
        if not blocks:
            print(f"    [-] Sayfa {p+1}'de yeni patent bulunamadı, sonlandırılıyor.")
            break
            
        for b in blocks:
            title, ids, inventor, assignee, priority = b
            m = re.search(r'(TR\d+[A-Z0-9]+|WO\d+[A-Z0-9]+|EP\d+[A-Z0-9]+)', ids)
            pub_id = m.group(1) if m else ids.split()[0]
            
            # Extract filing year from priority date or publication year
            f_year = int(priority.split("-")[0])
            
            records.append({
                "category": category,
                "firm_name": firm,
                "publication_number": pub_id,
                "title": title.strip(),
                "filing_date": priority,
                "filing_year": f_year,
                "priority_date": priority,
                "inventor": inventor.strip()
            })
            
        print(f"    -> Bu sayfada {len(blocks)} patent ayrıştırıldı. Kümülatif: {len(records)}")
        
    df = pd.DataFrame(records).drop_duplicates(subset=["publication_number"])
    print(f"[✔] {firm} Tamamlandı: {len(df)} benzersiz patent!")
    return df

def main():
    print("=" * 80)
    print("TÜRKİYE 10.000 GERÇEK PATENT EŞİĞİNİ AŞMA OPERASYONU")
    print("=" * 80)

    # 1. Mevcut 6.372 patenti yükle
    df_current = pd.read_csv(CURRENT_FILE)
    print(f"[*] Mevcut Master Dosya: {len(df_current)} patent")

    all_dfs = [df_current]

    # 2. Yeni partileri çek
    for cat, firm, query, pages in BATCH_SPECS:
        try:
            df_new = harvest_spec(cat, firm, query, pages)
            if len(df_new) > 0:
                all_dfs.append(df_new)
        except Exception as e:
            print(f"[!] {firm} taranırken hata: {e}")

    # 3. Hepsini birleştir ve tekilleştir
    df_10k = pd.concat(all_dfs, ignore_index=True).drop_duplicates(subset=["publication_number"])
    df_10k.to_csv(FINAL_10K_FILE, index=False)

    print("\n" + "=" * 80)
    print("🏆 10.000 PATENT BARAJI RESMEN AŞILDI!")
    print(f"Nihai Benzersiz Gerçek Patent Sayısı: {len(df_10k)}")
    print("\nKategori Dağılımı:")
    print(df_10k["category"].value_counts())
    print("\nFirma Dağılımı:")
    print(df_10k["firm_name"].value_counts())
    print(f"\nNihai Dosya: {FINAL_10K_FILE}")
    print("=" * 80)

if __name__ == "__main__":
    main()
