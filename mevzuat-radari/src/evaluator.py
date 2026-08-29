"""
AI and Rules-based Regulatory Relevance and Internal Audit Evaluator Module.
Features Universal Multi-Layered Compliance Matrix:
1. Vertical Sectoral Layer (Defense, Aviation, Maritime, Space, SSB, MSB, 5201/5202)
2. Horizontal Corporate Layer (Tax & Finance, Labor & HR, KVKK & Cyber, Public Procurement, Customs & Trade, Corporate Law)
3. Universal Public Noise Filter (suppresses academic/student/municipal noise)
4. Live GenAI LLM reasoning integration with graceful local fallback
"""
import os
import re
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any
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
from .sector_templates import (
    UNIVERSAL_NOISE_KEYWORDS,
    COMMERCIAL_OVERRIDE_TERMS,
    HORIZONTAL_CORPORATE_DOMAINS,
)


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


def score_item_relevance(item: GazetteItem, profile: CompanyProfile) -> Tuple[int, List[str], str, str, str]:
    """
    Computes multi-layered relevance score (0-100) across Vertical Sector and Horizontal Corporate domains.
    Returns (score, matched_reasons, risk_level, compliance_domain, domain_badge).
    """
    title_lower = lower_tr(item.title)
    institution_lower = lower_tr(item.institution or "")
    category_lower = lower_tr(item.category or "")
    combined_text = f"{title_lower} {institution_lower} {category_lower}"

    # 1. COMMERCIAL & SECTORAL OVERRIDE CHECK
    is_protected_from_noise = any(_contains_term(title_lower, term) for term in COMMERCIAL_OVERRIDE_TERMS)

    # 2. UNIVERSAL PUBLIC NOISE FILTER (If not protected by explicit commercial override)
    if not is_protected_from_noise:
        if any(_contains_term(title_lower, noise) for noise in UNIVERSAL_NOISE_KEYWORDS):
            return 0, [], "Bilgi", "Genel", "BİLGİ"

        if "üniversite" in combined_text:
            return 0, [], "Bilgi", "Genel", "BİLGİ"

        if "atama" in category_lower or "atama" in title_lower:
            reg_match = False
            for reg in profile.regulatory_bodies:
                reg_clean = re.sub(r"\(.*?\)", "", reg).strip()
                if _contains_term(title_lower, reg_clean):
                    reg_match = True
                    break
            if not reg_match:
                return 0, [], "Bilgi", "Genel", "BİLGİ"

    # 3. COMPANY-SPECIFIC NEGATIVE EXCLUSION FILTER
    if profile.keywords.excluded and not is_protected_from_noise:
        if any(_contains_term(title_lower, exc) or _contains_term(institution_lower, exc) for exc in profile.keywords.excluded):
            return 0, [], "Bilgi", "Genel", "BİLGİ"

    score = 0
    reasons = []
    detected_domain = "Sektörel Uyum"
    domain_badge = "SEKTÖREL"

    # =========================================================================
    # A. VERTICAL SECTOR LAYER (Savunma, Havacılık, NACE, Yetkili Kurumlar)
    # =========================================================================
    # High Priority Keywords
    for kw in profile.keywords.high_priority:
        if _contains_term(title_lower, kw):
            score += 35
            reasons.append(f"Yüksek öncelikli dikey sektörel anahtar kelime: '{kw}'")

    # Medium Priority Keywords
    for kw in profile.keywords.medium_priority:
        if _contains_term(title_lower, kw):
            score += 15
            reasons.append(f"Orta öncelikli sektörel anahtar kelime: '{kw}'")

    # Regulatory Bodies Jurisdiction (Match both full name and acronym in parens)
    for reg in profile.regulatory_bodies:
        reg_clean = re.sub(r"\(.*?\)", "", reg).strip()
        acronym_match = re.search(r"\((.*?)\)", reg)
        acronym = acronym_match.group(1).strip() if acronym_match else ""

        if _contains_term(title_lower, reg_clean) or (acronym and _contains_term(title_lower, acronym)) or \
           (institution_lower and (_contains_term(institution_lower, reg_clean) or (acronym and _contains_term(institution_lower, acronym)))):
            score += 30
            reasons.append(f"Tabi olunan yetkili düzenleyici kurum: '{reg}'")

    # Sector / NACE Alignment
    primary_sec = lower_tr(profile.sectors_and_nace.primary_sector)
    if "savunma" in primary_sec or "askeri" in primary_sec:
        defense_indicators = ["milli savunma", "savunma sanayii", "askeri", "askeri yasak bölge", "harp", "denizaltı", "iha", "5201", "5202", "milgem", "kargu"]
        if any(_contains_term(title_lower, term) for term in defense_indicators):
            score += 35
            reasons.append("Savunma Sanayii, Askeri Denizcilik ve Taktik İHA regülasyonları ile doğrudan ilgili")
            detected_domain = "Savunma Sanayii & Askeri Sistemler"
            domain_badge = "SAVUNMA & ASKERİ"

    # Operational Traits
    if profile.operational_traits.has_rd_center:
        if any(_contains_term(title_lower, term) for term in ["ar-ge", "teknoloji geliştirme", "tgb", "5746", "teknokent", "tübitak"]):
            score += 30
            reasons.append("Şirketin Ar-Ge Merkezi ve Teknoloji Geliştirme Bölgesi (TGB) operasyonlarını doğrudan ilgilendiriyor")
            if detected_domain == "Sektörel Uyum":
                detected_domain = "Ar-Ge & Teknoloji Teşvikleri"
                domain_badge = "AR-GE & TEKNOLOJİ"

    if profile.operational_traits.has_foreign_trade:
        if any(_contains_term(title_lower, term) for term in ["gümrük", "ithalat", "ihracat", "kambiyo", "askeri ihracat", "stratejik malzeme", "dış ticaret"]):
            score += 25
            reasons.append("Şirketin İthalat/İhracat ve Dış Ticaret operasyonlarını ilgilendiriyor")

    # =========================================================================
    # B. HORIZONTAL CORPORATE LAYER (Vergi, İş Hukuku, KVKK, İhale, Gümrük, Ticaret)
    # =========================================================================
    for dom_key, dom_data in HORIZONTAL_CORPORATE_DOMAINS.items():
        matched_kw = [k for k in dom_data["keywords"] if _contains_term(title_lower, k)]
        if matched_kw:
            h_score = 40
            if any(c in category_lower or c in title_lower for c in ["tebliğ", "yönetmelik", "karar", "kanun"]):
                h_score += 25
            score = max(score, h_score)
            
            reasons.append(f"Kurumsal Yatay Uyum [{dom_data['domain_name']}]: '{', '.join(matched_kw[:2])}' düzenlemesi")
            
            if detected_domain in ("Sektörel Uyum", "Genel"):
                detected_domain = dom_data["domain_name"]
                domain_badge = dom_data["badge_label"]

    # If no core reason was triggered, suppress
    if not reasons:
        return 0, [], "Bilgi", "Genel", "BİLGİ"

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

    return final_score, reasons, risk_level, detected_domain, domain_badge


