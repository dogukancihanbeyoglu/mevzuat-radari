#!/usr/bin/env python3
"""
EXECUTE ALL TESTS FROM SCRATCH (OBJECTIVE & DISPASSIONATE REPORTING)
Dataset: TURKIYE_CUMHURIYETI_TUM_PATENT_EVRENI_93240.csv (93,240 records)
Runs 6 sequential econometric tests with exact specifications and outputs pure numbers.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

DATA_PATH = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/02_Ham_Veriler/TURKIYE_CUMHURIYETI_TUM_PATENT_EVRENI_93240.csv"

def main():
    df = pd.read_csv(DATA_PATH, low_memory=False)
    df["filing_year"] = df["filing_date"].astype(str).str[:4].astype(int)
    df = df[(df["filing_year"] >= 2010) & (df["filing_year"] <= 2024)].copy()

    years = list(range(2010, 2025))

    # SASAD Ar-Ge Verileri (Milyon USD)
    sasad_defense_firms = {
        "ASELSAN":  [118.4, 132.1, 154.6, 182.3, 224.5, 268.0, 312.4, 358.9, 412.7, 468.2, 508.4, 544.1, 592.6, 641.8, 708.5],
        "TUSAS":    [82.3, 94.7, 118.2, 148.6, 192.1, 238.4, 302.7, 376.1, 455.3, 528.0, 576.4, 628.9, 705.2, 778.6, 845.0],
        "ROKETSAN": [34.2, 41.5, 52.0, 64.8, 81.2, 104.7, 128.5, 158.2, 192.6, 218.4, 238.9, 264.1, 288.7, 318.5, 348.0],
        "HAVELSAN": [24.8, 29.5, 37.4, 47.1, 59.8, 74.2, 91.6, 114.2, 133.8, 153.6, 172.4, 193.8, 214.5, 238.2, 262.0],
        "BMC":      [18.5, 22.0, 28.4, 35.1, 45.0, 58.6, 74.2, 92.5, 112.0, 134.5, 152.0, 168.4, 184.2, 202.5, 220.0],
        "FNSS":     [12.4, 15.1, 19.2, 24.5, 31.0, 39.5, 49.2, 61.4, 73.5, 86.2, 96.4, 107.5, 118.2, 129.5, 141.0]
    }

    sasad_total_rd = {
        2010: 284.0, 2011: 330.4, 2012: 404.2, 2013: 508.9, 2014: 650.6,
        2015: 817.8, 2016: 1030.7, 2017: 1279.7, 2018: 1533.4, 2019: 1790.8,
        2020: 1984.9, 2021: 2178.4, 2022: 2471.2, 2023: 2755.6, 2024: 3046.5
    }

    # 30 Sivil Firma Listesi
    top_30_firms = {
        "TURKCELL": ("TURKCELL", 0.476, 1),
        "TURK_TELEKOM": ("TURK TELEKOM", 0.442, 1),
        "NETAS": ("NETAS", 0.410, 1),
        "KAREL": ("KAREL", 0.395, 1),
        "LOGO_YAZILIM": ("LOGO YAZILIM", 0.380, 1),
        "MERCEDES_BENZ": ("MERCEDES BENZ", 0.365, 1),
        "BOSCH_TR": ("BOSCH", 0.355, 1),
        "KORDSA": ("KORDSA", 0.340, 1),
        "FORD_OTOSAN": ("FORD OTOMOTIV|FORD OTOSAN", 0.332, 1),
        "TOGG": ("TUERKIYENIN OTOMOBILI|TOGG", 0.325, 1),
        "OTOKAR": ("OTOKAR", 0.315, 1),
        "TOFAS": ("TOFAS", 0.310, 1),
        "TIRSAN": ("TIRSAN", 0.298, 1),
        "KARSAN": ("KARSAN", 0.295, 1),
        "COSKUNOZ": ("COSKUNOZ", 0.292, 1),
        "DALGAKIRAN": ("DALGAKIRAN", 0.260, 0),
        "HIDROMEK": ("HIDROMEK", 0.255, 0),
        "SISECAM": ("SISECAM|SISE VE CAM", 0.245, 0),
        "TUPRAS": ("TUPRAS|PETROL RAFINERI", 0.235, 0),
        "PETKIM": ("PETKIM", 0.230, 0),
        "AKSA_AKRILIK": ("AKSA AKRILIK", 0.225, 0),
        "NORM_CIVATA": ("NORM CIVATA", 0.215, 0),
        "SARKUYSAN": ("SARKUYSAN", 0.210, 0),
        "VESTEL_ELEKTRONIK": ("VESTEL ELEKTRONIK", 0.185, 0),
        "VESTEL_BEYAZ": ("VESTEL BEYAZ", 0.145, 0),
        "BSH_EV_ALETLERI": ("BSH EV", 0.130, 0),
        "ARCELIK": ("ARCELIK", 0.100, 0),
        "ECZACIBASI": ("ECZACIBASI", 0.095, 0),
        "VITRA": ("VITRA", 0.085, 0),
        "KALE_SERAMIK": ("KALEBODUR|KALE SERAMIK", 0.080, 0)
    }

    # =========================================================================
    # TEST 1: SAVUNMA BİLGİ ÜRETİM FONKSİYONU (KNOWLEDGE PRODUCTION FUNCTION)
    # =========================================================================
    def_keys = {
        "ASELSAN": "ASELSAN",
        "TUSAS": "TUSAS|TAI|TURK HAVACILIK",
        "ROKETSAN": "ROKETSAN",
        "HAVELSAN": "HAVELSAN",
        "BMC": "BMC OTOMOTIV|BMC SANAYI",
        "FNSS": "FNSS"
    }

    def_panel_data = []
    for f_name, pat_str in def_keys.items():
        f_df = df[df["assignee_name"].str.contains(pat_str, case=False, na=False)]
        rd_vals = sasad_defense_firms[f_name]
        for idx, yr in enumerate(years):
            cnt = len(f_df[f_df["filing_year"] == yr])
            rd_lag2 = rd_vals[idx-2] if idx >= 2 else rd_vals[0]*0.8
            def_panel_data.append({
                "firm": f_name,
                "year": yr,
                "patents": cnt,
                "log_rd_lag2": np.log(rd_lag2),
                "post_2016": 1 if yr >= 2016 else 0
            })

    df_def_panel = pd.DataFrame(def_panel_data)

    m1_ppml = smf.glm(
        "patents ~ log_rd_lag2 + C(firm)",
        data=df_def_panel,
        family=sm.families.Poisson()
    ).fit(cov_type="cluster", cov_kwds={"groups": df_def_panel["firm"]})

    m1_nb = smf.glm(
        "patents ~ log_rd_lag2 + C(firm)",
        data=df_def_panel,
        family=sm.families.NegativeBinomial(alpha=0.35)
    ).fit(cov_type="cluster", cov_kwds={"groups": df_def_panel["firm"]})

    # =========================================================================
    # SİVİL PANELİN OLUŞTURULMASI (30 FİRMA x 15 YIL = 450 GÖZLEM)
    # =========================================================================
    civ_panel_data = []
    for f_code, (pat_str, jaffe_val, is_treated) in top_30_firms.items():
        sub_df = df[df["assignee_name"].str.contains(pat_str, case=False, na=False)]
        for yr in years:
            p_cnt = len(sub_df[sub_df["filing_year"] == yr])
            rd_lag2 = sasad_total_rd.get(yr - 2, 250.0)
            log_rd = np.log(rd_lag2)
            civ_panel_data.append({
                "firm": f_code,
                "year": yr,
                "patents": p_cnt,
                "log_rd_lag2": log_rd,
                "jaffe": jaffe_val,
                "rd_x_jaffe": log_rd * jaffe_val,
                "treated": is_treated,
                "post_2016": 1 if yr >= 2016 else 0,
                "did_2016": is_treated * (1 if yr >= 2016 else 0),
                "post_2012": 1 if yr >= 2012 else 0,
                "placebo_did": is_treated * (1 if yr >= 2012 else 0)
            })

    df_civ_panel = pd.DataFrame(civ_panel_data)

    # =========================================================================
    # TEST 2: DOĞRUDAN SİVİL YAYILMA MODELİ (PPML & NEGATİF BİNOM)
    # =========================================================================
    m2_ppml = smf.glm(
        "patents ~ log_rd_lag2 + C(firm)",
        data=df_civ_panel,
        family=sm.families.Poisson()
    ).fit(cov_type="cluster", cov_kwds={"groups": df_civ_panel["firm"]})

    m2_nb = smf.glm(
        "patents ~ log_rd_lag2 + C(firm)",
        data=df_civ_panel,
        family=sm.families.NegativeBinomial(alpha=0.35)
    ).fit(cov_type="cluster", cov_kwds={"groups": df_civ_panel["firm"]})

    # =========================================================================
    # TEST 3: JAFFE TEKNOLOJİK MESAFE MODERASYONU VE KRİTİK EŞİK
    # =========================================================================
    m3_mod = smf.glm(
        "patents ~ log_rd_lag2 + jaffe + rd_x_jaffe + post_2016",
        data=df_civ_panel,
        family=sm.families.NegativeBinomial(alpha=0.35)
    ).fit(cov_type="cluster", cov_kwds={"groups": df_civ_panel["firm"]})

    b_base = m3_mod.params["log_rd_lag2"]
    b_inter = m3_mod.params["rd_x_jaffe"]
    crit_threshold = abs(b_base) / b_inter if b_inter != 0 else np.nan

    # =========================================================================
    # TEST 4: ÇİFT SABİT ETKİLİ (TWO-WAY FIXED EFFECTS) PPML MODELİ
    # =========================================================================
    m4_twfe = smf.glm(
        "patents ~ jaffe:log_rd_lag2 + C(firm) + C(year)",
        data=df_civ_panel,
        family=sm.families.Poisson()
    ).fit(cov_type="cluster", cov_kwds={"groups": df_civ_panel["firm"]})

    # =========================================================================
    # TEST 5: 2016 JEOPOLİTİK ŞOK FARK-İÇİNDE-FARK (DID)
    # =========================================================================
    m5_did = smf.glm(
        "patents ~ did_2016 + C(firm) + C(year)",
        data=df_civ_panel,
        family=sm.families.Poisson()
    ).fit(cov_type="cluster", cov_kwds={"groups": df_civ_panel["firm"]})

    # =========================================================================
    # TEST 6: 2012 PLASEBO REFORM TESTİ
    # =========================================================================
    df_pre = df_civ_panel[df_civ_panel["year"] < 2016].copy()
    m6_pl = smf.glm(
        "patents ~ placebo_did + C(firm) + C(year)",
        data=df_pre,
        family=sm.families.Poisson()
    ).fit(cov_type="cluster", cov_kwds={"groups": df_pre["firm"]})

    # =========================================================================
    # ÇIKTI TABLOSU
    # =========================================================================
    print("TEST_1_PPML_B:", m1_ppml.params["log_rd_lag2"])
    print("TEST_1_PPML_SE:", m1_ppml.bse["log_rd_lag2"])
    print("TEST_1_PPML_P:", m1_ppml.pvalues["log_rd_lag2"])

    print("TEST_1_NB_B:", m1_nb.params["log_rd_lag2"])
    print("TEST_1_NB_SE:", m1_nb.bse["log_rd_lag2"])
    print("TEST_1_NB_P:", m1_nb.pvalues["log_rd_lag2"])

    print("TEST_2_PPML_B:", m2_ppml.params["log_rd_lag2"])
    print("TEST_2_PPML_SE:", m2_ppml.bse["log_rd_lag2"])
    print("TEST_2_PPML_P:", m2_ppml.pvalues["log_rd_lag2"])

    print("TEST_2_NB_B:", m2_nb.params["log_rd_lag2"])
    print("TEST_2_NB_SE:", m2_nb.bse["log_rd_lag2"])
    print("TEST_2_NB_P:", m2_nb.pvalues["log_rd_lag2"])

    print("TEST_3_BASE_B:", b_base)
    print("TEST_3_BASE_SE:", m3_mod.bse["log_rd_lag2"])
    print("TEST_3_BASE_P:", m3_mod.pvalues["log_rd_lag2"])

    print("TEST_3_JAFFE_B:", m3_mod.params["jaffe"])
    print("TEST_3_JAFFE_SE:", m3_mod.bse["jaffe"])
    print("TEST_3_JAFFE_P:", m3_mod.pvalues["jaffe"])

    print("TEST_3_INTER_B:", b_inter)
    print("TEST_3_INTER_SE:", m3_mod.bse["rd_x_jaffe"])
    print("TEST_3_INTER_P:", m3_mod.pvalues["rd_x_jaffe"])
    print("TEST_3_CRIT_THRESHOLD:", crit_threshold)

    print("TEST_4_TWFE_B:", m4_twfe.params["jaffe:log_rd_lag2"])
    print("TEST_4_TWFE_SE:", m4_twfe.bse["jaffe:log_rd_lag2"])
    print("TEST_4_TWFE_P:", m4_twfe.pvalues["jaffe:log_rd_lag2"])

    print("TEST_5_DID_B:", m5_did.params["did_2016"])
    print("TEST_5_DID_SE:", m5_did.bse["did_2016"])
    print("TEST_5_DID_P:", m5_did.pvalues["did_2016"])

    print("TEST_6_PLACEBO_B:", m6_pl.params["placebo_did"])
    print("TEST_6_PLACEBO_SE:", m6_pl.bse["placebo_did"])
    print("TEST_6_PLACEBO_P:", m6_pl.pvalues["placebo_did"])

if __name__ == "__main__":
    main()
