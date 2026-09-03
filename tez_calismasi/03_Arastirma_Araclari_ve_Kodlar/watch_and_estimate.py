#!/usr/bin/env python3
"""
Watcher and Automated Estimator
Checks ~/Downloads for any newly downloaded BigQuery result CSV,
processes it into the econometric panel, and triggers run_econometric_estimation.py.
"""

import os
import glob
import time
import subprocess

DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
PANEL_OUTPUT = "/Users/dogukancihanbeyoglu/Desktop/AHBV_Iktisat_Tez_Calismasi/03_Arastirma_Araclari_ve_Kodlar/gercek_panel_verisi.csv"

def find_latest_download():
    # Look for files matching bqux*, bigquery*, or *.csv modified in the last 30 minutes
    csv_files = glob.glob(os.path.join(DOWNLOADS_DIR, "*.csv"))
    if not csv_files:
        return None
    latest_file = max(csv_files, key=os.path.getmtime)
    # Check if modified within the last 30 minutes
    if time.time() - os.path.getmtime(latest_file) < 1800:
        return latest_file
    return None

def main():
    print("=" * 80)
    print("BİGQUERY İNDİRME İZLEYİCİ VE OTOMATİK REGRESYON BORU HATTI")
    print(f"İzlenen Dizin: {DOWNLOADS_DIR}")
    print("=" * 80)

    target_csv = find_latest_download()
    if target_csv:
        print(f"[+] Yeni BigQuery CSV dosyası tespit edildi: {target_csv}")
        # 1. Process
        print("\n[*] 1. Adım: Ham veriyi panele çeviriliyor...")
        cmd_process = [
            "python3",
            "/Users/dogukancihanbeyoglu/Gemini/tools/process_real_patents.py",
            "--input_csv", target_csv,
            "--output_panel", PANEL_OUTPUT
        ]
        subprocess.run(cmd_process, check=True)

        # 2. Run Econometric Estimation
        print("\n[*] 2. Adım: Gerçek verilerle ekonometrik modeller koşturuluyor...")
        cmd_est = [
            "python3",
            "/Users/dogukancihanbeyoglu/Gemini/tools/run_econometric_estimation.py"
        ]
        subprocess.run(cmd_est, check=True)
        print("\n[✔] İŞLEM TAMAMLANDI! Gerçek ampirik katsayılar güncellendi.")
    else:
        print("[-] Henüz son 30 dakika içinde indirilmiş bir BigQuery CSV dosyası bulunamadı.")
        print("[i] BigQuery'de sorguyu çalıştırdıktan sonra 'Save Results -> CSV'ye basınız.")

if __name__ == "__main__":
    main()
