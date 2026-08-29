"""
Universal Industry Presets and Multi-Layered Compliance Taxonomy for Mevzuat Radarı.
Provides:
1. Universal Public Administration Noise Classifier (filters student/academic/municipal noise)
2. Horizontal Corporate Compliance Domains (Tax, Labor/HR, KVKK, Customs, Public Procurement, Corporate Law)
3. Vertical Sector Presets (Defense, FinTech, E-Commerce, Software, Energy)
"""
from typing import Dict, Any, List

# 1. Universal Public Administration Noise Keywords (Suppressed unless explicit commercial override)
UNIVERSAL_NOISE_KEYWORDS = [
    # Academic & University Internal Affairs
    "öğrenci", "lisans", "lisansüstü", "yüksek lisans", "doktora", "fakülte",
    "enstitü", "rektörlük", "akademik", "öğretim elemanı", "öğretim üyesi",
    "öğretim görevlisi", "müfredat", "sınav yönetmeliği", "öğrenci işleri",
    "yaz okulu", "kayıt kabul", "önlisans", "diploma", "tez savunma", "araştırma görevlisi",
    # Civil Servant Internal HR & Routine Discipline
    "görevde yükselme", "unvan değişikliği", "disiplin amirleri", "memur disiplin",
    "personel yer değiştirme", "hizmet içi eğitim", "zabıta yönetmeliği", "itfaiye personeli",
    # Professional Chambers Internal Affairs
    "tabip odası", "veteriner hekimler", "baro levhası", "noter stajyer", "oda aidatı",
    # Municipal Internal Budgets & Local Tariffs
    "belediye meclisi kararı", "belediye bütçesi", "il özel idaresi bütçe", "taksi dolmuş tarifesi",
]

# 2. Universal Commercial & Regulatory Override Terms
COMMERCIAL_OVERRIDE_TERMS = [
    "teknoloji geliştirme bölgesi", "tgb", "savunma sanayii", "askeri yasak bölge",
    "harp aracı", "ihracat kontrol", "5201", "5202", "kamu ihale", "ihale", "tedarik",
    "vergi muafiyeti", "ar-ge merkezi", "5746", "ithalat kotası", "kambiyo", "gümrük",
    "rekabet kurulu", "spk", "bddk", "epdk", "masak", "kvkk", "kişisel veri", "kişisel veriler",
    "veri aktarımı", "veri sorumlusu", "verbis", "asgari ücret", "kdv", "katma değer vergisi",
    "kurumlar vergisi", "gelir vergisi", "vergi usul", "sgk", "iş kanunu", "iş sağlığı ve güvenliği",
    "fiyat farkı", "ticaret sicili", "türk ticaret kanunu", "ttk",
]

