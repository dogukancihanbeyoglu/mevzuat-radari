"""
Email and Periodic Notification Dispatcher Module for Mevzuat Radarı.
Sends daily audit reports with PDF attachments to configured or requested recipients.
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import List, Optional, Dict, Any

from .models import DailyAuditReport
from .pdf_generator import generate_pdf_report
from .templates import format_html_report, format_markdown_report


class EmailNotifier:
    """Handles sending email reports with PDF attachments."""

    def __init__(
        self,
        smtp_host: Optional[str] = None,
        smtp_port: int = 587,
        smtp_user: Optional[str] = None,
        smtp_password: Optional[str] = None,
        sender_email: Optional[str] = None,
        use_tls: bool = True,
    ):
        self.smtp_host = smtp_host or os.environ.get("SMTP_HOST")
        self.smtp_port = int(os.environ.get("SMTP_PORT", smtp_port))
        self.smtp_user = smtp_user or os.environ.get("SMTP_USER")
        self.smtp_password = smtp_password or os.environ.get("SMTP_PASSWORD")
        self.sender_email = sender_email or os.environ.get("SMTP_SENDER", "mevzuat-radari@sirket.com")
        self.use_tls = use_tls

    def send_report_email(
        self,
        report: DailyAuditReport,
        recipient_emails: List[str],
        pdf_path: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Sends the audit report to recipient_emails with PDF attachment.
        If SMTP server is not configured, performs a safe simulation (dry-run) and saves the PDF.
        """
        if not recipient_emails:
            raise ValueError("En az bir alıcı e-posta adresi belirtilmelidir.")

        # Ensure PDF exists
        if not pdf_path or not os.path.exists(pdf_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            reports_dir = os.path.join(base_dir, "reports")
            clean_date = report.date.replace("/", "-").replace(".", "-")
            pdf_path = os.path.join(reports_dir, f"{clean_date}.pdf")
            generate_pdf_report(report, pdf_path)

        subject = f"🏛️ Resmî Gazete İç Denetim & Uyum Bülteni - {report.date} ({report.company_name})"
        html_body = format_html_report(report)

        # Check if live SMTP credentials exist
        if not self.smtp_host or not self.smtp_user:
            # Safe Dry-Run Mode
            return {
                "status": "success (dry-run)",
                "mode": "Simülasyon (SMTP bilgileri .env içinde tanımlanmadığı için rapor hazırlandı)",
                "recipients": recipient_emails,
                "subject": subject,
                "pdf_path": os.path.abspath(pdf_path),
                "pdf_size_bytes": os.path.getsize(pdf_path),
                "message": f"PDF başarıyla üretildi ({os.path.basename(pdf_path)}) ve {len(recipient_emails)} alıcıya gönderim simüle edildi.",
            }

        # Build real MIME message
        msg = MIMEMultipart("mixed")
        msg["From"] = self.sender_email
        msg["To"] = ", ".join(recipient_emails)
        msg["Subject"] = subject

        # HTML Part
        html_part = MIMEText(html_body, "html", "utf-8")
        msg.attach(html_part)

        # PDF Attachment
        with open(pdf_path, "rb") as f:
            pdf_attach = MIMEApplication(f.read(), _subtype="pdf")
            pdf_attach.add_header(
                "Content-Disposition",
                "attachment",
                filename=f"Mevzuat_Denetim_Bulteni_{report.date}.pdf",
            )
            msg.attach(pdf_attach)

        # Send via SMTP
        with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=20) as server:
            if self.use_tls:
                server.starttls()
            if self.smtp_user and self.smtp_password:
                server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.sender_email, recipient_emails, msg.as_string())

        return {
            "status": "success",
            "mode": "Live SMTP",
            "recipients": recipient_emails,
            "subject": subject,
            "pdf_path": os.path.abspath(pdf_path),
            "message": f"Rapor PDF ekiyle birlikte başarıyla {', '.join(recipient_emails)} adreslerine gönderildi.",
        }


def dispatch_daily_audit_pdf(
    recipient_emails: List[str],
    date_str: Optional[str] = None,
    min_score: int = 30,
    profile_path: str = "config/company_profile.yaml",
) -> Dict[str, Any]:
    """Helper function to run evaluation, generate PDF, and dispatch email."""
    from .evaluator import generate_daily_audit_report

    report = generate_daily_audit_report(
        date_str=date_str,
        min_score=min_score,
        profile_path=profile_path,
    )
    notifier = EmailNotifier()
    return notifier.send_report_email(report, recipient_emails)
