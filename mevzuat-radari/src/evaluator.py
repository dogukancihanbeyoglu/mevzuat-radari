"""
AI and Rules-based Regulatory Relevance and Internal Audit Evaluator Module.
Matches Gazette items against Company Profile and produces structured audit evaluations.
"""
import os
import re
from datetime import datetime
from typing import List, Tuple, Optional
import yaml

from .models import (
    CompanyProfile,
    GazetteItem,
    GazetteIndex,
    AuditEvaluation,
    DailyAuditReport,
)
from .scraper import fetch_gazette_index, fetch_regulation_content


def load_company_profile(profile_path: str = "config/company_profile.yaml") -> CompanyProfile:
    """Loads and validates company profile from YAML file."""
    if not os.path.isabs(profile_path):
        # Resolve relative to project root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        profile_path = os.path.join(base_dir, profile_path)

    if not os.path.exists(profile_path):
        raise FileNotFoundError(f"Şirket profili bulunamadı: {profile_path}")

    with open(profile_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if "company_profile" in data:
        data = data["company_profile"]

    return CompanyProfile(**data)


def score_item_relevance(item: GazetteItem, profile: CompanyProfile) -> Tuple[int, List[str], str]:
    """
    Computes a relevance score (0-100) between a GazetteItem and CompanyProfile.
    Returns (score, matched_reasons, risk_level).
    """
    score = 0
    reasons = []
    title_lower = item.title.lower()
    institution = (item.institution or "").lower()

    # 1. Check High Priority Keywords
    for kw in profile.keywords.high_priority:
        if kw.lower() in title_lower:
            score += 35
            reasons.append(f"Yüksek öncelikli anahtar kelime eşleşmesi: '{kw}'")

    # 2. Check Medium Priority Keywords
    for kw in profile.keywords.medium_priority:
        if kw.lower() in title_lower:
            score += 15
            reasons.append(f"Orta öncelikli anahtar kelime eşleşmesi: '{kw}'")

    # 3. Check Regulatory Bodies Match
    for reg in profile.regulatory_bodies:
        reg_lower = reg.lower()
        if reg_lower in title_lower or (institution and reg_lower in institution):
            score += 30
            reasons.append(f"Düzenleyici kurum yetki alanı eşleşmesi: '{reg}'")

    # 4. Check Operational Traits
    if profile.operational_traits.e_commerce_license:
        if any(term in title_lower for term in ["e-ticaret", "mesafeli", "elektronik ticaret", "etbis", "tüketici"]):
            score += 25
            reasons.append("Şirketin E-Ticaret faaliyeti ve ETBİS lisansı ile doğrudan ilgili")

    if profile.operational_traits.has_foreign_trade:
        if any(term in title_lower for term in ["gümrük", "ithalat", "ihracat", "kambiyo", "dış ticaret"]):
            score += 25
            reasons.append("Şirketin Dış Ticaret (İthalat/İhracat) operasyonlarını ilgilendiriyor")

    if profile.operational_traits.has_rd_center:
        if any(term in title_lower for term in ["ar-ge", "teknoloji geliştirme", "5746", "tekrokent", "tübitak"]):
            score += 25
            reasons.append("Şirketin Ar-Ge Merkezi ve Teşvik mevzuatı ile ilgili")

    # 5. Check Sector / NACE alignment
    if "fintek" in profile.sectors_and_nace.primary_sector.lower() or any("fintek" in s.lower() for s in profile.sectors_and_nace.secondary_sectors):
        if any(term in title_lower for term in ["ödeme", "elektronik para", "tcmb", "bddk", "finansal kiralama", "masak"]):
            score += 30
            reasons.append("Finansal teknolojiler ve ödeme sistemleri sektörü ile doğrudan ilgili")

    # Cap score at 100
    final_score = min(score, 100)

    # Determine Risk Level
    if final_score >= 75:
        risk_level = "Kritik"
    elif final_score >= 55:
        risk_level = "Yüksek"
    elif final_score >= 35:
        risk_level = "Orta"
    elif final_score > 0:
        risk_level = "Düşük"
    else:
        risk_level = "Bilgi"

    return final_score, reasons, risk_level


def infer_affected_departments(title: str, matched_reasons: List[str]) -> List[str]:
    """Infers internal company departments affected by the regulation."""
    t = title.lower()
    deps = set()

    if any(k in t for k in ["vergi", "kdv", "matrah", "fatura", "harç", "muhasebe", "mali"]):
        deps.add("Mali İşler & Muhasebe")
    if any(k in t for k in ["iş kanunu", "asgari ücret", "sgk", "kıdem", "izin", "istihdam", "işçi"]):
        deps.add("İnsan Kaynakları")
    if any(k in t for k in ["kişisel veri", "kvkk", "verbis", "bilgi güvenliği", "siber", "yazılım"]):
        deps.add("Bilgi Teknolojileri (IT)")
        deps.add("Hukuk & Uyum")
    if any(k in t for k in ["e-ticaret", "mesafeli", "tüketici", "etbis", "müşteri", "cayma"]):
        deps.add("E-Ticaret Operasyon")
        deps.add("Müşteri Hizmetleri")
        deps.add("Hukuk & Uyum")
    if any(k in t for k in ["gümrük", "ithalat", "ihracat", "kambiyo", "lojistik", "kargo"]):
        deps.add("Tedarik Zinciri & Lojistik")
        deps.add("Dış Ticaret")
    if any(k in t for k in ["ödeme", "elektronik para", "tcmb", "bddk", "fintek", "masak"]):
        deps.add("Uyum (Compliance)")
        deps.add("Risk Yönetimi")
        deps.add("Finans")

    if not deps:
        deps.add("Hukuk & Uyum")
        deps.add("İç Denetim")

    return sorted(list(deps))


def generate_action_checklist(title: str, category: str, risk_level: str) -> List[str]:
    """Generates practical internal audit checklist items."""
    checklist = []
    t = title.lower()

    if "yönetmelik" in t or category.lower() == "yönetmelik":
        checklist.append("İlgili şirket içi prosedür ve yönetmelik dokümanlarının revize edilmesi.")
        checklist.append("Mevcut iş süreçlerinin yeni mevzuat maddeleri ile GAP (fark) analizinin yapılması.")
    elif "tebliğ" in t or category.lower() == "tebliğ":
        checklist.append("Uygulama esaslarının operasyonel ekiplere duyurulması ve eğitim planlanması.")

    if any(k in t for k in ["vergi", "kdv", "fatura"]):
        checklist.append("ERP ve muhasebe parametrelerinin/oranlarının sistemde güncellenmesi.")
        checklist.append("Mali müşavir / Vergi danışmanı görüşü alınarak beyanname kontrollerinin yapılması.")

    if any(k in t for k in ["mesafeli", "tüketici", "e-ticaret"]):
        checklist.append("Web/Mobil platformlardaki sözleşme ve ön bilgilendirme metinlerinin güncellenmesi.")
        checklist.append("İade ve cayma süreçlerinin sistemsel ve operasyonel olarak test edilmesi.")

    if any(k in t for k in ["kvkk", "kişisel veri"]):
        checklist.append("Veri envanteri ve aydınlatma metinlerinin uyumluluğunun denetlenmesi.")

    checklist.append(f"İç Denetim Uyum Takvimine {datetime.now().strftime('%Y-%m')} dönemi takip görevi olarak eklenmesi.")
    return checklist


def evaluate_gazette_item(item: GazetteItem, profile: CompanyProfile, content: Optional[str] = None) -> AuditEvaluation:
    """Constructs a complete AuditEvaluation for a single item."""
    score, reasons, risk_level = score_item_relevance(item, profile)
    affected_deps = infer_affected_departments(item.title, reasons)
    checklist = generate_action_checklist(item.title, item.category, risk_level)

    # Executive Summary logic
    doc_info = f" ({item.doc_number})" if item.doc_number else ""
    institution_info = f" ({item.institution})" if item.institution else ""
    summary = f"{item.category}{institution_info} kapsamındaki '{item.title}' düzenlemesi yayımlanmıştır.{doc_info} Düzenleme şirketin tabi olduğu regülasyonlar ve operasyonel süreçleri açısından doğrudan etki doğurmaktadır."

    penalty_risk = None
    if risk_level in ("Kritik", "Yüksek"):
        penalty_risk = "Uyumsuzluk veya gecikme durumunda ilgili kanun ve yönetmelikler uyarınca idari para cezası, faaliyet durdurma veya itibar riski bulunmaktadır."

    # Parse effective date if found in content or title
    effective_date = "Yayımı tarihinde"
    if content:
        date_match = re.search(r"(\d{1,2}/\d{1,2}/\d{4})\s+tarihinde\s+yürürlüğe\s+girer", content, re.IGNORECASE)
        if date_match:
            effective_date = date_match.group(1)

    return AuditEvaluation(
        item=item,
        relevance_score=score,
        risk_level=risk_level,
        matched_reasons=reasons,
        executive_summary=summary,
        penalty_and_legal_risk=penalty_risk,
        affected_departments=affected_deps,
        action_checklist=checklist,
        effective_date=effective_date,
    )


def generate_daily_audit_report(
    date_str: Optional[str] = None,
    min_score: int = 30,
    profile_path: str = "config/company_profile.yaml",
) -> DailyAuditReport:
    """
    Main pipeline: Scrapes Gazette index, evaluates against company profile,
    fetches detail content for relevant items, and generates structured report.
    """
    profile = load_company_profile(profile_path)
    index = fetch_gazette_index(date_str)

    evaluations: List[AuditEvaluation] = []
    for item in index.items:
        score, _, _ = score_item_relevance(item, profile)
        if score >= min_score:
            content = None
            if not item.is_pdf:
                try:
                    content = fetch_regulation_content(item.url)
                except Exception:
                    content = None
            eval_res = evaluate_gazette_item(item, profile, content)
            evaluations.append(eval_res)

    # Sort evaluations by relevance_score descending
    evaluations.sort(key=lambda x: x.relevance_score, reverse=True)

    return DailyAuditReport(
        date=index.date,
        gazette_number=index.gazette_number,
        company_name=profile.general.name,
        total_scanned=index.total_items,
        relevant_count=len(evaluations),
        evaluations=evaluations,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
