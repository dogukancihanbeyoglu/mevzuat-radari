#!/usr/bin/env python3
"""
CLI Runner for Mevzuat Radarı.
Executes daily audit pipeline, generates reports and saves them to reports/ directory.
Usage:
    python run_daily_audit.py [--date YYYY-MM-DD] [--min-score 30] [--profile config/company_profile.yaml]
"""
import os
import sys
import argparse
from datetime import datetime

# Add package directory to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.evaluator import generate_daily_audit_report
from src.templates import format_markdown_report, format_html_report


def main():
    parser = argparse.ArgumentParser(description="Resmî Gazete İç Denetim & Uyum Radarı")
    parser.add_argument("--date", type=str, default=None, help="Taranacak tarih (YYYY-MM-DD veya DD.MM.YYYY, varsayılan: bugün)")
    parser.add_argument("--min-score", type=int, default=30, help="Raporlanacak minimum alaka skoru (0-100, varsayılan: 30)")
    parser.add_argument("--profile", type=str, default="config/company_profile.yaml", help="Şirket profili YAML dosyası yolu")
    parser.add_argument("--no-save", action="store_true", help="Raporları diske kaydetme, sadece ekrana bas")

    args = parser.parse_args()

    print("================================================================")
    print("🏛️  Resmî Gazete İç Denetim & Uyum Radarı Başlatılıyor...")
    print(f"📌 Tarih: {args.date or 'Bugün'}")
    print(f"📌 Minimum Alaka Eşiği: %{args.min_score}")
    print("================================================================")

    try:
        report = generate_daily_audit_report(
            date_str=args.date,
            min_score=args.min_score,
            profile_path=args.profile,
        )

        md_output = format_markdown_report(report)
        html_output = format_html_report(report)

        print(f"\n✅ Tarama Tamamlandı!")
        print(f"📊 Şirket: {report.company_name}")
        print(f"📄 Toplam Taranan Madde: {report.total_scanned}")
        print(f"🎯 İlgili / Aksiyon Gerektiren Karar Sayısı: {report.relevant_count}\n")

        # Save to reports directory if requested
        if not args.no_save:
            reports_dir = os.path.join(current_dir, "reports")
            os.makedirs(reports_dir, exist_ok=True)
            
            clean_date = report.date.replace("/", "-").replace(".", "-")
            md_path = os.path.join(reports_dir, f"{clean_date}.md")
            html_path = os.path.join(reports_dir, f"{clean_date}.html")

            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_output)

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_output)

            print(f"💾 Markdown Raporu Kaydedildi: {md_path}")
            print(f"💾 HTML Bülteni Kaydedildi: {html_path}")

        print("\n" + "="*50)
        print("📋 RAPOR ÖZETİ")
        print("="*50)
        print(md_output)

    except Exception as e:
        print(f"❌ Hata oluştu: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
