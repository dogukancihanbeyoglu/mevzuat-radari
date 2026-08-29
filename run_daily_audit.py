#!/usr/bin/env python3
"""
CLI Runner for Mevzuat Radarı.
Executes audit pipeline for a single date or date range, generates reports and dispatches emails.
Usage:
    # Single Date:
    python run_daily_audit.py [--date YYYY-MM-DD] [--email denetim@stm.com.tr]
    
    # Date Range (Batch / Archive):
    python run_daily_audit.py --start-date 2026-08-01 --end-date 2026-08-29
"""
import os
import sys
import argparse
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.evaluator import generate_daily_audit_report, generate_range_audit_report
from src.templates import format_markdown_report, format_html_report
from src.pdf_generator import generate_pdf_report
from src.notifier import EmailNotifier


def main():
    parser = argparse.ArgumentParser(description="Resmî Gazete İç Denetim & Uyum Radarı")
    parser.add_argument("--date", type=str, default=None, help="Taranacak tek tarih (YYYY-MM-DD)")
    parser.add_argument("--start-date", type=str, default=None, help="Aralık taraması başlangıç tarihi (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, default=None, help="Aralık taraması bitiş tarihi (YYYY-MM-DD)")
    parser.add_argument("--min-score", type=int, default=30, help="Raporlanacak minimum alaka skoru (0-100, varsayılan: 30)")
    parser.add_argument("--profile", type=str, default="config/company_profile.yaml", help="Şirket profili YAML dosyası")
    parser.add_argument("--email", type=str, default=None, help="PDF raporunun gönderileceği e-posta adresleri (virgülle ayrılmış)")
    parser.add_argument("--no-save", action="store_true", help="Raporları diske kaydetme")

    args = parser.parse_args()

    print("================================================================")
    print("🏛️  Resmî Gazete İç Denetim & Uyum Radarı Başlatılıyor...")
    if args.start_date and args.end_date:
        print(f"📌 Tarama Modu: Tarih Aralığı ({args.start_date} → {args.end_date})")
    else:
        print(f"📌 Tarama Modu: Tek Tarih ({args.date or 'Bugün'})")
    print(f"📌 Minimum Alaka Eşiği: %{args.min_score}")
    print("================================================================")

    try:
        if args.start_date and args.end_date:
            report = generate_range_audit_report(
                start_date=args.start_date,
                end_date=args.end_date,
                min_score=args.min_score,
                profile_path=args.profile,
            )
        else:
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

        pdf_path = None
        if not args.no_save:
            reports_dir = os.path.join(current_dir, "reports")
            os.makedirs(reports_dir, exist_ok=True)
            
            clean_date = report.date.replace("/", "-").replace(".", "-").replace(" ", "_")
            md_path = os.path.join(reports_dir, f"{clean_date}.md")
            html_path = os.path.join(reports_dir, f"{clean_date}.html")
            pdf_path = os.path.join(reports_dir, f"{clean_date}.pdf")

            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_output)

            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_output)

            generate_pdf_report(report, pdf_path)

            print(f"💾 Markdown Raporu: {md_path}")
            print(f"💾 HTML Bülteni: {html_path}")
            print(f"💾 PDF Bülteni: {pdf_path}")

        # Dispatch Email if requested
        if args.email:
            recipients = [e.strip() for e in args.email.split(",") if e.strip()]
            print(f"\n📧 E-Posta Raporu Dağıtımı Başlatılıyor ({len(recipients)} alıcı)...")
            notifier = EmailNotifier()
            result = notifier.send_report_email(report, recipients, pdf_path=pdf_path)
            print(f"   ✓ Durum: {result.get('status')}")
            print(f"   ✓ Mod: {result.get('mode')}")
            print(f"   ✓ Mesaj: {result.get('message')}")

        print("\n" + "="*50)
        print("📋 RAPOR ÖZETİ")
        print("="*50)
        print(md_output)

    except Exception as e:
        print(f"❌ Hata oluştu: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
