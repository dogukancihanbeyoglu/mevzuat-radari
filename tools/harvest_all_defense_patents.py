#!/usr/bin/env python3
"""
Full Defense Universe Harvester
Pulls 100% of all published Turkish defense patents:
- ASELSAN: 20 pages (~1,911 patents)
- HAVELSAN: 3 pages (~242 patents)
- ROKETSAN: 2 pages (~192 patents)
- TUSAŞ: already pulled (451 patents)
- STM & BAYKAR: already pulled
Merges everything into:
/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/TURK_SAVUNMA_SANAYII_TUM_PATENTLERI_YUZDE_100.csv
"""

import time
import subprocess
import re
import os
import pandas as pd

CSV_ALL = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/TURK_SAVUNMA_SANAYII_TUM_PATENTLERI_YUZDE_100.csv"

def harvest_firm_all_pages(firm_name, query_param, max_pages):
    print(f"\n==================================================")
    print(f"[*] {firm_name} İÇİN TÜM SAYFALAR TARANIYOR ({max_pages} Sayfa)...")
    print(f"==================================================")
    
    firm_records = []
    for page in range(max_pages):
        url = f"https://patents.google.com/?assignee={query_param}&country=TR&num=100&page={page}"
        print(f"[*] {firm_name} Sayfa {page+1}/{max_pages} yükleniyor...")
        
        # Load URL in Chrome
        subprocess.run(["osascript", "-e", f'tell application "Google Chrome" to set URL of active tab of front window to "{url}"'], check=True)
        time.sleep(3.0)
        
        # Copy page content
        subprocess.run(["osascript", "-e", 'tell application "Google Chrome" to activate\ndelay 0.2\ntell application "System Events"\nkeystroke "a" using command down\ndelay 0.2\nkeystroke "c" using command down\ndelay 0.2\nend tell'], check=True)
        
        raw_text = subprocess.check_output(["pbpaste"]).decode("utf-8", errors="ignore")
        
        # Regex to parse blocks
        pat_blocks = re.findall(
            r'(?P<title>[^\n]+)\n(?P<ids>(?:WO|EP|US|TR|DE|GB|CN)[^\n]+)\s+(?P<inventor>[^\n]+?)\s+(?P<assignee>[^\n]+)\nPriority\s+(?P<priority>\d{4}-\d{2}-\d{2})\s+•\s+Filed\s+(?P<filed>\d{4}-\d{2}-\d{2})',
            raw_text
        )
        
        if not pat_blocks:
            print(f"    [-] Sayfa {page+1}'de yeni patent bulunamadı, döngü sonlandırılıyor.")
            break
            
        page_count = 0
        for b in pat_blocks:
            title, ids, inventor, assignee, priority, filed = b
            m = re.search(r'(TR\d+[A-Z0-9]+|WO\d+[A-Z0-9]+|EP\d+[A-Z0-9]+)', ids)
            pub_id = m.group(1) if m else ids.split()[0]
            firm_records.append({
                "firm_name": firm_name,
                "publication_number": pub_id,
                "title": title.strip(),
                "filing_date": filed,
                "filing_year": int(filed.split("-")[0]),
                "priority_date": priority,
                "inventor": inventor.strip()
            })
            page_count += 1
            
        print(f"    -> {page_count} patent ayrıştırıldı. Kümülatif: {len(firm_records)}")
        
    df_firm = pd.DataFrame(firm_records).drop_duplicates(subset=["publication_number"])
    print(f"[✔] {firm_name} Tamamlandı: {len(df_firm)} benzersiz patent!")
    return df_firm

def main():
    # 1. Start with existing TUSAŞ, STM, BAYKAR
    existing_file = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/GERCEK_HAM_PATENTLER_LISTESI.csv"
    existing_df = pd.read_csv(existing_file)
    base_df = existing_df[existing_df["firm_name"].isin(["TUSAS", "STM", "BAYKAR"])].copy()
    
    # 2. Harvest remaining: ROKETSAN (2 pages) and HAVELSAN (3 pages) and ASELSAN (20 pages)
    df_roketsan = harvest_firm_all_pages("ROKETSAN", "Roketsan", max_pages=2)
    df_havelsan = harvest_firm_all_pages("HAVELSAN", "Havelsan", max_pages=3)
    df_aselsan = harvest_firm_all_pages("ASELSAN", "Aselsan", max_pages=20)
    
    # 3. Combine All
    all_dfs = [base_df[["firm_name", "publication_number", "title", "filing_date", "filing_year", "inventor"]],
               df_roketsan[["firm_name", "publication_number", "title", "filing_date", "filing_year", "inventor"]],
               df_havelsan[["firm_name", "publication_number", "title", "filing_date", "filing_year", "inventor"]],
               df_aselsan[["firm_name", "publication_number", "title", "filing_date", "filing_year", "inventor"]]]
               
    df_final = pd.concat(all_dfs, ignore_index=True).drop_duplicates(subset=["publication_number"])
    df_final.to_csv(CSV_ALL, index=False)
    
    print("\n" + "=" * 80)
    print("🏆 TÜRKİYE SAVUNMA SANAYİİ RESMİ PATENT EVRENİ %100 DERLENDİ!")
    print(f"Toplam Tescilli Savunma Patenti: {len(df_final)}")
    print(df_final["firm_name"].value_counts())
    print(f"Kaydedilen Dosya: {CSV_ALL}")
    print("=" * 80)

if __name__ == "__main__":
    main()
