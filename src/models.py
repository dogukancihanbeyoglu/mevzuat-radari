"""
Data models for Mevzuat Radarı (Resmî Gazete İç Denetim & Uyum Radarı).
Includes support for Deep Content Analysis, Company-Specific Impact, and Multi-Tier Compliance.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class GeneralCompanyInfo(BaseModel):
    name: str = Field(default="Anonim Şirket", description="Şirket unvanı")
    legal_type: str = Field(default="Anonim Şirket", description="Şirket türü")
    scale: str = Field(default="Büyük Ölçekli", description="Şirket ölçeği")
    employee_count: int = Field(default=100, description="Çalışan sayısı")
    annual_turnover_tl: str = Field(default="100M+", description="Yıllık ciro skalası")
    is_publicly_traded: bool = Field(default=False, description="Halka açık mı?")


class SectorsAndNace(BaseModel):
    primary_sector: str = Field(..., description="Ana faaliyet alanı")
    secondary_sectors: List[str] = Field(default_factory=list, description="Yan faaliyet alanları")
    nace_codes: List[str] = Field(default_factory=list, description="NACE kodları")


class OperationalTraits(BaseModel):
    has_foreign_trade: bool = Field(default=False, description="İthalat / İhracat var mı?")
    has_rd_center: bool = Field(default=False, description="Ar-Ge merkezi veya teknokent teşviki var mı?")
    uses_subcontractors: bool = Field(default=False, description="Alt işveren / taşeron kullanımı var mı?")
    e_commerce_license: bool = Field(default=False, description="E-ticaret faaliyeti var mı?")
    processes_special_category_data: bool = Field(default=False, description="Özel nitelikli kişisel veri işleme")


class KeywordsConfig(BaseModel):
    high_priority: List[str] = Field(default_factory=list, description="Yüksek öncelikli anahtar kelimeler")
    medium_priority: List[str] = Field(default_factory=list, description="Orta öncelikli anahtar kelimeler")
    excluded: List[str] = Field(default_factory=list, description="Negatif / Hariç tutulacak kelimeler (öğrenci, akademik, vb.)")


class CompanyProfile(BaseModel):
    general: GeneralCompanyInfo
    sectors_and_nace: SectorsAndNace
    regulatory_bodies: List[str] = Field(default_factory=list, description="Tabi olunan kurumlar")
    operational_traits: OperationalTraits = Field(default_factory=OperationalTraits)
    risk_priorities: Dict[str, str] = Field(default_factory=dict, description="Risk öncelik haritası")
    keywords: KeywordsConfig = Field(default_factory=KeywordsConfig)


class GazetteItem(BaseModel):
    title: str = Field(..., description="Mevzuat/Karar başlığı")
    url: str = Field(..., description="Detay URL bağlantısı (.htm veya .pdf)")
    category: str = Field(default="Genel", description="Kategori: Yönetmelik, Tebliğ, Kurul Kararı, CB Kararı vb.")
    institution: Optional[str] = Field(default=None, description="Düzenleyici Kurum / Bakanlık")
    section: str = Field(default="Yürütme ve İdare Bölümü", description="Bölüm: Yürütme ve İdare, Yargı, vb.")
    doc_number: Optional[str] = Field(default=None, description="Tebliğ/Karar/Sayı No")
    gazette_date: Optional[str] = Field(default=None, description="Gazetenin yayım tarihi (YYYY-MM-DD)")
    gazette_number: Optional[str] = Field(default=None, description="Resmî Gazete sayısı")
    location_breadcrumb: Optional[str] = Field(default=None, description="Gazetedeki tam konumu")
    is_pdf: bool = Field(default=False, description="Belge PDF formatında mı?")


class GazetteIndex(BaseModel):
    date: str = Field(..., description="Gazete tarihi (YYYY-MM-DD veya DD.MM.YYYY)")
    gazette_number: Optional[str] = Field(default=None, description="Resmî Gazete sayısı")
    total_items: int = Field(default=0, description="Toplam madde sayısı")
    items: List[GazetteItem] = Field(default_factory=list, description="Fihrist maddeleri")


class AuditEvaluation(BaseModel):
    item: GazetteItem
    relevance_score: int = Field(..., ge=0, le=100, description="0-100 arası alaka skoru")
    risk_level: str = Field(..., description="Risk Seviyesi: Kritik, Yüksek, Orta, Düşük, Bilgi")
    compliance_domain: str = Field(default="Sektörel Uyum", description="Uyum Alanı: Sektörel Uyum, Vergi & Maliye, İş Hukuku & İK, KVKK & Siber, vb.")
    domain_badge: str = Field(default="SEKTÖREL", description="Rozet: SEKTÖREL, VERGİ & MALİYE, İŞ HUKUKU & İK, vb.")
    matched_reasons: List[str] = Field(default_factory=list, description="Neden şirketle alakalı?")
    executive_summary: str = Field(..., description="Yönetici özeti")
    company_specific_impact: Optional[str] = Field(default=None, description="Şirket profili açısından derin etki ve anlam analizi")
    key_articles_summary: Optional[str] = Field(default=None, description="Metinden çıkarılan kritik maddeler ve hükümler")
    compliance_deadlines: Optional[str] = Field(default=None, description="Yürürlük, geçiş süresi ve bildirim takvimi")
    penalty_and_legal_risk: Optional[str] = Field(default=None, description="Cezai ve hukuki yaptırım riski")
    affected_departments: List[str] = Field(default_factory=list, description="Etkilenen departmanlar")
    action_checklist: List[str] = Field(default_factory=list, description="İç denetim kontrol/aksiyon listesi")
    effective_date: Optional[str] = Field(default=None, description="Yürürlük tarihi")
    raw_content_preview: Optional[str] = Field(default=None, description="Kaynak metin önizlemesi")


class DailyAuditReport(BaseModel):
    date: str
    gazette_number: Optional[str] = None
    company_name: str
    total_scanned: int
    relevant_count: int
    evaluations: List[AuditEvaluation] = Field(default_factory=list)
    generated_at: str
