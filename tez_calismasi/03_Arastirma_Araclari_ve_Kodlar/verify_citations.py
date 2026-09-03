#!/usr/bin/env python3
"""
Academic Citation & DOI Verifier (Crossref API)
Zero-dependency tool using Crossref's public REST API to verify academic citations,
retrieve true DOIs, and prevent hallucinated references.
"""

import sys
import json
import urllib.request
import urllib.parse
import argparse

CROSSREF_API_URL = "https://api.crossref.org/works"

def search_crossref(query=None, doi=None, rows=3):
    headers = {
        "User-Agent": "AcademicThesisAgent/1.0 (mailto:academic-research@universities.edu)"
    }
    
    if doi:
        clean_doi = doi.strip().replace("https://doi.org/", "")
        url = f"{CROSSREF_API_URL}/{urllib.parse.quote(clean_doi)}"
    else:
        params = {
            "query.bibliographic": query,
            "rows": rows
        }
        url = f"{CROSSREF_API_URL}?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        print(f"[Error] HTTP {e.code}: {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"[Error] Connection failed: {e}", file=sys.stderr)
    return None

def verify_item(title=None, author=None, year=None, doi=None):
    print("=" * 60)
    print("AKADEMİK ATIF DOĞRULAMA (CROSSREF REST API)")
    print("=" * 60)
    
    if doi:
        print(f"[*] DOI Sorgulanıyor: {doi}")
        res = search_crossref(doi=doi)
        if res and "message" in res:
            item = res["message"]
            display_match(item, is_exact=True)
            return True
        else:
            print("[X] DOI BULUNAMADI! Bu atıf sahte veya hatalı olabilir.")
            return False

    query_parts = []
    if title: query_parts.append(title)
    if author: query_parts.append(author)
    if year: query_parts.append(str(year))
    full_query = " ".join(query_parts)

    print(f"[*] Literatürde Aranıyor: '{full_query}'")
    res = search_crossref(query=full_query, rows=3)
    
    if not res or "message" not in res or "items" not in res["message"]:
        print("[X] Sonuç bulunamadı.")
        return False
        
    items = res["message"]["items"]
    if not items:
        print("[X] Eşleşen makale bulunamadı! Lütfen atıf bilgilerini kontrol edin.")
        return False
        
    print(f"[+] {len(items)} olası eşleşme bulundu:\n")
    for idx, it in enumerate(items, 1):
        titles = it.get("title", ["Başlık Yok"])
        t = titles[0] if titles else "Başlık Yok"
        authors = it.get("author", [])
        author_names = ", ".join([f"{a.get('family', '')} {a.get('given', '')}" for a in authors[:3]])
        if len(authors) > 3:
            author_names += " et al."
            
        issued = it.get("issued", {}).get("date-parts", [[None]])[0][0]
        doi_val = it.get("DOI", "DOI Yok")
        journal = it.get("container-title", ["Bilinmeyen Dergi"])
        j = journal[0] if journal else "Bilinmeyen Dergi"
        
        print(f"{idx}. {t}")
        print(f"   Yazarlar : {author_names}")
        print(f"   Yıl / Dergi : {issued} | {j}")
        print(f"   DOI     : https://doi.org/{doi_val}")
        print("-" * 50)
        
    return True

def display_match(item, is_exact=False):
    titles = item.get("title", [""])
    t = titles[0] if titles else ""
    authors = item.get("author", [])
    author_str = ", ".join([f"{a.get('family', '')} {a.get('given', '')}" for a in authors])
    doi = item.get("DOI", "")
    journal = item.get("container-title", [""])[0] if item.get("container-title") else ""
    year = item.get("issued", {}).get("date-parts", [[None]])[0][0]
    
    print("[DOĞRULANDI - GERÇEK AKADEMİK KAYNAK]")
    print(f"Başlık  : {t}")
    print(f"Yazarlar: {author_str}")
    print(f"Yıl     : {year}")
    print(f"Dergi   : {journal}")
    print(f"Link    : https://doi.org/{doi}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify academic citations via Crossref")
    parser.add_argument("--doi", help="DOI string to verify")
    parser.add_argument("--title", help="Paper title")
    parser.add_argument("--author", help="Author last name")
    parser.add_argument("--year", help="Publication year")
    parser.add_argument("--query", help="Full free text query")
    
    args = parser.parse_args()
    if not (args.doi or args.title or args.author or args.query):
        parser.print_help()
        sys.exit(1)
        
    q = args.query or args.title
    verify_item(title=q, author=args.author, year=args.year, doi=args.doi)
