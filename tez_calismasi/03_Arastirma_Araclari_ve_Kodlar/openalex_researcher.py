#!/usr/bin/env python3
"""
OpenAlex Academic Literature & Citation Intelligence Tool
Zero-dependency, zero-API-key client for OpenAlex REST API (https://api.openalex.org)
Retrieves peer-reviewed papers, abstracts, citation counts, open-access links,
and automatically generates APA 7 compliant bibliographic references.
"""

import sys
import json
import urllib.request
import urllib.parse
import argparse

OPENALEX_API_URL = "https://api.openalex.org/works"

def search_openalex(query, filter_type=None, sort="cited_by_count:desc", per_page=5):
    """
    Queries OpenAlex for scholarly works.
    """
    headers = {
        "User-Agent": "AcademicThesisAgent/2.0 (mailto:academic-research@universities.edu)"
    }
    
    params = {
        "search": query,
        "sort": sort,
        "per_page": per_page
    }
    
    if filter_type:
        params["filter"] = filter_type
        
    url = f"{OPENALEX_API_URL}?{urllib.parse.urlencode(params)}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data.get("results", [])
    except Exception as e:
        print(f"[Hata] OpenAlex API sorgusu başarısız: {e}", file=sys.stderr)
        return []

def format_apa7(work):
    """
    Formats an OpenAlex work into APA 7th edition citation and bibliography.
    """
    # Authors
    authorships = work.get("authorships", [])
    author_names = []
    for a in authorships:
        author = a.get("author", {})
        display_name = author.get("display_name", "")
        if display_name:
            parts = display_name.split()
            if len(parts) > 1:
                last = parts[-1]
                initials = " ".join([p[0] + "." for p in parts[:-1]])
                author_names.append(f"{last}, {initials}")
            else:
                author_names.append(display_name)
                
    if not author_names:
        authors_str = "Bilinmeyen Yazar"
        in_text_str = "Bilinmeyen"
    elif len(author_names) == 1:
        authors_str = author_names[0]
        in_text_str = author_names[0].split(",")[0]
    elif len(author_names) == 2:
        authors_str = f"{author_names[0]} & {author_names[1]}"
        in_text_str = f"{author_names[0].split(',')[0]} ve {author_names[1].split(',')[0]}"
    else:
        authors_str = f"{author_names[0]} vd."
        in_text_str = f"{author_names[0].split(',')[0]} vd."
        
    year = work.get("publication_year", "t.y.")
    title = work.get("title", "Başlıksız")
    
    # Journal / Venue
    primary_location = work.get("primary_location") or {}
    source = primary_location.get("source") or {}
    journal = source.get("display_name", "")
    
    # DOI
    doi = work.get("doi", "")
    
    # Citation Count & Open Access
    cited_by = work.get("cited_by_count", 0)
    open_access = work.get("open_access", {})
    oa_url = open_access.get("oa_url", "")
    
    apa_ref = f"{authors_str} ({year}). {title}."
    if journal:
        apa_ref += f" *{journal}*."
    if doi:
        apa_ref += f" {doi}"
        
    return {
        "apa_ref": apa_ref,
        "in_text": f"({in_text_str}, {year})",
        "title": title,
        "year": year,
        "journal": journal,
        "doi": doi,
        "cited_by": cited_by,
        "oa_url": oa_url
    }

def main():
    parser = argparse.ArgumentParser(description="OpenAlex Literatür ve Atıf Arama Aracı")
    parser.add_argument("query", help="Arama sorgusu (örn: 'defense R&D spillover' veya 'patent citation network')")
    parser.add_argument("--count", type=int, default=5, help="Getirilecek sonuç sayısı (varsayılan: 5)")
    parser.add_argument("--sort", choices=["cited", "recent"], default="cited", help="Sıralama ölçütü (en çok atıf / en yeni)")
    args = parser.parse_args()
    
    sort_param = "cited_by_count:desc" if args.sort == "cited" else "publication_year:desc"
    
    print("=" * 70)
    print(f"[*] OPENALEX LİTERATÜR ARAMASI: '{args.query}'")
    print(f"[*] Sıralama: {'En Çok Atıf Alanlar' if args.sort == 'cited' else 'En Yeniler'}")
    print("=" * 70)
    
    results = search_openalex(args.query, sort=sort_param, per_page=args.count)
    if not results:
        print("[!] Hiçbir akademik yayın bulunamadı.")
        return
        
    for i, work in enumerate(results, 1):
        info = format_apa7(work)
        print(f"\n[{i}] {info['title']}")
        print(f"    Yıl & Dergi : {info['year']} | {info['journal'] if info['journal'] else 'Kitap/Rapor/Arşiv'}")
        print(f"    Atıf Sayısı : {info['cited_by']} atıf")
        print(f"    APA 7 Metin İçi : {info['in_text']}")
        print(f"    APA 7 Kaynakça : {info['apa_ref']}")
        if info['oa_url']:
            print(f"    Açık Erişim PDF : {info['oa_url']}")
        print("-" * 70)

if __name__ == "__main__":
    main()
