# 🏛️ Resmî Gazete İç Denetim & Uyum Radarı (Mevzuat-Radari)
## Proje Tasarımı, Teknik Altyapı ve Adım Adım Geliştirme Yol Haritası

Bu doküman, T.C. Resmî Gazete'yi günlük olarak tarayan, şirketin faaliyet alanı/büyüklük/sektör profiline göre filtreleyen ve iç denetim/uyum için pratik etki analizi raporları üreten **MCP (Model Context Protocol)** tabanlı projenin tüm teknik isterlerini ve geliştirme adımlarını içerir.

---

## 📌 1. Proje Vizyonu ve Temel İlkeler
* **Yalınlık & Yüksek Etki:** Gereksiz karmaşıklıktan (over-engineering) kaçınılmış, doğrudan sonuca odaklı hafif bir Python mimarisi.
* **Akıllı Eşleştirme (Company-Aware):** Kararlar genel özetlenmez; şirketin NACE kodları, cirosu, tabi olduğu kurumlar ve operasyonel risklerine göre filtrelenir.
* **İç Denetçi Perspektifi:** Çıktılar salt hukuki metin değil; risk derecesi, cezai yaptırım, etkilenen departman ve denetim kontrol listesi (checklist) sunar.
* **MCP Standart Uyumu:** Hem Claude Desktop / Antigravity IDE gibi yapay zeka ajanlarıyla interaktif çalışır, hem de periyodik cron scriptiyle bağımsız rapor üretebilir.

---

## 🧠 2. Sequential Thinking Analizi (Tasarım Mantığı)

1. **Adım 1 - Veri Çekme (Ingestion):**
   * Resmî Gazete fihristi `https://www.resmigazete.gov.tr/` üzerinden günlük olarak çekilir.
   * Yürütme/İdare Bölümü (Yönetmelikler, Tebliğler, Kurul Kararları, Cumhurbaşkanı Kararları) ve Yargı Bölümü öncelikli taranır.
   * İlan bölümleri (ihale, şirket ilanları vb.) kural olarak elenerek gereksiz veri yükü engellenir.

2. **Adım 2 - Şirket Profilleme & Ön Filtreleme (Triyaj):**
   * Her kararın başlığı ve yayınlayan kurumu, `company_profile.yaml` dosyasındaki sektörler, düzenleyiciler ve anahtar kelimelerle taranır.
   * *Örnek:* Şirket finans/fintek alanındaysa BDDK/SPK/TCMB kararları anında "Yüksek İlgi" olarak işaretlenir.

3. **Adım 3 - Derin İçerik Okuma & LLM Analizi:**
   * Ön filtreyi geçen kararların detay sayfaları/metinleri çekilir.
   * Yapay zeka modeli yapılandırılmış bir prompt ile 5 boyutlu iç denetim analizini gerçekleştirir.

4. **Adım 4 - Raporlama & Arşivleme:**
   * Çıktılar günlük tarihli Markdown ve HTML bülten formatında `reports/YYYY-MM-DD.md` klasörüne arşivlenir.

---

## 🏗️ 3. Proje Klasör Mimarisi

```text
mevzuat-radari/
├── config/
│   └── company_profile.yaml       # Şirketin faaliyet alanı, ölçeği ve kural parametreleri
├── src/
│   ├── __init__.py
│   ├── scraper.py                 # Resmî Gazete fihrist ve metin çekme modülü
│   ├── evaluator.py               # Profil eşleştirme, alaka puanlama ve LLM analiz mantığı
│   ├── templates.py               # Günlük denetim bülteni şablonları (Markdown / HTML)
│   └── server.py                  # FastMCP protokolü araç ve kaynak sağlayıcısı
├── reports/                       # Üretilen günlük denetim raporlarının arşivi
├── run_daily_audit.py             # Tek komutla günlük tarama ve rapor üretme CLI aracı
├── requirements.txt               # Bağımlılıklar
└── README.md                      # Kurulum ve hızlı başlangıç rehberi
```

---

## 📋 4. Şirket Profilleme Formatı (`config/company_profile.yaml`)

