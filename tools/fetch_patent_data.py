#!/usr/bin/env python3
"""
Defense Patent Data Fetcher & Network Pipeline Prototype
Queries open patent data for Turkish defense contractors (ASELSAN, TUSAŞ, ROKETSAN, etc.)
and parses IPC classifications, forward citations, and application years.
"""

import json
import urllib.request
import urllib.parse
import csv
import sys

DEFENSE_ASSIGNEES = [
    "ASELSAN ELEKTRONIK SANAYI VE TICARET A.S.",
    "TUSAS TURK HAVACILIK VE UZAY SANAYII A.S.",
    "ROKETSAN ROKET SANAYII VE TICARET A.S.",
    "BAYKAR MAKINA SANAYI VE TICARET A.S.",
    "HAVELSAN HAVA ELEKTRONIK SANAYI VE TICARET A.S.",
    "STM SAVUNMA TEKNOLOJILERI MUHENDISLIK VE TICARET A.S."
]

def generate_sample_pipeline_schema():
    """
    Defines the exact tabular schema for the thesis econometric panel dataset.
    """
    fields = [
        "patent_id",
        "assignee_name",
        "sector_type",         # Defense vs. Civil
        "app_year",
        "grant_year",
        "primary_ipc",         # e.g., G01S (Radar), H04B (Comm), B64C (Aerospace)
        "ipc_class_group",     # Electrical, Mechanical, Instruments
        "forward_citations",   # Number of future patents citing this patent
        "civil_citations",     # Number of civilian company patents citing this patent
        "citing_firm_names",   # List of firms (e.g., Arcelik, Ford Otosan, Turkcell)
        "jaffe_tech_distance"  # Proximity metric to civilian NACE sectors
    ]
    print("[+] Panel Veri Seti Şeması Tanımlandı:")
    for f in fields:
        print(f"  - {f}")
    return fields

if __name__ == "__main__":
    print("=" * 65)
    print("TÜRK SAVUNMA SANAYİİ PATENT VE ATIF AĞI VERİ MİMARİSİ (PROTOTİP)")
    print("=" * 65)
    print(f"Hedef Ana Yükleniciler: {len(DEFENSE_ASSIGNEES)} Şirket")
    for a in DEFENSE_ASSIGNEES:
        print(f"  * {a}")
    print("-" * 65)
    generate_sample_pipeline_schema()
    print("=" * 65)
    print("[Bilgi] Tam veri çekme modülü Aşama 2'de EPATS ve Google Patents API ile entegre edilecektir.")
