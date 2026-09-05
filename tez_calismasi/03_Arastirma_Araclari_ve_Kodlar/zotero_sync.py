#!/usr/bin/env python3
"""
ZOTERO LIBRARY SYNC & MANAGER
Directly communicates with Zotero Web API using user credentials:
User ID: 21484193
API Key: 2JL9AtKCiRo88Qki7FxY5I1x
"""

import urllib.request
import json
import re

USER_ID = "21484193"
API_KEY = "2JL9AtKCiRo88Qki7FxY5I1x"
BASE_URL = f"https://api.zotero.org/users/{USER_ID}"

HEADERS = {
    "Zotero-API-Version": "3",
    "Zotero-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def get_library_items():
    url = f"{BASE_URL}/items?limit=25"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp:
            items = json.loads(resp.read().decode())
            print(f"[✔] Zotero Kütüphanesindeki Toplam Eser Sayısı: {len(items)}")
            for it in items:
                d = it.get("data", {})
                print(f"  - [{d.get('itemType')}] {d.get('title')} ({d.get('date', 'Yıl Belirtilmemiş')})")
            return items
    except Exception as e:
        print("[!] Hata:", e)
        return []

def add_item_to_zotero(title, creators, item_type="journalArticle", date="", publication="", doi="", abstract=""):
    url = f"{BASE_URL}/items"
    creator_list = []
    for c in creators:
        creator_list.append({
            "creatorType": "author",
            "firstName": c.get("first", ""),
            "lastName": c.get("last", "")
        })
        
    payload = [{
        "itemType": item_type,
        "title": title,
        "creators": creator_list,
        "date": date,
        "publicationTitle": publication,
        "DOI": doi,
        "abstractNote": abstract
    }]
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode())
            print(f"[✔] Eser Zotero'ya başarıyla eklendi: {title}")
            return res
    except Exception as e:
        print(f"[!] Eser eklenirken hata: {e}")
        return None

def sync_bibtex_to_zotero(bib_path):
    print(f"[*] BibTeX dosyasından Zotero'ya aktarım başlatılıyor: {bib_path}")
    with open(bib_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    entries = re.split(r'@\w+\{', content)[1:]
    print(f"[*] Tespit edilen kaynak sayısı: {len(entries)}")
    
    for entry in entries[:10]: # İlk 10 kritik makaleyi yükle
        title_m = re.search(r'title\s*=\s*\{([^}]+)\}', entry)
        author_m = re.search(r'author\s*=\s*\{([^}]+)\}', entry)
        year_m = re.search(r'year\s*=\s*\{([^}]+)\}', entry)
        journal_m = re.search(r'journal\s*=\s*\{([^}]+)\}', entry)
        doi_m = re.search(r'doi\s*=\s*\{([^}]+)\}', entry)
        
        if title_m:
            title = title_m.group(1).replace("\n", " ").strip()
            date = year_m.group(1) if year_m else ""
            pub = journal_m.group(1) if journal_m else ""
            doi = doi_m.group(1) if doi_m else ""
            
            creators = []
            if author_m:
                authors = author_m.group(1).split(" and ")
                for a in authors:
                    parts = a.split(",")
                    if len(parts) == 2:
                        creators.append({"last": parts[0].strip(), "first": parts[1].strip()})
                    else:
                        creators.append({"last": a.strip(), "first": ""})
                        
            add_item_to_zotero(title, creators, date=date, publication=pub, doi=doi)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "sync":
        sync_bibtex_to_zotero("/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/05_Literatur_Kutuphanesi/thesis_references.bib")
    else:
        get_library_items()