def infer_affected_departments(title: str, matched_reasons: List[str], domain_badge: str = "SEKTÖREL") -> List[str]:
    """Infers internal company departments affected by the regulation across all corporate domains."""
    t = lower_tr(title)
    deps = set()

    # Domain specific additions
    if domain_badge == "VERGİ & MALİYE" or any(_contains_term(t, k) for k in ["vergi", "kdv", "fatura", "ssdf", "muhasebe", "mali", "tevkifat"]):
        deps.add("Mali İşler & Muhasebe")
        deps.add("Finansman & Bütçe")
    if domain_badge == "İŞ HUKUKU & İK" or any(_contains_term(t, k) for k in ["iş kanunu", "asgari ücret", "sgk", "istihdam", "işçi", "isg", "tazminat"]):
        deps.add("İnsan Kaynakları")
        deps.add("Bordro & Özlük İşleri")
        deps.add("İş Sağlığı ve Güvenliği (İSG)")
    if domain_badge == "KVKK & SİBER" or any(_contains_term(t, k) for k in ["kvkk", "kişisel veri", "verbis", "siber", "veri aktarımı", "usom", "btk"]):
        deps.add("Hukuk & Uyum")
        deps.add("Siber Güvenlik Operasyon Merkezi (SOC)")
        deps.add("Bilgi Teknolojileri (IT)")
    if domain_badge == "KAMU İHALE & SÖZLEŞMELER" or any(_contains_term(t, k) for k in ["kamu ihale", "4734", "4735", "fiyat farkı", "ihale"]):
        deps.add("Sözleşmeler & İhale Yönetimi")
        deps.add("Satınalma & Tedarik Zinciri")
    if domain_badge == "GÜMRÜK & DIŞ TİCARET" or any(_contains_term(t, k) for k in ["gümrük", "ithalat", "ihracat", "kambiyo", "dahilde işleme"]):
        deps.add("Dış Ticaret & Lojistik")
        deps.add("Gümrük Operasyonları")

    # Defense / Technical additions
    if any(_contains_term(t, k) for k in ["milli savunma", "askeri", "savunma", "harp", "deniz", "iha", "milgem", "kargu"]):
        deps.add("Savunma Projeleri Yönetimi")
        deps.add("Mühendislik & Sistem Entegrasyonu")
    if any(_contains_term(t, k) for k in ["yasak bölge", "tesis güvenlik", "güvenlik", "istihbarat", "gizli"]):
        deps.add("Tesis Güvenlik Koordinatörlüğü")
        deps.add("İdari İşler & Güvenlik")
    if any(_contains_term(t, k) for k in ["teknoloji geliştirme", "teknoloji", "ar-ge", "teknokent", "5746", "tgb"]):
        deps.add("Ar-Ge & Teknoloji Yönetimi")
        deps.add("Teşvik ve Fon Yönetimi")

    if not deps:
        deps.add("Hukuk & Uyum")
        deps.add("İç Denetim Başkanlığı")
    else:
        deps.add("Hukuk & Sözleşmeler")
        deps.add("İç Denetim Başkanlığı")

    return sorted(list(deps))