```yaml
company_profile:
  general:
    name: "Örnek Şirket A.Ş."
    legal_type: "Anonim Şirket"
    scale: "Büyük Ölçekli"           # KOBİ / Büyük Ölçekli / Halka Açık
    employee_count: 500
    annual_turnover_tl: "250M+"      # KVKK, Bağımsız Denetim vb. eşikler için
    is_publicly_traded: false

  sectors_and_nace:
    primary_sector: "Perakende & E-Ticaret"
    secondary_sectors:
      - "Lojistik & Depolama"
      - "Fintek / Ödeme Sistemleri"
    nace_codes:
      - "47.91.00"
      - "52.29.00"

  regulatory_bodies:
    - "Ticaret Bakanlığı"
    - "Hazine ve Maliye Bakanlığı (GİB)"
    - "KVKK"
    - "TCMB"
    - "Çalışma ve Sosyal Güvenlik Bakanlığı"

  operational_traits:
    has_foreign_trade: true          # Gümrük / Kambiyo mevzuatı takibi
    has_rd_center: true              # 5746 sayılı Ar-Ge teşvikleri takibi
    uses_subcontractors: true        # Taşeron / İş hukuku riskleri
    e_commerce_license: true         # ETBİS / Mesafeli Sözleşmeler takibi

  risk_priorities:
    tax_and_finance: "Kritik"
    labor_and_sgk: "Yüksek"
    data_privacy_kvkk: "Kritik"
    commercial_and_consumer: "Yüksek"
```

---

## 🛠️ 5. MCP Sunucusu Araçları (Tools & Resources)

| Araç Adı | Parametreler | Görevi |
| :--- | :--- | :--- |
| `get_company_profile` | Yok | Mevcut şirket profilini ve risk önceliklerini döner. |
| `fetch_gazette_index` | `date` (Opsiyonel, YYYY-MM-DD) | Belirtilen günün fihristini yapılandırılmış liste olarak çeker. |
| `get_regulation_content` | `url` (Zorunlu) | İlgili tebliğ/karar metnini temiz metin/Markdown olarak getirir. |
| `evaluate_daily_gazette` | `date`, `min_relevance_score` | Günü şirket profiliyle eşleştirir, LLM ile analiz eder ve denetim raporu üretir. |

---

## 📊 6. Üretilecek Günlük Denetim Raporu Şablonu

```markdown
# 🏛️ Resmî Gazete Günlük İç Denetim & Uyum Bülteni
**Tarih:** 29 Ağustos 2026 | **Sayı:** 32xxx | **Taranan Madde:** 24 | **İlgili Bulunan:** 2

---

### 🔴 [Kritik] Mesafeli Sözleşmeler Yönetmeliğinde Değişiklik Yapılmasına Dair Yönetmelik
* **Kurum:** Ticaret Bakanlığı
* **Alaka Skoru:** %95 (E-Ticaret ve Tüketici Hakları Faaliyet Alanı Eşleşmesi)
* **Yürürlük Tarihi:** 01.10.2026

#### 📝 Yönetici Özeti
Tüketici iadelerinde kargo masraflarının satıcı tarafından karşılanması zorunluluğuna ilişkin istisnalar yeniden düzenlendi. Ön bilgilendirme formlarında cayma hakkı metninin güncellenmesi zorunlu kılındı.

#### ⚠️ Risk & Cezai Yaptırım
Uyumsuzluk halinde her bir tüketici işlemi için 6502 sayılı Kanun uyarınca idari para cezası ve ETBİS nezdinde idari yaptırım riski.

#### 🏢 Etkilenen Departmanlar
* E-Ticaret Operasyon, Hukuk & Uyum, Müşteri Hizmetleri, IT/Yazılım

#### ✅ İç Denetim Kontrol Listesi (Aksiyonlar)
- [ ] Web sitesi ve mobil uygulama mesafeli satış sözleşmesi şablonlarının revize edilmesi.
- [ ] Müşteri hizmetleri iade prosedür dokümanının güncellenmesi.
- [ ] Çağrı merkezi kayıtlarının yeni iade politikasına göre denetlenmesi.
```

---

## 🚀 7. Adım Adım Uygulama Yol Haritası

1. **Aşama 1: Çekirdek Kütüphaneler & Scraper (`src/scraper.py`)**
   * `httpx` ve `beautifulsoup4` ile Resmî Gazete fihristini çeken, bölümlere ayıran ve karar metinlerini temizleyen fonksiyonların yazılması.
2. **Aşama 2: Şirket Profili & Eşleştirme Motoru (`src/evaluator.py`)**
   * `company_profile.yaml` okuyucusu ve anahtar kelime/düzenleyici kurum bazlı filtreleme mantığının kurulması.
3. **Aşama 3: FastMCP Sunucusu (`src/server.py`)**
   * Tool ve Resource tanımlarının `FastMCP` ile protokole bağlanması.
4. **Aşama 4: Raporlama & CLI Scripti (`run_daily_audit.py`)**
   * Tek komutla günün gazetesini tarayıp `reports/` altına Markdown rapor kaydeden çalıştırılabilir scriptin hazırlanması.
5. **Aşama 5: Test & Doğrulama**
   * Gerçek bir Resmî Gazete sayısı üzerinde uçtan uca test çalıştırılması.
