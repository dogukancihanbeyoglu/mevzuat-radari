"""
AI and Multi-Tier Regulatory Hierarchy & Systematic Compliance Evaluator.
Features Deep Decision Content & Company Profile Impact Analysis Engine.
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
    SYSTEMATIC_COMPLIANCE_DOMAINS,
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
    Computes multi-tiered systematic relevance score (0-100) across:
    1. Norms Hierarchy (Presidential Decrees, Constitutional Court, Precedents)
    2. Vertical Sector & Regulators
    3. Cross-Cutting Corporate & Economic Domains (Tax, Labor, KVKK, Tenders, Customs, Incentives, ESG, Standards)
    Returns (score, matched_reasons, risk_level, compliance_domain, domain_badge).
    """
    title_lower = lower_tr(item.title)
    institution_lower = lower_tr(item.institution or "")
    category_lower = lower_tr(item.category or "")
    section_lower = lower_tr(item.section or "")
    combined_text = f"{title_lower} {institution_lower} {category_lower} {section_lower}"

    # 1. COMMERCIAL & SYSTEMIC OVERRIDE CHECK
    is_protected_from_noise = any(_contains_term(title_lower, term) for term in COMMERCIAL_OVERRIDE_TERMS) or \
                              any(_contains_term(category_lower, term) for term in ["kararname", "anayasa mahkemesi", "içtihat"])

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
    # TIER 1: CONSTITUTIONAL & SYSTEMIC LEGAL HIERARCHY
    # =========================================================================
    if "cumhurbaşkanlığı kararnamesi" in category_lower or "cumhurbaşkanlığı kararnamesi" in title_lower or "kararname numarası" in title_lower:
        score = max(score, 65)
        reasons.append("Hukuki Normlar Hiyerarşisi: Cumhurbaşkanlığı Kararnamesi (Genel Teşkilat / Sistemik Hüküm)")
        detected_domain = "Cumhurbaşkanlığı Kararnameleri & Sistemik Düzenlemeler"
        domain_badge = "CB KARARNAMESİ"

    if "anayasa mahkemesi" in category_lower or "anayasa mahkemesi" in institution_lower or "anayasa mahkemesi" in title_lower:
        score = max(score, 60)
        reasons.append("Yargısal Denetim: Anayasa Mahkemesi İptal / Bireysel Başvuru Esas Kararı")
        detected_domain = "Anayasa Mahkemesi Kararları"
        domain_badge = "YARGI & AYM"

    if "içtihadı birleştirme" in title_lower or "yargıtay içtihadı" in title_lower or "danıştay dava daireleri" in title_lower:
        score = max(score, 60)
        reasons.append("Yargısal İçtihat: Bağlayıcı Yüksek Yargı İçtihadı Birleştirme Kararı")
        detected_domain = "Yüksek Yargı İçtihadı Birleştirme"
        domain_badge = "YARGI & İÇTİHAT"

    # =========================================================================
    # TIER 2: VERTICAL SECTOR & COMPANY SPECIFIC LAYER
    # =========================================================================
    for kw in profile.keywords.high_priority:
        if _contains_term(title_lower, kw):
            score += 35
            reasons.append(f"Yüksek öncelikli dikey sektörel anahtar kelime: '{kw}'")

    for kw in profile.keywords.medium_priority:
        if _contains_term(title_lower, kw):
            score += 15
            reasons.append(f"Orta öncelikli sektörel anahtar kelime: '{kw}'")

    for reg in profile.regulatory_bodies:
        reg_clean = re.sub(r"\(.*?\)", "", reg).strip()
        acronym_match = re.search(r"\((.*?)\)", reg)
        acronym = acronym_match.group(1).strip() if acronym_match else ""

        if _contains_term(title_lower, reg_clean) or (acronym and _contains_term(title_lower, acronym)) or \
           (institution_lower and (_contains_term(institution_lower, reg_clean) or (acronym and _contains_term(institution_lower, acronym)))):
            score += 30
            reasons.append(f"Tabi olunan yetkili düzenleyici kurum: '{reg}'")

    primary_sec = lower_tr(profile.sectors_and_nace.primary_sector)
    if "savunma" in primary_sec or "askeri" in primary_sec:
        defense_indicators = ["milli savunma", "savunma sanayii", "askeri", "askeri yasak bölge", "harp", "denizaltı", "iha", "5201", "5202", "milgem", "kargu"]
        if any(_contains_term(title_lower, term) for term in defense_indicators):
            score += 35
            reasons.append("Savunma Sanayii, Askeri Denizcilik ve Taktik İHA regülasyonları ile doğrudan ilgili")
            detected_domain = "Savunma Sanayii & Askeri Sistemler"
            domain_badge = "SAVUNMA & ASKERİ"

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
    # TIER 3: CROSS-CUTTING CORPORATE & ECONOMIC REGULATORY DOMAINS
    # =========================================================================
    for dom_key, dom_data in SYSTEMATIC_COMPLIANCE_DOMAINS.items():
        matched_kw = [k for k in dom_data["keywords"] if _contains_term(title_lower, k)]
        if matched_kw:
            h_score = 45
            if any(c in category_lower or c in title_lower for c in ["tebliğ", "yönetmelik", "karar", "kanun", "kararname"]):
                h_score += 20
            score = max(score, h_score)
            
            reasons.append(f"Kurumsal/Sistemik Uyum [{dom_data['domain_name']}]: '{', '.join(matched_kw[:2])}' düzenlemesi")
            
            if detected_domain in ("Sektörel Uyum", "Genel"):
                detected_domain = dom_data["domain_name"]
                domain_badge = dom_data["badge_label"]

    # =========================================================================
    # TIER 4: STRATEGIC ECONOMIC TRIGGERS (Kamulaştırma vb.)
    # =========================================================================
    if "acele kamulaştırma" in title_lower or "kamulaştırma" in title_lower:
        score = max(score, 50)
        reasons.append("Stratejik Yatırım / Kamulaştırma: Taşınmaz ve saha mülkiyetini ilgilendiren kamu kararı")
        if detected_domain in ("Sektörel Uyum", "Genel"):
            detected_domain = "Kamulaştırma & Saha Güvenliği"
            domain_badge = "KAMULAŞTIRMA"

    if not reasons:
        return 0, [], "Bilgi", "Genel", "BİLGİ"

    final_score = min(score, 100)

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


