#!/usr/bin/env python3
"""
Raw Patent & Citation Processing Pipeline
Converts raw BigQuery / Google Patents / TÜRKPATENT citation extracts into
a balanced econometric panel dataset for PPML and Negative Binomial estimation.
"""

import sys
import os
import argparse
import pandas as pd
import numpy as np

def process_raw_citation_data(input_csv, output_panel_csv):
    """
    Ingests raw citation records and builds the econometric panel.
    """
    if not os.path.exists(input_csv):
        print(f"[!] Hata: Girdi dosyası bulunamadı: {input_csv}")
        return None

    print(f"[*] Ham atıf verisi okunuyor: {input_csv}")
    df_raw = pd.read_csv(input_csv)
    print(f"[+] Toplam ham atıf satırı: {len(df_raw)}")

    # Clean and harmonize defense firm names
    def clean_defense(name):
        name_upper = str(name).upper()
        if "ASELSAN" in name_upper: return "ASELSAN"
        if "TUSAS" in name_upper or "HAVACILIK" in name_upper or "TAI" in name_upper: return "TUSAS"
        if "ROKETSAN" in name_upper: return "ROKETSAN"
        if "BAYKAR" in name_upper: return "BAYKAR"
        if "HAVELSAN" in name_upper: return "HAVELSAN"
        if "STM" in name_upper or "SAVUNMA TEKNOLOJILERI" in name_upper: return "STM"
        return "DIGER_SAVUNMA"

    df_raw["defense_firm_clean"] = df_raw["defense_assignee"].apply(clean_defense)

    # Filter out other defense if any
    df_filtered = df_raw[df_raw["defense_firm_clean"] != "DIGER_SAVUNMA"].copy()

    # Aggregate: Count of citations by (defense_firm, civilian_sector, citation_year)
    agg = df_filtered.groupby(["defense_firm_clean", "civilian_sector_group", "citation_year"]).size().reset_index(name="real_cites")

    print("[+] Sektörel ve yıllık atıf frekansları hesaplandı:")
    print(agg.head(10))

    return agg

def main():
    parser = argparse.ArgumentParser(description="Ham Patent Atıf Verisi İşleme ve Panel Oluşturma Aracı")
    parser.add_argument("--input_csv", help="BigQuery veya Google Patents'ten indirilen ham CSV dosyası")
    parser.add_argument("--output_panel", default="gercek_panel_verisi.csv", help="Üretilecek panel CSV yolu")
    args = parser.parse_args()

    print("=" * 80)
    print("SAVUNMA SANAYİİ HAM PATENT & ATIF VERİ İŞLEME MOTORU")
    print("=" * 80)

    if args.input_csv:
        process_raw_citation_data(args.input_csv, args.output_panel)
    else:
        print("[i] Kullanım: python3 tools/process_real_patents.py --input_csv <ham_veri.csv>")
        print("[i] BigQuery SQL şablonu: tools/extract_defense_citations_bigquery.sql")

if __name__ == "__main__":
    main()
