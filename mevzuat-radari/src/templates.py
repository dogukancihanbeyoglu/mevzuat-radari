"""
Report Template Generator Module for Mevzuat Radarı.
Formats DailyAuditReport into clean Markdown and responsive HTML bulletins.
"""
from .models import DailyAuditReport


def format_markdown_report(report: DailyAuditReport) -> str:
    """Renders DailyAuditReport as a rich GitHub Flavored Markdown document."""
    lines = []
    lines.append(f"# 🏛️ Resmî Gazete İç Denetim & Uyum Bülteni")
    lines.append(f"**Şirket:** {report.company_name} | **Tarih:** {report.date} | **Sayı:** {report.gazette_number or 'Günlük Sayı'}")
    lines.append(f"**Taranan Toplam Madde:** {report.total_scanned} | **İlgili/Aksiyon Gerektiren Madde:** {report.relevant_count}")
    lines.append(f"*Rapor Oluşturma Zamanı: {report.generated_at}*")
    lines.append("\n---\n")

    if not report.evaluations:
        lines.append("### ℹ️ Bugün İçin Şirketi İlgilendiren Kritik Bir Karar Bulunmadı")
        lines.append("Şirket profilindeki sektör, NACE kodları ve düzenleyici kurum kriterlerine uyan öncelikli bir tebliğ/yönetmelik tespit edilmemiştir.")
        return "\n".join(lines)

    for i, ev in enumerate(report.evaluations, 1):
        badge = "🔴" if ev.risk_level == "Kritik" else ("🟠" if ev.risk_level == "Yüksek" else "🟡")
        lines.append(f"### {badge} {i}. [{ev.risk_level.upper()}] {ev.item.title}")
        lines.append(f"* **Kategori:** {ev.item.category} | **Bölüm:** {ev.item.section}")
        if ev.item.institution:
            lines.append(f"* **Düzenleyen Kurum:** {ev.item.institution}")
        lines.append(f"* **Alaka Skoru:** %{ev.relevance_score}")
        lines.append(f"* **Yürürlük Tarihi:** {ev.effective_date or 'Belirtilmemiş'}")
        lines.append(f"* **Kaynak Bağlantı:** [{ev.item.url}]({ev.item.url})")
        lines.append("")

        lines.append("#### 🎯 Eşleşme Gerekçeleri")
        for r in ev.matched_reasons:
            lines.append(f"- {r}")
        lines.append("")

        lines.append("#### 📝 Yönetici Özeti")
        lines.append(f"{ev.executive_summary}")
        lines.append("")

        if ev.penalty_and_legal_risk:
            lines.append("#### ⚠️ Yaptırım & Ceza Riski")
            lines.append(f"{ev.penalty_and_legal_risk}")
            lines.append("")

        if ev.affected_departments:
            lines.append("#### 🏢 Etkilenen Departmanlar")
            lines.append(", ".join([f"`{d}`" for d in ev.affected_departments]))
            lines.append("")

        if ev.action_checklist:
            lines.append("#### ✅ İç Denetim Aksiyon Kontrol Listesi")
            for chk in ev.action_checklist:
                lines.append(f"- [ ] {chk}")
            lines.append("")

        lines.append("\n---\n")

    return "\n".join(lines)


def format_html_report(report: DailyAuditReport) -> str:
    """Renders DailyAuditReport as a responsive, email-friendly HTML document."""
    items_html = ""
    for i, ev in enumerate(report.evaluations, 1):
        color = "#e53e3e" if ev.risk_level == "Kritik" else ("#dd6b20" if ev.risk_level == "Yüksek" else "#d69e2e")
        reasons_li = "".join([f"<li>{r}</li>" for r in ev.matched_reasons])
        deps_spans = " ".join([f"<span style='background:#edf2f7;padding:3px 8px;border-radius:4px;font-size:12px;margin-right:4px;'>{d}</span>" for d in ev.affected_departments])
        checklist_li = "".join([f"<li style='margin-bottom:4px;'>⬜ {chk}</li>" for chk in ev.action_checklist])

        items_html += f"""
        <div style="border: 1px solid #e2e8f0; border-left: 5px solid {color}; border-radius: 8px; padding: 18px; margin-bottom: 20px; background-color: #ffffff;">
            <h3 style="margin-top:0; color: #2d3748; font-size: 16px;">
                <span style="background:{color}; color:white; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-right: 6px;">{ev.risk_level}</span>
                {i}. {ev.item.title}
            </h3>
            <p style="color: #718096; font-size: 13px; margin: 4px 0;">
                <strong>Kategori:</strong> {ev.item.category} | <strong>Alaka:</strong> %{ev.relevance_score} | <strong>Yürürlük:</strong> {ev.effective_date or 'Yayımı tarihi'}
            </p>
            <div style="margin: 10px 0; font-size: 14px; line-height: 1.5; color: #4a5568;">
                <strong>Özet:</strong> {ev.executive_summary}
            </div>
            <div style="margin: 10px 0;">
                <strong>Etkilenen Departmanlar:</strong><br>{deps_spans}
            </div>
            <div style="margin-top: 12px; padding: 10px; background-color: #f7fafc; border-radius: 6px;">
                <strong style="color:#2b6cb0;">İç Denetim Aksiyon Listesi:</strong>
                <ul style="margin: 6px 0 0 0; padding-left: 20px; font-size: 13px; color: #2d3748; list-style: none;">
                    {checklist_li}
                </ul>
            </div>
            <p style="margin-top: 10px; font-size: 12px;">
                <a href="{ev.item.url}" target="_blank" style="color: #3182ce; text-decoration: none;">Resmî Gazete Kaynak Belgesini Görüntüle &rarr;</a>
            </p>
        </div>
        """

    if not report.evaluations:
        items_html = "<div style='padding: 20px; background: #ebf8ff; border-radius: 8px; color: #2b6cb0;'>Bugün şirket profilini ilgilendiren öncelikli bir karar yayımlanmamıştır.</div>"

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Resmî Gazete İç Denetim Bülteni - {report.date}</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; margin: 0; padding: 24px; color: #1a202c;">
    <div style="max-width: 800px; margin: 0 auto; background: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); padding: 28px;">
        <header style="border-bottom: 2px solid #edf2f7; padding-bottom: 16px; margin-bottom: 24px;">
            <h1 style="margin: 0; font-size: 22px; color: #1a365d;">🏛️ Resmî Gazete İç Denetim & Uyum Bülteni</h1>
            <p style="margin: 6px 0 0 0; color: #718096; font-size: 14px;">
                <strong>Şirket:</strong> {report.company_name} | <strong>Tarih:</strong> {report.date} | <strong>Sayı:</strong> {report.gazette_number or 'Günlük'}
            </p>
            <p style="margin: 4px 0 0 0; color: #a0aec0; font-size: 12px;">
                Taranan: {report.total_scanned} madde | İlgili: {report.relevant_count} karar | Oluşturuldu: {report.generated_at}
            </p>
        </header>
        <main>
            {items_html}
        </main>
        <footer style="margin-top: 30px; border-top: 1px solid #edf2f7; padding-top: 14px; text-align: center; font-size: 12px; color: #a0aec0;">
            Mevzuat Radarı (Resmî Gazete İç Denetim & Uyum Ajanı) tarafından otomatik oluşturulmuştur.
        </footer>
    </div>
</body>
</html>
"""