# 3. Horizontal Corporate Compliance Domains (Affects EVERY Turkish Commercial Entity)
HORIZONTAL_CORPORATE_DOMAINS: Dict[str, Dict[str, Any]] = {
    "tax_and_finance": {
        "domain_name": "Mali İşler & Vergi Mevzuatı",
        "badge_label": "VERGİ & MALİYE",
        "badge_color": "emerald",
        "keywords": [
            "katma değer vergisi", "kdv", "kurumlar vergisi", "gelir vergisi", "vergi usul kanunu",
            "vuk", "vergi tevsik", "tevkifat", "e-fatura", "e-defter", "e-arşiv", "enflasyon muhasebesi",
            "enflasyon düzeltmesi", "transfer fiyatlandırması", "savunma sanayii destekleme fonu",
            "ssdf", "kambiyo", "döviz tebliği", "reeskont", "damga vergisi", "harçlar kanunu",
            "muhtasar", "vergi ziyaı", "yeniden değerleme oranı", "özel tüketim vergisi", "ötv",
        ],
        "default_departments": ["Mali İşler & Muhasebe", "Vergi & Finansman", "Hukuk & Uyum"],
        "checklist": [
            "ERP ve muhasebe parametrelerinin yeni vergi oranları/tebliğ hükümlerine göre güncellenmesi.",
            "Yeminli Mali Müşavir (YMM) / Vergi Danışmanı görüşü alınarak beyanname kontrollerinin yapılması.",
            "E-Fatura, e-defter ve tevsik limitlerinin ilgili dönem takvimine işlenmesi."
        ]
    },
    "labor_and_hr": {
        "domain_name": "İş Hukuku, İK & Sosyal Güvenlik",
        "badge_label": "İŞ HUKUKU & İK",
        "badge_color": "indigo",
        "keywords": [
            "asgari ücret", "sgk", "sosyal güvenlik", "iş kanunu", "4857", "kıdem tazminatı",
            "ihbar tazminatı", "iş sağlığı ve güvenliği", "isg", "6331", "istihdam teşviki",
            "işsizlik sigortası", "engelli istihdamı", "fazla mesai", "uzaktan çalışma",
            "iş kazası bildirimi", "prim teşviki", "kıdem tazminatı tavanı", "iş güvencesi",
        ],
        "default_departments": ["İnsan Kaynakları", "Bordro & Özlük İşleri", "İş Sağlığı ve Güvenliği (İSG)", "Hukuk & Uyum"],
        "checklist": [
            "Bordro, özlük hakları ve asgari ücret/tavan parametrelerinin İK yazılımında güncellenmesi.",
            "İş sözleşmeleri, uzaktan çalışma yönergeleri ve şirket içi İK prosedürlerinin gözden geçirilmesi.",
            "6331 sayılı Kanun kapsamında İSG risk değerlendirmesi ve periyodik eğitim takviminin denetlenmesi."
        ]
    },
    "data_privacy_and_cyber": {
        "domain_name": "Kişisel Verilerin Korunması & Siber Uyum",
        "badge_label": "KVKK & SİBER",
        "badge_color": "cyan",
        "keywords": [
            "kişisel veri", "kişisel veriler", "kvkk", "6698", "verbis", "veri sorumlusu",
            "veri aktarımı", "aktarılması", "standart sözleşme", "açık rıza", "veri işleyen",
            "veri ihlal", "özel nitelikli kişisel veri", "siber güvenlik", "usom", "elektronik haberleşme",
            "e-imza", "5070", "çerez politikası",
        ],
        "default_departments": ["Hukuk & Uyum", "Siber Güvenlik Operasyon Merkezi (SOC)", "Bilgi Teknolojileri (IT)"],
        "checklist": [
            "VERBİS kayıt envanteri ve veri işleme politikalarının güncel mevzuatla uyumunun doğrulanması.",
            "Yurtdışı veri aktarımı ve standart sözleşme taahhütlerinin KVKK Kurul kararlarına göre revize edilmesi.",
            "Bilgi güvenliği ve siber olay bildirim prosedürlerinin test edilmesi."
        ]
    },
    "public_procurement": {
        "domain_name": "Kamu İhale & Sözleşmeler Hukuku",
        "badge_label": "KAMU İHALE & SÖZLEŞMELER",
        "badge_color": "amber",
        "keywords": [
            "kamu ihale kanunu", "kamu ihale", "4734", "4735", "kamu sözleşmeleri", "fiyat farkı kararnamesi",
            "fiyat farkı", "ihale eşik değerleri", "teminat mektubu", "yerli malı tebliği",
            "sanayi işbirliği programı", "sip", "doğrudan temin", "aşırı düşük teklif", "kik",
        ],
        "default_departments": ["Sözleşmeler & İhale Yönetimi", "Satınalma & Tedarik Zinciri", "Hukuk & Uyum"],
        "checklist": [
            "Kamu ihale eşik değerleri ve teminat oranlarının sözleşme hazırlık süreçlerine yansıtılması.",
            "Mevcut kamu sözleşmelerindeki fiyat farkı ve süre uzatımı haklarının analiz edilmesi.",
            "Yerli katkı oranı ve sanayi iş birliği şartnamelerinin kontrol edilmesi."
        ]
    },
    "customs_and_trade": {
        "domain_name": "Gümrük, Dış Ticaret & İthalat/İhracat",
        "badge_label": "GÜMRÜK & DIŞ TİCARET",
        "badge_color": "sky",
        "keywords": [
            "gümrük genel tebliği", "ithalat rejimi", "ihracat rejimi", "gümrük kanunu", "4458",
            "dahilde işleme rejimi", "dir", "menşe şahadetnamesi", "ithalatta haksız rekabet",
            "gözetim tebliği", "ihracat bedelleri", "kambiyo takibi", "ithalat vergisi", "ek mali yükümlülük",
        ],
        "default_departments": ["Dış Ticaret & Lojistik", "Gümrük Operasyonları", "Tedarik Zinciri", "Mali İşler"],
        "checklist": [
            "Gümrük tarife pozisyonları (GTİP) ve ithalat gözetim/vergi oranlarının kontrol edilmesi.",
            "Dahilde İşleme İzin Belgeleri (DİİB) ve ihracat taahhüt sürelerinin incelenmesi.",
            "İhracat bedellerinin yurda getirilmesi ve kambiyo kapanış sürelerinin takibe alınması."
        ]
    },
    "corporate_and_commercial": {
        "domain_name": "Şirketler & Ticaret Hukuku",
        "badge_label": "TİCARET & ŞİRKETLER",
        "badge_color": "purple",
        "keywords": [
            "türk ticaret kanunu", "ttk", "6102", "ticaret sicili", "anonim şirket", "genel kurul",
            "sermaye kaybı", "borca batıklık", "bağımsız denetim kriterleri", "rekabetin korunması",
            "4054", "rekabet kurulu", "birleşme ve devralma", "ticari elektronik ileti",
        ],
        "default_departments": ["Hukuk & Uyum", "Yönetim Kurulu Genel Sekreterliği", "İç Denetim Başkanlığı"],
        "checklist": [
            "Genel kurul, yönetim kurulu karar defteri ve ticaret sicil yükümlülüklerinin denetlenmesi.",
            "Bağımsız denetim eşik değerleri ve finansal raporlama standartlarına uyumun teyit edilmesi.",
            "Rekabet Hukuku ve dikey anlaşmalar kapsamındaki şirket sözleşmelerinin gözden geçirilmesi."
        ]
    }
}