def analyze_company_profile_impact(
    item: GazetteItem,
    profile: CompanyProfile,
    content: Optional[str],
    domain_badge: str,
    score: int,
) -> Tuple[str, str, str, str]:
    """
    Performs deep content inspection against the company profile.
    Returns (company_specific_impact, key_articles_summary, compliance_deadlines, raw_content_preview).
    """
    c_text = (content or "").strip()
    raw_preview = c_text[:380] + ("..." if len(c_text) > 380 else "") if c_text else "Kaynak metin fihrist başlığı üzerinden incelenmiştir."

    # 1. Company-Specific Semantic Meaning & Operational Impact
    comp_name = profile.general.name
    scale = profile.general.scale
    turnover = profile.general.annual_turnover_tl
    employees = profile.general.employee_count
    sec = profile.sectors_and_nace.primary_sector

    if "SAVUNMA" in domain_badge or "ASKERİ" in domain_badge:
        impact = (
            f"Şirketimiz {comp_name} ({sec}) açısından bu düzenleme; yürüttüğümüz askeri sistemler, "
            f"taktik İHA projeleri (KARGU/ALPAGU) ve askeri denizcilik (MİLGEM) platformlarının operasyonel test sahaları, "
            f"tesis güvenlik belgesi (5201/5202) ve Savunma Sanayii Başkanlığı (SSB) ile Milli Savunma Bakanlığı (MSB) "
            f"sözleşme yükümlülüklerini doğrudan bağlamaktadır. Proje ekiplerimizin saha izinleri ve gizlilik protokolleri kontrol edilmelidir."
        )
    elif "VERGİ" in domain_badge or "MALİ" in domain_badge:
        impact = (
            f"Şirketimizin {scale} ölçekli yapısı ve {turnover} yıllık işlem hacmi kapsamında; "
            f"bu tebliğ muhasebe ve ERP sistemlerimizde faturalama, tevkifat oranları, beyanname takvimi ve vergi matrahı "
            f"hesaplamalarında anlık güncelleme gerektirmektedir. Ayrıca şirketin 5746 sayılı Ar-Ge teşvikleri ve "
            f"Savunma Sanayii Destekleme Fonu (SSDF) kesintileri ile uyumu YMM denetiminde incelenmelidir."
        )
    elif "İŞ HUKUKU" in domain_badge or "İK" in domain_badge:
        impact = (
            f"Şirketimiz bünyesindeki {employees} çalışan, mühendislik iş gücü ve alt işveren/taşeron ilişkileri bakımından; "
            f"bordro parametreleri, kıdem tazminatı tavanı, SGK prim teşvikleri ve 6331 sayılı İSG mevzuatı kapsamında "
            f"çalışma ortamı ve iş sözleşmesi koşullarının ivedilikle güncellenmesini zorunlu kılmaktadır."
        )
    elif "KVKK" in domain_badge or "SİBER" in domain_badge:
        impact = (
            f"Şirketimizin işlediği personel, tedarikçi ve savunma sanayii paydaş verileri ile bilgi güvenliği operasyonlarımız "
            f"açısından; VERBİS envanteri, yurt dışına veri aktarım standart sözleşmeleri ve USOM/BTK siber olay bildirim "
            f"süreçlerinde yasal uyumun teyit edilmesi gerekmektedir."
        )
    elif "İHALE" in domain_badge or "SÖZLEŞME" in domain_badge:
        impact = (
            f"Şirketimizin kamu otoriteleri ve ana yüklenicilerle akdettiği sözleşmeler bakımından; "
            f"4734/4735 sayılı Kanunlar uyarınca fiyat farkı hesaplama formülleri, teminat mektubu oranları ve teslimat süre uzatımı "
            f"hakları maliyet ve nakit akışı fizibilitelerimize doğrudan etki etmektedir."
        )
    elif "GÜMRÜK" in domain_badge or "TİCARET" in domain_badge:
        impact = (
            f"Şirketimizin uluslararası tedarik zinciri, stratejik alt sistem ithalatı ve ihracat teslimatları kapsamında; "
            f"GTİP gümrük tarife pozisyonları, gözetim belgeleri, Dahilde İşleme İzin Belgeleri (DİİB) ve kambiyo ihracat bedeli "
            f"kapatma süreleri gümrük müşavirimiz kanalıyla denetlenmelidir."
        )
    elif "TEŞVİK" in domain_badge or "YATIRIM" in domain_badge:
        impact = (
            f"Şirketimizin Ar-Ge merkezi, teknopark ofisleri ve yüksek teknoloji üretim yatırımları için; "
            f"Sağlanan KDV istisnası, gümrük vergisi muafiyeti, faiz desteği ve SGK işveren hissesi prim indirimleri "
            f"şirketimizin yatırım bütçesi ve nakit projeksiyonlarına olumlu katkı sunmaktadır."
        )
    elif "ÇEVRE" in domain_badge or "SÜRDÜRÜLEBİLİRLİK" in domain_badge:
        impact = (
            f"Tesislerimizin çevre izin ve lisans belgeleri, Sıfır Atık sistemi, endüstriyel atık bertaraf protokolleri ve "
            f"Yeşil Dönüşüm / Karbon ayak izi kriterleri uyarınca idari ve saha operasyonlarımızın denetlenmesi gerekmektedir."
        )
    elif "STANDART" in domain_badge or "SANAYİ" in domain_badge:
        impact = (
            f"Üretim hatlarımız ve mühendislik çıktılarımız açısından; Sanayi Sicil Belgesi vize işlemleri ve güncellenen "
            f"TSE/CE standartlarına uygunluk sertifikasyonları satınalma ve üretim birimlerince doğrulanmalıdır."
        )
    elif "KARARNAME" in domain_badge or "AYM" in domain_badge or "İÇTİHAT" in domain_badge:
        impact = (
            f"Normlar hiyerarşisinin en üst basamağında yer alan bu düzenleme; şirketimizin kamu kurumlarıyla olan idari "
            f"muhataplıklarını, yetki hiyerarşisini ve devam eden adli/idari uyuşmazlıklardaki hukuki savunma stratejilerini doğrudan belirlemektedir."
        )
    else:
        impact = (
            f"Şirketimiz {comp_name} ({sec}) genel kurumsal işleyişi ve iç denetim uyum riskleri kapsamında; "
            f"ilgili mevzuat hükümleri operasyonel süreçlerimize entegre edilmeli ve takibe alınmalıdır."
        )

    # 2. Key Articles & Core Provisions Extraction
    articles = []
    if c_text:
        # Check for specific articles
        found_articles = re.findall(r"(MADDE\s+\d+[\s–\-—:]+[^\n\r]+)", c_text, re.IGNORECASE)
        if found_articles:
            articles = found_articles[:3]

    if articles:
        key_articles = " | ".join(articles)
    else:
        key_articles = f"Metin analizi: {item.category} çerçevesinde şirket yükümlülüklerini ve idari prosedürleri belirleyen temel hükümler yayımlanmıştır."

    # 3. Compliance Deadlines & Effective Date
    deadlines = "Yayımı tarihinde yürürlüğe girer."
    if c_text:
        date_match = re.search(r"(\d{1,2}/\d{1,2}/\d{4})\s+tarihinde\s+yürürlüğe\s+girer", c_text, re.IGNORECASE)
        if date_match:
            deadlines = f"{date_match.group(1)} tarihinde yürürlüğe girer."
        elif "yayımı tarihinden itibaren" in lower_tr(c_text):
            trans_match = re.search(r"yayımı\s+tarihinden\s+itibaren\s+([^.\n]+)", c_text, re.IGNORECASE)
            if trans_match:
                deadlines = f"Geçiş süreci: Yayımı tarihinden itibaren {trans_match.group(1).strip()}"

    return impact, key_articles, deadlines, raw_preview