def generate_action_checklist(title: str, category: str, risk_level: str, domain_badge: str = "SEKTÖREL") -> List[str]:
    """Generates practical internal audit checklist items based on regulatory domain."""
    checklist = []
    t = lower_tr(title)

    # 1. Tax & Accounting
    if domain_badge == "VERGİ & MALİYE" or any(_contains_term(t, k) for k in ["vergi", "kdv", "fatura", "ssdf", "muhasebe", "tevkifat"]):
        checklist.append("ERP ve muhasebe parametrelerinin yeni vergi/fon oranlarına göre sistemde güncellenmesi.")
        checklist.append("Yeminli Mali Müşavir (YMM) / Vergi Danışmanı görüşü alınarak beyanname kontrollerinin yapılması.")
        checklist.append("E-Fatura, e-defter ve tevsik limitlerinin ilgili dönem takvimine işlenmesi.")

    # 2. Labor & HR
    elif domain_badge == "İŞ HUKUKU & İK" or any(_contains_term(t, k) for k in ["asgari ücret", "sgk", "iş kanunu", "isg", "tazminat"]):
        checklist.append("Bordro, özlük hakları ve asgari ücret/tavan parametrelerinin İK yazılımında güncellenmesi.")
        checklist.append("İş sözleşmeleri, uzaktan çalışma ve şirket içi İK prosedürlerinin mevzuata göre revize edilmesi.")
        checklist.append("6331 sayılı Kanun kapsamında İSG risk değerlendirmesi ve periyodik denetim adımlarının yürütülmesi.")

    # 3. KVKK & Data Privacy
    elif domain_badge == "KVKK & SİBER" or any(_contains_term(t, k) for k in ["kvkk", "kişisel veri", "verbis", "veri aktarımı"]):
        checklist.append("VERBİS kayıt envanteri ve veri işleme politikalarının güncel Kurul kararıyla doğrulanması.")
        checklist.append("Yurtdışı veri aktarımı ve standart sözleşme taahhütlerinin revize edilmesi.")
        checklist.append("Siber olay bildirim ve bilgi güvenliği prosedürlerinin test edilmesi.")

    # 4. Public Procurement & Tenders
    elif domain_badge == "KAMU İHALE & SÖZLEŞMELER" or any(_contains_term(t, k) for k in ["kamu ihale", "4734", "4735", "fiyat farkı"]):
        checklist.append("Kamu ihale eşik değerleri ve teminat oranlarının teklif hazırlık süreçlerine yansıtılması.")
        checklist.append("Mevcut sözleşmelerdeki fiyat farkı ve süre uzatımı haklarının hukuki analizinin yapılması.")

    # 5. Customs & Trade
    elif domain_badge == "GÜMRÜK & DIŞ TİCARET" or any(_contains_term(t, k) for k in ["gümrük", "ithalat", "ihracat", "kambiyo"]):
        checklist.append("Gümrük tarife pozisyonları (GTİP) ve ithalat gözetim/vergi oranlarının kontrol edilmesi.")
        checklist.append("Dahilde İşleme İzin Belgeleri (DİİB) ve ihracat taahhüt sürelerinin incelenmesi.")

    # 6. Defense & R&D / General
    else:
        if "teknoloji geliştirme" in t or "ar-ge" in t or "tgb" in t:
            checklist.append("Teknoloji Geliştirme Bölgesi (TGB) kapsamındaki Ar-Ge projelerinin ve teşvik şartlarının gözden geçirilmesi.")
            checklist.append("Yeni teknopark alanında şirketimiz için tesis/ofis tahsis imkanlarının değerlendirilmesi.")

        if "askeri yasak bölge" in t or "yasak bölge" in t:
            checklist.append("Şirketin operasyon, saha testleri ve uçuş/seyir izin protokollerinin askeri bölge sınırları doğrultusunda güncellenmesi.")
            checklist.append("Tesis ve Saha Güvenliği Prosedürlerinin Askeri Yasak Bölgeler mevzuatına uyumunun denetlenmesi.")

        if "yönetmelik" in t or (category and "yönetmelik" in lower_tr(category)):
            checklist.append("Şirket içi ilgili yönerge ve süreç dokümanlarının revize edilmesi.")
            checklist.append("Mevcut iş süreçlerinin yeni mevzuat maddeleri ile GAP (fark) analizinin yapılması.")

    checklist.append(f"İç Denetim Uyum Takvimine {datetime.now().strftime('%Y-%m')} dönemi periyodik kontrol adımı olarak eklenmesi.")
    return checklist