# 4. Standard Vertical Sector Presets
SECTOR_PRESETS: Dict[str, Dict[str, Any]] = {
    "defense_aerospace": {
        "name": "Savunma Sanayii, Havacılık & Askeri Sistemler (STM, Aselsan vb.)",
        "primary_sector": "Savunma Sanayii, Askeri Denizcilik ve Taktik İHA Sistemleri",
        "nace_codes": ["30.40.00", "30.11.02", "62.01.01", "72.19.01", "30.30.01"],
        "regulatory_bodies": [
            "Cumhurbaşkanlığı Savunma Sanayii Başkanlığı (SSB)",
            "Milli Savunma Bakanlığı (MSB)",
            "Sanayi ve Teknoloji Bakanlığı",
            "Ticaret Bakanlığı (Kontrole Tabi Savunma İhracatı)",
            "Ulaştırma ve Altyapı Bakanlığı / BTK / USOM",
            "Hazine ve Maliye Bakanlığı (Savunma Sanayii Destekleme Fonu - SSDF)",
            "Kişisel Verileri Koruma Kurumu (KVKK)",
        ],
        "high_priority_keywords": [
            "savunma sanayii", "milli savunma", "askeri", "teknoloji geliştirme bölgesi",
            "insansız hava aracı", "iha", "siber güvenlik", "askeri yasak bölge",
            "denizaltı", "harp gemisi", "5201", "5202", "ssb", "ar-ge", "tesis güvenlik",
            "kargu", "milgem", "alpagu", "milli gizli", "nato gizli"
        ],
        "medium_priority_keywords": [
            "ihracat izni", "stratejik malzeme", "kamulaştırma", "teknokent",
            "bilgi güvenliği", "kamu ihale", "kambiyo", "radar", "aviyonik"
        ],
        "excluded_keywords": UNIVERSAL_NOISE_KEYWORDS + [
            "sağlık personeli", "hastane", "belediye", "eczane", "tıbbi cihaz", "ilaç fiyat"
        ],
        "has_foreign_trade": True,
        "has_rd_center": True,
        "e_commerce_license": False,
    },
    "fintech_banking": {
        "name": "Finans, Bankacılık & FinTech (Ödeme Sistemleri, Elektronik Para, Kripto)",
        "primary_sector": "Finansal Teknolojiler, Ödeme Hizmetleri ve Elektronik Para",
        "nace_codes": ["64.19.01", "66.19.01", "64.99.01", "62.01.01"],
        "regulatory_bodies": [
            "Bankacılık Düzenleme ve Denetleme Kurumu (BDDK)",
            "Türkiye Cumhuriyet Merkez Bankası (TCMB)",
            "Sermaye Piyasası Kurulu (SPK)",
            "Mali Suçları Araştırma Kurulu (MASAK)",
            "Kişisel Verileri Koruma Kurumu (KVKK)",
            "Sigortacılık ve Özel Emeklilik Düzenleme ve Denetleme Kurumu (SEDDK)",
        ],
        "high_priority_keywords": [
            "ödeme hizmetleri", "elektronik para", "6493", "5411", "6362", "bddk", "tcmb",
            "masak", "kara para", "kripto varlık", "açık bankacılık", "fast", "iban",
            "sermaye yeterliliği", "kredi kartı", "pos", "uzaktan kimlik tespiti"
        ],
        "medium_priority_keywords": [
            "finansal kiralama", "faktoring", "tüketici kredisi", "faiz oranı",
            "döviz pozisyonu", "kambiyo", "bilgi sistemleri tebliği", "siber güvenlik"
        ],
        "excluded_keywords": UNIVERSAL_NOISE_KEYWORDS + [
            "milli savunma", "askeri", "harp", "silah", "kamulaştırma", "maden ruhsatı"
        ],
        "has_foreign_trade": False,
        "has_rd_center": True,
        "e_commerce_license": True,
    },
    "ecommerce_retail": {
        "name": "E-Ticaret, Pazaryeri & Perakende Ticaret",
        "primary_sector": "Elektronik Ticaret, Dijital Pazaryeri ve Perakende Satış",
        "nace_codes": ["47.91.00", "47.19.01", "53.20.09", "62.01.01"],
        "regulatory_bodies": [
            "Ticaret Bakanlığı (İç Ticaret & Tüketicinin Korunması)",
            "Rekabet Kurumu",
            "Kişisel Verileri Koruma Kurumu (KVKK)",
            "Gelir İdaresi Başkanlığı (GİB)",
            "Bilgi Teknolojileri ve İletişim Kurumu (BTK)",
        ],
        "high_priority_keywords": [
            "elektronik ticaret", "e-ticaret", "6563", "6502", "mesafeli sözleşmeler",
            "etbis", "pazaryeri", "tüketicinin korunması", "fiyat etiketi",
            "haksız ticari uygulama", "cayma hakkı", "kargo taşıma", "e-fatura"
        ],
        "medium_priority_keywords": [
            "indirimli satış", "reklam kurulu", "ticari elektronik ileti", "iys",
            "stokçuluk", "fahiş fiyat", "rekabet ihlali", "ithalat gözetim"
        ],
        "excluded_keywords": UNIVERSAL_NOISE_KEYWORDS + [
            "milli savunma", "askeri", "harp", "nükleer", "petrol arama", "maden"
        ],
        "has_foreign_trade": True,
        "has_rd_center": True,
        "e_commerce_license": True,
    },
    "energy_utilities": {
        "name": "Enerji, Elektrik Piyasası & Yenilenebilir Kaynaklar",
        "primary_sector": "Elektrik Üretimi, Dağıtımı ve Yenilenebilir Enerji (GES/RES)",
        "nace_codes": ["35.11.19", "35.12.01", "35.14.01"],
        "regulatory_bodies": [
            "Enerji Piyasası Düzenleme Kurumu (EPDK)",
            "Enerji ve Tabii Kaynaklar Bakanlığı",
            "Türkiye Elektrik İletim A.Ş. (TEİAŞ)",
            "Çevre, Şehircilik ve İklim Değişikliği Bakanlığı",
            "Rekabet Kurumu",
        ],
        "high_priority_keywords": [
            "epdk", "elektrik piyasası", "6446", "yekdem", "lisanssız elektrik",
            "güneş enerjisi", "ges", "rüzgar enerjisi", "res", "şebeke bağlantı",
            "dağıtım tarifesi", "karbon emisyon", "doğal gaz piyasası"
        ],
        "medium_priority_keywords": [
            "kamulaştırma", "çed", "çevre izin", "enerji verimliliği", "piyasa takas fiyatı",
            "emisyon ticareti", "maden sahası"
        ],
        "excluded_keywords": UNIVERSAL_NOISE_KEYWORDS + [
            "askeri", "savunma sanayii", "tıbbi cihaz", "eczane", "hastane"
        ],
        "has_foreign_trade": False,
        "has_rd_center": True,
        "e_commerce_license": False,
    },
    "software_saas": {
        "name": "Yazılım, SaaS & Ar-Ge Teknolojileri",
        "primary_sector": "Bilgisayar Programlama, Bulut Bilişim ve SaaS Platformları",
        "nace_codes": ["62.01.01", "62.02.01", "58.29.01", "72.19.01"],
        "regulatory_bodies": [
            "Sanayi ve Teknoloji Bakanlığı (Teknopark & Ar-Ge GM)",
            "Bilgi Teknolojileri ve İletişim Kurumu (BTK)",
            "Kişisel Verileri Koruma Kurumu (KVKK)",
            "Gelir İdaresi Başkanlığı (Ar-Ge Vergi Teşvikleri)",
        ],
        "high_priority_keywords": [
            "teknoloji geliştirme bölgesi", "tgb", "teknokent", "5746", "4691", "ar-ge",
            "siber güvenlik", "kvkk", "kişisel veri", "bulut bilişim", "yazılım ihracatı",
            "yapay zeka", "telif hakları", "fikri mülkiyet"
        ],
        "medium_priority_keywords": [
            "tübitak", "kosgeb", "hizmet ihracatı teşvik", "açık kaynak", "veri merkezi",
            "bilgi güvenliği", "e-imza"
        ],
        "excluded_keywords": UNIVERSAL_NOISE_KEYWORDS + [
            "milli savunma", "askeri yasak bölge", "sağlık personeli", "belediye meclisi"
        ],
        "has_foreign_trade": True,
        "has_rd_center": True,
        "e_commerce_license": False,
    }
}


def get_preset_list() -> List[Dict[str, str]]:
    """Returns list of preset keys and labels for UI dropdown."""
    return [{"key": k, "name": v["name"]} for k, v in SECTOR_PRESETS.items()]


def get_preset_data(preset_key: str) -> Dict[str, Any]:
    """Retrieves full configuration dict for a selected preset."""
    if preset_key in SECTOR_PRESETS:
        return SECTOR_PRESETS[preset_key]
    return SECTOR_PRESETS["defense_aerospace"]
