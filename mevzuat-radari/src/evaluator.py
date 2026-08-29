"""
AI and Rules-based Regulatory Relevance and Internal Audit Evaluator Module.
Features Advanced Contextual Rule-Based Engine:
- Negative Keyword Exclusion Filters (suppresses academic, student, municipal false positives)
- Strict Word-boundary Regex Matching (avoids substring false triggers like 'cihaz' matching 'iha')
- Context & Entity Routing (distinguishes commercial/defense regulations from academic university rules)
- Live GenAI LLM reasoning integration with graceful fallback
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
from .scraper import fetch_gazette_index, fetch_gazette_date_range, fetch_regulation_content
from .llm_engine import call_llm_evaluation
from .utils import lower_tr


def load_company_profile(profile_path: str = "config/company_profile.yaml") -> CompanyProfile:
    """Loads and validates company profile from YAML file."""
    if not os.path.isabs(profile_path):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        profile_path = os.path.join(base_dir, profile_path)

    if not os.path.exists(profile_path):
        raise FileNotFoundError(f"Şirket profili bulunamadı: {profile_path}")

    with open(profile_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if "company_profile" in data:
        data = data["company_profile"]

    return CompanyProfile(**data)


def _contains_term(text: str, term: str) -> bool:
    """Checks if a term matches either as a phrase or with word boundaries for short acronyms."""
    term_lower = lower_tr(term.strip())
    if not term_lower:
        return False
    if len(term_lower) <= 4:
        pattern = rf"\b{re.escape(term_lower)}\b"
        return bool(re.search(pattern, text))
    return term_lower in text


def score_item_relevance(item: GazetteItem, profile: CompanyProfile) -> Tuple[int, List[str], str]:
    """
    Computes an advanced contextual relevance score (0-100) between a GazetteItem and CompanyProfile.
    Employs negative filtering, regex word boundaries, and institutional context routing.
    Returns (score, matched_reasons, risk_level).
    """
    title_lower = lower_tr(item.title)
    institution_lower = lower_tr(item.institution or "")
    category_lower = lower_tr(item.category or "")
    combined_text = f"{title_lower} {institution_lower} {category_lower}"

    # 1. NEGATIVE EXCLUSION FILTER (Academic, Student, Medical, Municipal, Routine Appointments)
    excluded_matches = [
        exc for exc in profile.keywords.excluded 
        if _contains_term(title_lower, exc) or _contains_term(institution_lower, exc)
    ]
    
    # Overriding commercial/technological keywords (if present, allow evaluation)
    commercial_override = any(
        _contains_term(title_lower, term) 
        for term in ["teknoloji geliştirme bölgesi", "tgb", "savunma sanayii", "askeri yasak bölge", "harp aracı", "ihracat kontrol", "5201", "5202", "ihale", "tedarik"]
    )

    if excluded_matches and not commercial_override:
        return 0, [], "Bilgi"

    # Suppress pure university academic/internal regulations
    if "üniversite" in combined_text and not commercial_override:
        academic_terms = ["eğitim", "öğretim", "sınav", "lisans", "enstitü", "fakülte", "disiplin", "burs", "yurt", "kayıt", "öğrenci", "akademik", "öğretim elemanı"]
        if any(_contains_term(title_lower, term) for term in academic_terms):
            return 0, [], "Bilgi"

    # Suppress generic non-defense public appointments and routine personnel lists
    if "atama kararları" in category_lower or "atama kararı" in title_lower:
        if not any(_contains_term(title_lower, term) for term in ["savunma sanayii başkanlığı", "ssb", "milli savunma bakanlığı", "msb"]):
            return 0, [], "Bilgi"

    score = 0
    reasons = []

    # 2. HIGH PRIORITY KEYWORDS
    for kw in profile.keywords.high_priority:
        if _contains_term(title_lower, kw):
            score += 35
            reasons.append(f"Yüksek öncelikli anahtar kelime eşleşmesi: '{kw}'")

    # 3. MEDIUM PRIORITY KEYWORDS
    for kw in profile.keywords.medium_priority:
        if _contains_term(title_lower, kw):
            score += 15
            reasons.append(f"Orta öncelikli anahtar kelime eşleşmesi: '{kw}'")

    # 4. REGULATORY BODIES MATCH
    for reg in profile.regulatory_bodies:
        if _contains_term(title_lower, reg) or (institution_lower and _contains_term(institution_lower, reg)):
            score += 30
            reasons.append(f"Düzenleyici kurum yetki alanı eşleşmesi: '{reg}'")

    # 5. OPERATIONAL TRAITS MATCH
    if profile.operational_traits.has_rd_center:
        if any(_contains_term(title_lower, term) for term in ["ar-ge", "teknoloji geliştirme", "tgb", "5746", "teknokent", "tübitak"]):
            score += 30
            reasons.append("Şirketin Ar-Ge Merkezi ve Teknoloji Geliştirme Bölgesi faaliyetleri ile doğrudan ilgili")

    if profile.operational_traits.has_foreign_trade:
        if any(_contains_term(title_lower, term) for term in ["gümrük", "ithalat", "ihracat", "kambiyo", "askeri ihracat", "stratejik malzeme"]):
            score += 25
            reasons.append("Şirketin İhracat/İthalat ve Savunma Malzemesi Dolaşım operasyonlarını ilgilendiriyor")

    if profile.operational_traits.e_commerce_license:
        if any(_contains_term(title_lower, term) for term in ["e-ticaret", "mesafeli", "elektronik ticaret", "etbis", "tüketici"]):
            score += 25
            reasons.append("Şirketin E-Ticaret faaliyeti ve ETBİS lisansı ile ilgili")

    # 6. SECTOR & NACE ALIGNMENT
    primary_sec = lower_tr(profile.sectors_and_nace.primary_sector)
    if "savunma" in primary_sec or "askeri" in primary_sec:
        defense_indicators = ["milli savunma", "savunma sanayii", "askeri", "askeri yasak bölge", "harp", "denizaltı", "iha", "5201", "5202"]
        if any(_contains_term(title_lower, term) for term in defense_indicators):
            score += 35
            reasons.append("Savunma Sanayii, Askeri Projeler ve Güvenlik regülasyonları ile doğrudan ilgili")

    # If no core contextual reason was found, suppress false alarm
    if not reasons:
        return 0, [], "Bilgi"

    # Cap score at 100
    final_score = min(score, 100)

    # Determine Risk Level
    if final_score >= 70:
        risk_level = "Kritik"
    elif final_score >= 50:
        risk_level = "Yüksek"
    elif final_score >= 30:
        risk_level = "Orta"
    elif final_score > 0:
        risk_level = "Düşük"
    else:
        risk_level = "Bilgi"

    return final_score, reasons, risk_level


def infer_affected_departments(title: str, matched_reasons: List[str]) -> List[str]:
    """Infers internal company departments affected by the regulation."""
    t = lower_tr(title)
    deps = set()

    if any(_contains_term(t, k) for k in ["milli savunma", "askeri", "savunma", "harp", "deniz", "iha"]):
        deps.add("Savunma Projeleri Yönetimi")
        deps.add("Mühendislik & Sistem Entegrasyonu")
    if any(_contains_term(t, k) for k in ["yasak bölge", "tesis güvenlik", "güvenlik", "istihbarat", "gizli"]):
        deps.add("Tesis Güvenlik Koordinatörlüğü")
        deps.add("İdari İşler & Güvenlik")
    if any(_contains_term(t, k) for k in ["teknoloji geliştirme", "teknoloji", "ar-ge", "teknokent", "5746"]):
        deps.add("Ar-Ge & Teknoloji Yönetimi")
        deps.add("Teşvik ve Fon Yönetimi")
    if any(_contains_term(t, k) for k in ["siber", "bilgi sistem", "yazılım", "usom", "btk"]):
        deps.add("Siber Güvenlik Operasyon Merkezi (SOC)")
        deps.add("Bilgi Teknolojileri (IT)")
    if any(_contains_term(t, k) for k in ["ihracat", "ithalat", "gümrük", "5201", "5202", "kontrole tabi"]):
        deps.add("İhracat & Lojistik Operasyonları")
        deps.add("Sözleşmeler & İhracat Kontrol")
    if any(_contains_term(t, k) for k in ["vergi", "kdv", "fatura", "ssdf", "muhasebe", "mali"]):
        deps.add("Mali İşler & Muhasebe")
    if any(_contains_term(t, k) for k in ["iş kanunu", "asgari ücret", "sgk", "istihdam", "işçi"]):
        deps.add("İnsan Kaynakları")

    if not deps:
        deps.add("Hukuk & Uyum")
        deps.add("İç Denetim Başkanlığı")
    else:
        deps.add("Hukuk & Sözleşmeler")
        deps.add("İç Denetim Başkanlığı")

    return sorted(list(deps))


def generate_action_checklist(title: str, category: str, risk_level: str) -> List[str]:
    """Generates practical internal audit checklist items."""
    checklist = []
    t = lower_tr(title)

    if "teknoloji geliştirme" in t or "ar-ge" in t:
        checklist.append("Teknoloji Geliştirme Bölgesi (TGB) kapsamındaki Ar-Ge projelerinin ve teşvik şartlarının gözden geçirilmesi.")
        checklist.append("Üniversite-Sanayi iş birliği ve yeni teknopark alanında tesis/ofis tahsis imkanlarının değerlendirilmesi.")

    if "askeri yasak bölge" in t or "yasak bölge" in t:
        checklist.append("Şirketin operasyon, saha testleri ve uçuş/seyir izin protokollerinin askeri bölge sınırları doğrultusunda güncellenmesi.")
        checklist.append("Tesis ve Saha Güvenliği Prosedürlerinin Askeri Yasak Bölgeler mevzuatına uyumunun denetlenmesi.")

    if "yönetmelik" in t or (category and "yönetmelik" in lower_tr(category)):
        checklist.append("Şirket içi ilgili yönerge ve süreç dokümanlarının revize edilmesi.")
        checklist.append("Mevcut iş süreçlerinin yeni mevzuat maddeleri ile GAP (fark) analizinin yapılması.")

    if any(_contains_term(t, k) for k in ["ihracat", "5201", "5202"]):
        checklist.append("MSB ve SSB izin prosedürlerinin ihracat kontrol listeleriyle doğrulanması.")

    if any(_contains_term(t, k) for k in ["vergi", "kdv", "fatura", "ssdf"]):
        checklist.append("ERP ve muhasebe parametrelerinin/oranlarının sistemde güncellenmesi.")
        checklist.append("Vergi danışmanı görüşü alınarak beyanname ve fon kontrollerinin yapılması.")

    checklist.append(f"İç Denetim Uyum Takvimine {datetime.now().strftime('%Y-%m')} dönemi periyodik kontrol adımı olarak eklenmesi.")
    return checklist


def evaluate_gazette_item(item: GazetteItem, profile: CompanyProfile, content: Optional[str] = None) -> AuditEvaluation:
    """
    Constructs a complete AuditEvaluation for a single item.
    Leverages live LLM analysis if configured; otherwise uses deterministic local heuristics.
    """
    llm_res = call_llm_evaluation(
        title=item.title,
        category=item.category,
        institution=item.institution,
        raw_content=content,
        company_profile_dict=profile.model_dump(),
    )

    if llm_res and isinstance(llm_res, dict) and "relevance_score" in llm_res:
        score = int(llm_res.get("relevance_score", 0))
        risk_level = str(llm_res.get("risk_level", "Orta"))
        matched_reasons = list(llm_res.get("matched_reasons", []))
        summary = str(llm_res.get("executive_summary", ""))
        penalty_risk = llm_res.get("penalty_and_legal_risk")
        affected_deps = list(llm_res.get("affected_departments", []))
        checklist = list(llm_res.get("action_checklist", []))
    else:
        score, matched_reasons, risk_level = score_item_relevance(item, profile)
        affected_deps = infer_affected_departments(item.title, matched_reasons)
        checklist = generate_action_checklist(item.title, item.category, risk_level)

        doc_info = f" ({item.doc_number})" if item.doc_number else ""
        institution_info = f" ({item.institution})" if item.institution else ""
        summary = f"{item.category}{institution_info} kapsamındaki '{item.title}' düzenlemesi yayımlanmıştır.{doc_info} Düzenleme şirketin savunma sanayii, Ar-Ge ve askeri operasyonel süreçleri açısından doğrudan etki doğurmaktadır."

        penalty_risk = None
        if risk_level in ("Kritik", "Yüksek"):
            penalty_risk = "Milli Savunma / SSB mevzuatı, Tesis Güvenlik Belgesi gereksinimleri ve ilgili kanunlar uyarınca idari yaptırım, faaliyet kısıtı ve sözleşme fesih riski bulunmaktadır."

    effective_date = "Yayımı tarihinde"
    if content:
        date_match = re.search(r"(\d{1,2}/\d{1,2}/\d{4})\s+tarihinde\s+yürürlüğe\s+girer", content, re.IGNORECASE)
        if date_match:
            effective_date = date_match.group(1)

    return AuditEvaluation(
        item=item,
        relevance_score=score,
        risk_level=risk_level,
        matched_reasons=matched_reasons,
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
    Main pipeline for a single date: Scrapes Gazette index, evaluates against company profile,
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


def generate_range_audit_report(
    start_date: str,
    end_date: str,
    min_score: int = 30,
    profile_path: str = "config/company_profile.yaml",
) -> DailyAuditReport:
    """
    Date Range pipeline: Scrapes Gazette indices across [start_date, end_date],
    evaluates all items against company profile, and aggregates into a combined report.
    """
    profile = load_company_profile(profile_path)
    indices = fetch_gazette_date_range(start_date, end_date)

    total_scanned = sum(idx.total_items for idx in indices)
    evaluations: List[AuditEvaluation] = []

    for idx in indices:
        for item in idx.items:
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

    evaluations.sort(key=lambda x: x.relevance_score, reverse=True)

    range_label = f"{start_date} - {end_date}"
    return DailyAuditReport(
        date=range_label,
        gazette_number=f"{len(indices)} Sayı Taranmıştır",
        company_name=profile.general.name,
        total_scanned=total_scanned,
        relevant_count=len(evaluations),
        evaluations=evaluations,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
