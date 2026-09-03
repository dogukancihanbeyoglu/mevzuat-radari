#!/usr/bin/env python3
"""
Chrome Automation Patent Harvester
Bypasses web scraping blocks by leveraging local Google Chrome to load
Google Patents pages, dump genuine patent records directly from rendered DOM,
and extract real publication numbers, dates, titles, and assignees.
"""

import time
import subprocess
import re
import pandas as pd

TARGET_FIRMS = [
    ("ASELSAN", "https://patents.google.com/?assignee=Aselsan&country=TR&num=100"),
    ("TUSAS", "https://patents.google.com/?assignee=TUSAS&country=TR&num=100"),
    ("ROKETSAN", "https://patents.google.com/?assignee=Roketsan&country=TR&num=100"),
    ("HAVELSAN", "https://patents.google.com/?assignee=Havelsan&country=TR&num=100"),
    ("STM", "https://patents.google.com/?assignee=Savunma+Teknolojileri+Muhendislik&country=TR&num=100"),
    ("BAYKAR", "https://patents.google.com/?assignee=Baykar&country=TR&num=100"),
    ("FORD_OTOSAN", "https://patents.google.com/?assignee=Ford+Otomotiv+Sanayi&country=TR&num=100"),
    ("TURKCELL", "https://patents.google.com/?assignee=Turkcell&country=TR&num=100"),
    ("ARCELIK", "https://patents.google.com/?assignee=Arcelik&country=TR&num=100")
]

def harvest_firm(firm_name, url):
    print(f"[*] {firm_name} için patentler taranıyor: {url}")
    # Tell Chrome to load URL
    apple_script_load = f'''
    tell application "Google Chrome"
        set URL of active tab of front window to "{url}"
    end tell
    '''
    subprocess.run(["osascript", "-e", apple_script_load], check=True)
    time.sleep(3.5) # Allow DOM to render completely

    # Select all and copy
    apple_script_copy = '''
    tell application "Google Chrome" to activate
    delay 0.3
    tell application "System Events"
        keystroke "a" using command down
        delay 0.2
        keystroke "c" using command down
        delay 0.2
    end tell
    '''
    subprocess.run(["osascript", "-e", apple_script_copy], check=True)
    time.sleep(0.5)

    raw_text = subprocess.check_output(["pbpaste"]).decode("utf-8", errors="ignore")
    
    # Regex parser for Google Patents result card
    lines = raw_text.split("\n")
    records = []
    
    # Extract TR publication numbers and dates
    pat_blocks = re.findall(
        r'(?P<title>[^\n]+)\n(?P<ids>(?:WO|EP|US|TR|DE|GB|CN)[^\n]+)\s+(?P<inventor>[^\n]+?)\s+(?P<assignee>[^\n]+)\nPriority\s+(?P<priority>\d{4}-\d{2}-\d{2})\s+•\s+Filed\s+(?P<filed>\d{4}-\d{2}-\d{2})\s+•\s+Published\s+(?P<published>\d{4}-\d{2}-\d{2})',
        raw_text
    )

    for item in pat_blocks:
        title, ids, inventor, assignee, priority, filed, published = item
        # Extract the TR or WO publication ID
        tr_id_match = re.search(r'(TR\d+[A-Z0-9]+|WO\d+[A-Z0-9]+|EP\d+[A-Z0-9]+)', ids)
        pub_id = tr_id_match.group(1) if tr_id_match else ids.split()[0]
        
        records.append({
            "firm_category": "SAVUNMA" if firm_name in ["ASELSAN", "TUSAS", "ROKETSAN", "HAVELSAN", "STM", "BAYKAR"] else "SIVIL",
            "firm_name": firm_name,
            "publication_number": pub_id,
            "title": title.strip(),
            "filing_date": filed,
            "filing_year": int(filed.split("-")[0]),
            "publication_date": published,
            "priority_date": priority,
            "inventor": inventor.strip(),
            "assignee_raw": assignee.strip()
        })
        
    print(f"[+] {firm_name}: {len(records)} adet gerçek patent başarıyla çekildi ve ayrıştırıldı.")
    return records

def main():
    print("=" * 80)
    print("GOOGLE CHROME OTOMASYONUYLA GERÇEK PATENT VERİSİ DERLEME MOTORU")
    print("=" * 80)

    all_patents = []
    for firm, url in TARGET_FIRMS:
        try:
            recs = harvest_firm(firm, url)
            all_patents.extend(recs)
        except Exception as e:
            print(f"[!] {firm} taranırken hata: {e}")

    df = pd.DataFrame(all_patents)
    output_path = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/GERCEK_HAM_PATENTLER_LISTESI.csv"
    df.to_csv(output_path, index=False)
    print("=" * 80)
    print(f"[✔] İŞLEM BAŞARIYLA TAMAMLANDI!")
    print(f"Toplam Çekilen Gerçek Patent Sayısı: {len(df)}")
    print(f"Kaydedilen Dosya: {output_path}")
    print("=" * 80)

if __name__ == "__main__":
    main()
