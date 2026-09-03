#!/usr/bin/env python3
"""
Jaffe (1993) Technological Proximity & Distance Index Calculator
Calculates the technological distance matrix between defense contractors and civilian sectors
based on IPC (International Patent Classification) patent distributions.

Formula:
P_{ij} = (F_i . F_j) / ( ||F_i|| * ||F_j|| )
where F_i is the vector of patent shares across IPC technology classes.
"""

import sys
import json
import math
import argparse
import csv

# Sample default Turkish Defense vs Civilian IPC distribution (IPC 4-digit)
# Used for initial calibration and simulation
DEFAULT_FIRMS_IPC = {
    # Savunma Ana Yüklenicileri
    "ASELSAN": {
        "G01S": 45,  # Radar, sonar, lidarlar
        "H04B": 38,  # Radyo ve kablosuz haberleşme
        "H01Q": 25,  # Antenler ve dalga kılavuzları
        "F41G": 30,  # Silah nişangah ve atış kontrol
        "G06T": 20,  # Görüntü işleme ve elektro-optik
        "B64U": 15   # İHA kontrol ve aviyonik
    },
    "TUSAS": {
        "B64C": 55,  # Uçak ve helikopter gövde/yapı
        "B64D": 40,  # Uçak teçhizatı ve aviyonik sistemler
        "B64U": 50,  # İnsansız hava araçları (İHA)
        "G05D": 22,  # Otopilot ve kontrol sistemleri
        "B29C": 18   # Kompozit malzeme şekillendirme
    },
    "ROKETSAN": {
        "F42B": 60,  # Mühimmat, roket ve füzeler
        "F02K": 35,  # Roket motorları ve itki sistemleri
        "C06B": 25,  # Katı yakıt ve patlayıcı kimyası
        "G01C": 20   # Ataletsel seyrüsefer (INS) sensörleri
    },
    "BAYKAR": {
        "B64U": 65,  # İnsansız hava sistemleri
        "G05D": 45,  # Uçuş kontrol ve otonomi algoritmaları
        "G08G": 20,  # Hava trafik kontrol ve radar
        "B64C": 30   # Aerodinamik gövde tasarımı
    },
    "HAVELSAN": {
        "G06F": 50,  # Yazılım mimarileri ve C4ISR komuta kontrol
        "G09B": 45,  # Askeri ve sivil uçuş/görev simülatörleri
        "H04L": 35,  # Güvenli ağ iletimi ve siber savunma
        "G06T": 25   # Sentetik taktik çevre modelleme
    },
    "STM": {
        "G01C": 25,  # Ataletsel seyrüsefer ve hassas konumlandırma (EP3120166B1, US10353079B2)
        "B64U": 20,  # Taktik mini İHA kontrolü (KARGU, ALPAGU, TOGAN)
        "B63G": 18,  # Askeri denizaltı/suüstü platform gövde & akustik sönümleme (TR201000065A2)
        "H04L": 15,  # Siber savunma ve taktik veri füzyonu
        "G05D": 12   # Otonom rota planlama ve sürü zekâsı
    },
    "ARCELIK_BeyazEsya": {
        "A47L": 70,  # Ev aletleri ve yıkama
        "F25D": 65,  # Soğutma sistemleri
        "H04B": 15,  # Akıllı ev / IoT haberleşme
        "G05D": 12,  # Otomatik kontrol
        "G06T": 8    # Kamera/görüntü tanıma
    },
    "FORD_OTOSAN_Otomotiv": {
        "B60W": 55,  # Sürüş destek ve otonom araç kontrolü
        "G01S": 25,  # Otomotiv radarı ve lidar
        "H04B": 20,  # V2X araç haberleşmesi
        "B60K": 30,  # Elektrikli tahrik sistemleri
        "G05D": 28   # Şerit takip ve hareket kontrolü
    },
    "TURKCELL_Telekom": {
        "H04B": 85,  # 5G/6G baz istasyonu ve kablosuz aktarım
        "H04L": 70,  # Veri iletimi ve şifreleme
        "G06T": 15,  # Mobil görüntü analitiği
        "G01S": 10   # Konumlandırma ve baz istasyonu radarı
    }
}

def calculate_jaffe_proximity(vec1, vec2, all_classes):
    """
    Computes cosine similarity between two patent frequency vectors.
    """
    dot_product = sum(vec1.get(cls, 0) * vec2.get(cls, 0) for cls in all_classes)
    norm1 = math.sqrt(sum(vec1.get(cls, 0) ** 2 for cls in all_classes))
    norm2 = math.sqrt(sum(vec2.get(cls, 0) ** 2 for cls in all_classes))
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)

def compute_full_matrix(firms_data):
    all_classes = sorted(list(set(cls for data in firms_data.values() for cls in data.keys())))
    firm_names = list(firms_data.keys())
    
    matrix = {}
    for f1 in firm_names:
        matrix[f1] = {}
        for f2 in firm_names:
            matrix[f1][f2] = calculate_jaffe_proximity(firms_data[f1], firms_data[f2], all_classes)
    return firm_names, matrix, all_classes

def print_table(firm_names, matrix):
    print("=" * 85)
    print("JAFFE (1993) TEKNOLOJİK YAKINLIK MATRİSİ (TECHNOLOGICAL PROXIMITY - P_ij)")
    print("=" * 85)
    header = f"{'Firma':<22} | " + " | ".join([f"{f[:8]:>8}" for f in firm_names])
    print(header)
    print("-" * len(header))
    for f1 in firm_names:
        row = f"{f1:<22} | " + " | ".join([f"{matrix[f1][f2]:8.3f}" for f2 in firm_names])
        print(row)
    print("=" * 85)
    print("[i] 1.000 = Tam teknolojik örtüşme | 0.000 = Sıfır ortak teknoloji tabanı.")

def main():
    parser = argparse.ArgumentParser(description="Jaffe (1993) Teknolojik Mesafe Hesaplayıcı")
    parser.add_argument("--json", help="Özel firma IPC JSON dosya yolu")
    parser.add_argument("--export_csv", help="Sonuçları CSV olarak kaydetme yolu")
    args = parser.parse_args()
    
    firms_data = DEFAULT_FIRMS_IPC
    if args.json:
        with open(args.json, "r", encoding="utf-8") as f:
            firms_data = json.load(f)
            
    firm_names, matrix, all_classes = compute_full_matrix(firms_data)
    print_table(firm_names, matrix)
    
    print("\n🔍 ÖRNEK YAYILMA (SPILLOVER) YAKINLIK KATSAYILARI:")
    print(f"-> ASELSAN <-> FORD OTOSAN (Radar & Kontrol): {matrix['ASELSAN']['FORD_OTOSAN_Otomotiv']:.4f}")
    print(f"-> ASELSAN <-> TURKCELL (Haberleşme): {matrix['ASELSAN']['TURKCELL_Telekom']:.4f}")
    print(f"-> TUSAŞ <-> FORD OTOSAN (Otonom Kontrol): {matrix['TUSAS']['FORD_OTOSAN_Otomotiv']:.4f}")
    print(f"-> ROKETSAN <-> ARÇELİK (Uzak Teknoloji Kümeleri): {matrix['ROKETSAN']['ARCELIK_BeyazEsya']:.4f}")
    
    if args.export_csv:
        with open(args.export_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Firma"] + firm_names)
            for f1 in firm_names:
                writer.writerow([f1] + [round(matrix[f1][f2], 4) for f2 in firm_names])
        print(f"\n[+] Matris başarıyla CSV olarak kaydedildi: {args.export_csv}")

if __name__ == "__main__":
    main()