def evaluate_gazette_item(item: GazetteItem, profile: CompanyProfile, content: Optional[str] = None) -> AuditEvaluation:
    """
    Constructs a complete AuditEvaluation for a single item across all compliance domains.
    Leverages live LLM analysis if configured; otherwise uses universal deterministic heuristics.
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
        compliance_domain = "Sektörel / Yapay Zeka Analizi"
        domain_badge = "YZ DEĞERLENDİRME"
    else:
        score, matched_reasons, risk_level, compliance_domain, domain_badge = score_item_relevance(item, profile)
        affected_deps = infer_affected_departments(item.title, matched_reasons, domain_badge)
        checklist = generate_action_checklist(item.title, item.category, risk_level, domain_badge)

        doc_info = f" ({item.doc_number})" if item.doc_number else ""
        institution_info = f" ({item.institution})" if item.institution else ""
        summary = f"[{domain_badge}] {item.category}{institution_info} kapsamındaki '{item.title}' düzenlemesi yayımlanmıştır.{doc_info} Düzenleme şirketin {lower_tr(compliance_domain)} ve operasyonel işleyişi açısından doğrudan etki doğurmaktadır."

        penalty_risk = None
        if risk_level in ("Kritik", "Yüksek"):
            if domain_badge == "VERGİ & MALİYE":
                penalty_risk = "Vergi Usul Kanunu uyarınca vergi ziyaı cezası, gecikme faizi ve usulsüzlük yaptırımı riski bulunmaktadır."
            elif domain_badge == "İŞ HUKUKU & İK":
                penalty_risk = "İş Kanunu ve 6331 sayılı İSG Kanunu uyarınca idari para cezası ve iş durdurma riski bulunmaktadır."
            elif domain_badge == "KVKK & SİBER":
                penalty_risk = "6698 sayılı KVKK uyarınca 1.000.000 TL'yi aşan idari para cezası ve itibar kaybı riski bulunmaktadır."
            elif domain_badge == "KAMU İHALE & SÖZLEŞMELER":
                penalty_risk = "Kamu İhale Sözleşmeleri uyarınca teminatın irat kaydedilmesi ve kamu ihalelerinden yasaklanma riski bulunmaktadır."
            else:
                penalty_risk = "Yetkili düzenleyici otoritelerin mevzuatı ve ilgili kanunlar uyarınca idari para cezası, faaliyet kısıtı ve sözleşme fesih riski bulunmaktadır."

    effective_date = "Yayımı tarihinde"
    if content:
        date_match = re.search(r"(\d{1,2}/\d{1,2}/\d{4})\s+tarihinde\s+yürürlüğe\s+girer", content, re.IGNORECASE)
        if date_match:
            effective_date = date_match.group(1)

    return AuditEvaluation(
        item=item,
        relevance_score=score,
        risk_level=risk_level,
        compliance_domain=compliance_domain,
        domain_badge=domain_badge,
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
        score, _, _, _, _ = score_item_relevance(item, profile)
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
            score, _, _, _, _ = score_item_relevance(item, profile)
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
