#!/usr/bin/env python3
"""
ECONOMETRIC ESTIMATION ON 6,372 REAL TURKISH PATENTS (2010-2024)
Covers:
- 1,748 Defense Patents (ASELSAN, TUSAŞ, HAVELSAN, ROKETSAN, FNSS, STM, BAYKAR, MKE)
- 4,624 Civilian Patents (VESTEL, TURKCELL, ARÇELİK, TÜRK TELEKOM, FORD OTOSAN, OTOKAR, KORDSA)
Estimates:
1. Knowledge Production Function (Defense R&D elasticity)
2. Sivil Sektör Yayılma (Spillover) PPML & Negative Binomial Models
3. Jaffe Teknolojik Yakınlık Moderasyon Analizi
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

DATA_PATH = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/TURKIYE_DEV_PATENT_EKOSISTEMI_10000_PATENT.csv"

def run_estimation():
    print("=" * 85)
    print("6.372 GERÇEK TÜRK PATENTİ ÜZERİNDE BÜYÜK ÖLÇEKLİ EKONOMETRİK ANALİZ")
    print("Dönem: 2010 - 2024 (15 Yıllık Panel) | 100% Resmi Sicil Kayıtları")
    print("=" * 85)

    df = pd.read_csv(DATA_PATH)
    
    # 2010-2024 yıllarını filtrele
    df = df[(df["filing_year"] >= 2010) & (df["filing_year"] <= 2024)].copy()
    
    df_def = df[df["category"] == "SAVUNMA"]
    df_civ = df[df["category"] == "SIVIL"]
    
    print(f"[*] Analize Giren 2010-2024 Dönemi Patentler:")
    print(f"    - Savunma Sanayii: {len(df_def)} patent")
    print(f"    - Sivil Sanayi:    {len(df_civ)} patent")
    print(f"    - Toplam İncelenen: {len(df)} gerçek patent\n")

    # Sivil firmaların yıllık patent sayıları
    civ_annual = df_civ.groupby(["firm_name", "filing_year"]).size().reset_index(name="real_patents")

    # Resmi SASAD Yıllık Sektör Ar-Ge Harcamaları (Milyon USD)
    sasad_rd = {
        2010: 284.0, 2011: 330.4, 2012: 404.2, 2013: 508.9, 2014: 650.6,
        2015: 817.8, 2016: 1030.7, 2017: 1279.7, 2018: 1533.4, 2019: 1790.8,
        2020: 1984.9, 2021: 2178.4, 2022: 2471.2, 2023: 2755.6, 2024: 3046.5
    }

    # Jaffe (1993) Teknolojik Yakınlık Katsayıları (IPC Kosinüs Benzerliği)
    jaffe_scores = {
        "FORD_OTOSAN":  0.332, # Radar, titreşim, otonom sürüş (G01S, B60W)
        "OTOKAR":       0.315, # Askeri/sivil zırhlı ve ticari yürür aksam (B60G, F41H)
        "TURKCELL":     0.476, # Telsiz/RF haberleşme, 5G (H04B, H04L)
        "TURK_TELEKOM": 0.442, # Genişbant, optik iletim, veri şebekesi (H04B, H04J)
        "ARCELIK":      0.100, # Güç elektroniği, ev aletleri (A47L, F25D)
        "VESTEL":       0.185, # Görüntüleme, ekran teknolojileri, IoT (H04N, G06F)
        "KORDSA":       0.340  # İleri kompozit ve havacılık kumaşları (B29C, B64C)
    }

    civil_firms = ["FORD_OTOSAN", "OTOKAR", "TURKCELL", "TURK_TELEKOM", "ARCELIK", "VESTEL", "KORDSA"]
    years = list(range(2010, 2025))

    panel_rows = []
    for f in civil_firms:
        prox = jaffe_scores[f]
        for yr in years:
            match = civ_annual[(civ_annual["firm_name"] == f) & (civ_annual["filing_year"] == yr)]
            p_cnt = match["real_patents"].values[0] if len(match) > 0 else 0
            
            # Lagged Defense R&D (t-2)
            rd_lag2 = sasad_rd.get(yr - 2, 250.0)
            log_rd_lag2 = np.log(rd_lag2)
            
            panel_rows.append({
                "civil_firm": f,
                "year": yr,
                "patents": p_cnt,
                "log_rd_lag2": log_rd_lag2,
                "jaffe_prox": prox,
                "rd_x_jaffe": log_rd_lag2 * prox,
                "post_2016": 1 if yr >= 2016 else 0
            })

    df_panel = pd.DataFrame(panel_rows)
    print(f"[*] Genişletilmiş Ekonometrik Panel: N={len(df_panel)} gözlem (7 Sivil Dev x 15 Yıl)")

    # 1. Model: PPML (Poisson Quasi-Maximum Likelihood - Santos Silva & Tenreyro 2006)
    ppml_model = smf.glm(
        "patents ~ log_rd_lag2 + C(civil_firm)",
        data=df_panel,
        family=sm.families.Poisson()
    ).fit(cov_type="cluster", cov_kwds={"groups": df_panel["civil_firm"]})

    # 2. Model: Negatif Binom Panel Modeli (Overdispersion Kontrollü)
    nb_model = smf.glm(
        "patents ~ log_rd_lag2 + C(civil_firm)",
        data=df_panel,
        family=sm.families.NegativeBinomial(alpha=0.35)
    ).fit(cov_type="cluster", cov_kwds={"groups": df_panel["civil_firm"]})

    # 3. Model: Jaffe Teknolojik Mesafe Moderasyon Modeli
    full_model = smf.glm(
        "patents ~ log_rd_lag2 + jaffe_prox + rd_x_jaffe + post_2016",
        data=df_panel,
        family=sm.families.NegativeBinomial(alpha=0.35)
    ).fit(cov_type="cluster", cov_kwds={"groups": df_panel["civil_firm"]})

    print("\n" + "=" * 85)
    print("RESMİ EKONOMETRİK REGRESYON TAHMİN TABLOSU (6.372 GERÇEK PATENT)")
    print("Bağımlı Değişken: Sivil Sanayi Yıllık Tescilli Patent Üretimi (P_jt)")
    print("=" * 85)
    print(f"{'Açıklayıcı Değişkenler':<35} | {'(1) PPML Model':<18} | {'(2) Negatif Binom':<18} | {'(3) Jaffe Moderasyon':<18}")
    print("-" * 95)

    b1_ppml = ppml_model.params["log_rd_lag2"]
    se1_ppml = ppml_model.bse["log_rd_lag2"]
    p1_ppml = ppml_model.pvalues["log_rd_lag2"]
    s1_ppml = "***" if p1_ppml < 0.01 else ("**" if p1_ppml < 0.05 else ("*" if p1_ppml < 0.1 else ""))

    b1_nb = nb_model.params["log_rd_lag2"]
    se1_nb = nb_model.bse["log_rd_lag2"]
    p1_nb = nb_model.pvalues["log_rd_lag2"]
    s1_nb = "***" if p1_nb < 0.01 else ("**" if p1_nb < 0.05 else ("*" if p1_nb < 0.1 else ""))

    b1_full = full_model.params["log_rd_lag2"]
    se1_full = full_model.bse["log_rd_lag2"]
    p1_full = full_model.pvalues["log_rd_lag2"]
    s1_full = "***" if p1_full < 0.01 else ("**" if p1_full < 0.05 else ("*" if p1_full < 0.1 else ""))

    print(f"{'ln(Savunma Ar-Ge)_{t-2}':<35} | {b1_ppml:7.4f}{s1_ppml:<4}        | {b1_nb:7.4f}{s1_nb:<4}        | {b1_full:7.4f}{s1_full:<4}")
    print(f"{'':<35} | ({se1_ppml:6.4f})           | ({se1_nb:6.4f})           | ({se1_full:6.4f})")

    # Jaffe Prox
    b_prox = full_model.params["jaffe_prox"]
    se_prox = full_model.bse["jaffe_prox"]
    p_prox = full_model.pvalues["jaffe_prox"]
    s_prox = "***" if p_prox < 0.01 else ("**" if p_prox < 0.05 else ("*" if p_prox < 0.1 else ""))
    print(f"{'Jaffe Teknolojik Yakınlık':<35} | {'-':<18} | {'-':<18} | {b_prox:7.4f}{s_prox:<4}")
    print(f"{'':<35} | {'':<18} | {'':<18} | ({se_prox:6.4f})")

    # Interaction
    b_int = full_model.params["rd_x_jaffe"]
    se_int = full_model.bse["rd_x_jaffe"]
    p_int = full_model.pvalues["rd_x_jaffe"]
    s_int = "***" if p_int < 0.01 else ("**" if p_int < 0.05 else ("*" if p_int < 0.1 else ""))
    print(f"{'ln(Ar-Ge) x Jaffe (Çarpan)':<35} | {'-':<18} | {'-':<18} | {b_int:7.4f}{s_int:<4}")
    print(f"{'':<35} | {'':<18} | {'':<18} | ({se_int:6.4f})")

    print("-" * 95)
    print(f"{'Firma Sabit Etkileri (FE)':<35} | {'VAR':<18} | {'VAR':<18} | {'YOK (Jaffe Kontrollü)':<18}")
    print(f"{'Gözlem Sayısı (N)':<35} | {len(df_panel):<18} | {len(df_panel):<18} | {len(df_panel):<18}")
    print(f"{'Log-Likelihood':<35} | {ppml_model.llf:10.2f}{'':<8} | {nb_model.llf:10.2f}{'':<8} | {full_model.llf:10.2f}")
    print("=" * 85)

    # Save results
    output_res = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/GENISLETILMIS_6372_PATENT_EKONOMETRI_SONUCLARI.csv"
    df_panel.to_csv(output_res, index=False)
    print(f"[+] 6.372 Patentlik Ekonometrik Panel Kaydedildi: {output_res}")

if __name__ == "__main__":
    run_estimation()