def infer_affected_departments(title: str, matched_reasons: List[str], domain_badge: str = "SEKTÖREL") -> List[str]:
    """Infers internal company departments affected by the regulation across all corporate and systemic domains."""
    t = lower_tr(title)
    deps = set()

    if "KARARNAME" in domain_badge or "AYM" in domain_badge or "İÇTİHAT" in domain_badge:
        deps.add("Üst Yönetim & Genel Müdürlük")
        deps.add("Hukuk & Uyum")
        deps.add("Stratejik Planlama")

    if "VERGİ" in domain_badge or "MALİ" in domain_badge or any(_contains_term(t, k) for k in ["vergi", "kdv", "fatura", "ssdf", "muhasebe", "mali", "tevkifat"]):
        deps.add("Mali İşler & Muhasebe")
        deps.add("Finansman & Bütçe")
    if "İŞ HUKUKU" in domain_badge or "İK" in domain_badge or any(_contains_term(t, k) for k in ["iş kanunu", "asgari ücret", "sgk", "istihdam", "işçi", "isg", "tazminat"]):
        deps.add("İnsan Kaynakları")
        deps.add("Bordro & Özlük İşleri")
        deps.add("İş Sağlığı ve Güvenliği (İSG)")
    if "KVKK" in domain_badge or "SİBER" in domain_badge or any(_contains_term(t, k) for k in ["kvkk", "kişisel veri", "verbis", "siber", "veri aktarımı", "usom", "btk"]):
        deps.add("Hukuk & Uyum")
        deps.add("Siber Güvenlik Operasyon Merkezi (SOC)")
        deps.add("Bilgi Teknolojileri (IT)")
    if "İHALE" in domain_badge or "SÖZLEŞME" in domain_badge or any(_contains_term(t, k) for k in ["kamu ihale", "4734", "4735", "fiyat farkı", "ihale"]):
        deps.add("Sözleşmeler & İhale Yönetimi")
        deps.add("Satınalma & Tedarik Zinciri")
    if "GÜMRÜK" in domain_badge or "TİCARET" in domain_badge or any(_contains_term(t, k) for k in ["gümrük", "ithalat", "ihracat", "kambiyo", "dahilde işleme"]):
        deps.add("Dış Ticaret & Lojistik")
        deps.add("Gümrük Operasyonları")
    if "TEŞVİK" in domain_badge or "YATIRIM" in domain_badge or any(_contains_term(t, k) for k in ["yatırım teşvik", "devlet yardımları", "faiz desteği"]):
        deps.add("Yatırım & Finansman")
        deps.add("Stratejik Planlama")
    if "ÇEVRE" in domain_badge or "SÜRDÜRÜLEBİLİRLİK" in domain_badge or any(_contains_term(t, k) for k in ["çevre", "çed", "sıfır atık", "karbon"]):
        deps.add("İş Sağlığı, Güvenliği & Çevre (İSG-Ç)")
        deps.add("Tesis Yönetimi & İdari İşler")
    if "STANDART" in domain_badge or "SANAYİ" in domain_badge or any(_contains_term(t, k) for k in ["sanayi sicil", "tse", "ce işareti", "standart"]):
        deps.add("Kalite Güvence & Standardizasyon")
        deps.add("Üretim & Mühendislik")
    if "KAMULAŞTIRMA" in domain_badge or any(_contains_term(t, k) for k in ["kamulaştırma", "yasak bölge", "saha"]):
        deps.add("Tesis Güvenlik Koordinatörlüğü")
        deps.add("İdari İşler & Emlak")

    if any(_contains_term(t, k) for k in ["milli savunma", "askeri", "savunma", "harp", "deniz", "iha", "milgem", "kargu"]):
        deps.add("Savunma Projeleri Yönetimi")
        deps.add("Mühendislik & Sistem Entegrasyonu")
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
    """Generates practical internal audit checklist items based on systematic regulatory domain."""
    checklist = []
    t = lower_tr(title)

    if "KARARNAME" in domain_badge:
        checklist.append("Cumhurbaşkanlığı Kararnamesi ile değişen kamu teşkilat yapısı ve yetki devirlerinin incelenmesi.")
        checklist.append("Şirketimizin kamu kurumlarıyla olan yasal süreç ve muhataplıklarının güncellenmesi.")
    elif "AYM" in domain_badge or "İÇTİHAT" in domain_badge:
        checklist.append("Yüksek Mahkeme iptal/içtihat kararının şirket aleyhine/lehine doğurabileceği uyuşmazlıkların incelenmesi.")
        checklist.append("Devam eden ticari sözleşme ve davaların güncel içtihada göre hukuki analizinin yapılması.")
    elif "VERGİ" in domain_badge or "MALİ" in domain_badge or any(_contains_term(t, k) for k in ["vergi", "kdv", "fatura", "ssdf", "muhasebe", "tevkifat"]):
        checklist.append("ERP ve muhasebe parametrelerinin yeni vergi/fon oranlarına göre sistemde güncellenmesi.")
        checklist.append("Yeminli Mali Müşavir (YMM) / Vergi Danışmanı görüşü alınarak beyanname kontrollerinin yapılması.")
        checklist.append("E-Fatura, e-defter ve tevsik limitlerinin ilgili dönem takvimine işlenmesi.")
    elif "İŞ HUKUKU" in domain_badge or "İK" in domain_badge or any(_contains_term(t, k) for k in ["asgari ücret", "sgk", "iş kanunu", "isg", "tazminat"]):
        checklist.append("Bordro, özlük hakları ve asgari ücret/tavan parametrelerinin İK yazılımında güncellenmesi.")
        checklist.append("İş sözleşmeleri, uzaktan çalışma ve şirket içi İK prosedürlerinin mevzuata göre revize edilmesi.")
        checklist.append("6331 sayılı Kanun kapsamında İSG risk değerlendirmesi ve periyodik denetim adımlarının yürütülmesi.")
    elif "KVKK" in domain_badge or "SİBER" in domain_badge or any(_contains_term(t, k) for k in ["kvkk", "kişisel veri", "verbis", "veri aktarımı"]):
        checklist.append("VERBİS kayıt envanteri ve veri işleme politikalarının güncel Kurul kararıyla doğrulanması.")
        checklist.append("Yurtdışı veri aktarımı ve standart sözleşme taahhütlerinin revize edilmesi.")
        checklist.append("Siber olay bildirim ve bilgi güvenliği prosedürlerinin test edilmesi.")
    elif "İHALE" in domain_badge or "SÖZLEŞME" in domain_badge or any(_contains_term(t, k) for k in ["kamu ihale", "4734", "4735", "fiyat farkı"]):
        checklist.append("Kamu ihale eşik değerleri ve teminat oranlarının teklif hazırlık süreçlerine yansıtılması.")
        checklist.append("Mevcut sözleşmelerdeki fiyat farkı ve süre uzatımı haklarının hukuki analizinin yapılması.")
    elif "GÜMRÜK" in domain_badge or "TİCARET" in domain_badge or any(_contains_term(t, k) for k in ["gümrük", "ithalat", "ihracat", "kambiyo"]):
        checklist.append("Gümrük tarife pozisyonları (GTİP) ve ithalat gözetim/vergi oranlarının kontrol edilmesi.")
        checklist.append("Dahilde İşleme İzin Belgeleri (DİİB) ve ihracat taahhüt sürelerinin incelenmesi.")
    elif "TEŞVİK" in domain_badge or "YATIRIM" in domain_badge:
        checklist.append("Yatırım Teşvik Belgesi (YTB) ve vergi muafiyeti şartlarının fizibilitelere yansıtılması.")
        checklist.append("Faiz desteği ve SGK prim desteği başvurularının takvimlendirilmesi.")
    elif "ÇEVRE" in domain_badge or "SÜRDÜRÜLEBİLİRLİK" in domain_badge:
        checklist.append("Çevre İzin/Lisans ve Sıfır Atık beyannamelerinin denetlenmesi.")
        checklist.append("Karbon emisyon ve Yeşil Dönüşüm kriterlerinin tesis operasyonlarına entegrasyonu.")
    elif "STANDART" in domain_badge or "SANAYİ" in domain_badge:
        checklist.append("Sanayi Sicil Belgesi ve yıllık işletme cetvellerinin kontrol edilmesi.")
        checklist.append("TSE / CE uygunluk sertifikalarının üretim süreçlerine uyarlanması.")
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
        
        impact, key_articles, deadlines, raw_preview = analyze_company_profile_impact(item, profile, content, domain_badge, score)
    else:
        score, matched_reasons, risk_level, compliance_domain, domain_badge = score_item_relevance(item, profile)
        affected_deps = infer_affected_departments(item.title, matched_reasons, domain_badge)
        checklist = generate_action_checklist(item.title, item.category, risk_level, domain_badge)
        impact, key_articles, deadlines, raw_preview = analyze_company_profile_impact(item, profile, content, domain_badge, score)

        doc_info = f" ({item.doc_number})" if item.doc_number else ""
        institution_info = f" ({item.institution})" if item.institution else ""
        summary = f"[{domain_badge}] {item.category}{institution_info} kapsamındaki '{item.title}' düzenlemesi yayımlanmıştır.{doc_info} Düzenleme şirketin {lower_tr(compliance_domain)} ve operasyonel işleyişi açısından doğrudan etki doğurmaktadır."

        penalty_risk = None
        if risk_level in ("Kritik", "Yüksek"):
            if "KARARNAME" in domain_badge:
                penalty_risk = "Doğrudan kanun hükmünde yasal bağlayıcılığı haiz olup, şirket faaliyetlerinin teşkilat düzenlemelerine uyumlu yürütülmesi zorunludur."
            elif "VERGİ" in domain_badge or "MALİ" in domain_badge:
                penalty_risk = "Vergi Usul Kanunu uyarınca vergi ziyaı cezası, gecikme faizi ve usulsüzlük yaptırımı riski bulunmaktadır."
            elif "İŞ HUKUKU" in domain_badge or "İK" in domain_badge:
                penalty_risk = "İş Kanunu ve 6331 sayılı İSG Kanunu uyarınca idari para cezası ve iş durdurma riski bulunmaktadır."
            elif "KVKK" in domain_badge or "SİBER" in domain_badge:
                penalty_risk = "6698 sayılı KVKK uyarınca 1.000.000 TL'yi aşan idari para cezası ve itibar kaybı riski bulunmaktadır."
            elif "İHALE" in domain_badge or "SÖZLEŞME" in domain_badge:
                penalty_risk = "Kamu İhale Sözleşmeleri uyarınca teminatın irat kaydedilmesi ve kamu ihalelerinden yasaklanma riski bulunmaktadır."
            else:
                penalty_risk = "Yetkili düzenleyici otoritelerin mevzuatı ve ilgili kanunlar uyarınca idari para cezası, faaliyet kısıtı ve sözleşme fesih riski bulunmaktadır."

    effective_date = deadlines

    return AuditEvaluation(
        item=item,
        relevance_score=score,
        risk_level=risk_level,
        compliance_domain=compliance_domain,
        domain_badge=domain_badge,
        matched_reasons=matched_reasons,
        executive_summary=summary,
        company_specific_impact=impact,
        key_articles_summary=key_articles,
        compliance_deadlines=deadlines,
        penalty_and_legal_risk=penalty_risk,
        affected_departments=affected_deps,
        action_checklist=checklist,
        effective_date=effective_date,
        raw_content_preview=raw_preview,
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
