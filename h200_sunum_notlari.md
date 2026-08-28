# NVIDIA H200 ile Kurum İçi Yapay Zeka Dağıtım ve İç Denetim Strateji Dokümanı

> **Donanım Özeti:** 1x NVIDIA H200 (141 GB HBM3e VRAM, 4.8 TB/s Bant Genişliği)  
> **Hedef Donanım Varış Tarihi:** Ocak 2027  
> **Hazırlık Dönemi:** Eylül 2026 – Aralık 2026 (4 Ay)

---

## 1. Multi-LoRA Mimarisi (Ana Model + Uzman Adaptörler)
**"Tek Bir Güçlü Motor, Onlarca Departman Uzmanı"**

### Çalışma Prensibi
VRAM belleğine 1 adet güçlü temel model (Base Model — örn. Llama 3.3 70B veya Qwen 2.5 32B) sabit olarak yüklenir. Farklı departmanların ihtiyaçlarına göre eğitilmiş çok hafif LoRA (Low-Rank Adaptation) adaptörleri (her biri ~50 MB - 200 MB) ana modelin üzerine dinamik olarak takılır.

* **Kapasite:** Tek GPU üzerinde **30 – 50+ farklı kurum içi uzman yapay zeka** eşzamanlı çalışabilir.
* **Örnek Yapı:**
  * **Temel Model:** Llama 3.3 70B (FP8 / ~75 GB VRAM)
  * **Adaptörler:**
    * Hukuk & Sözleşme İnceleme LoRA (~100 MB)
    * İK & İç Yönetmelik LoRA (~100 MB)
    * Kurum İçi Yazılım Standartları LoRA (~150 MB)
    * Mali İşler & Muhasebe LoRA (~100 MB)

### Avantajları
* **Maksimum VRAM Verimliliği:** Her departman için ayrı 70B model kurmak yerine tek model üzerinden onlarca farklı görev yürütülür.
* **Düşük Maliyet ve Hızlı Geliştirme:** Yeni bir departman eklendiğinde sadece küçük bir adaptör eğitilir; sunucuya ekstra yük binmez.
* **Sıfır Gecikmeli Geçiş:** Kullanıcı isteğine göre anında ilgili adaptör devreye girer.

### Kısıtları & Dikkat Edilmesi Gerekenler
* Tüm departmanlar aynı temel model mimarisine (örneğin hepsi Llama tabanlıysa) bağlı kalmak zorundadır.
* Farklı diller veya tamamen farklı mimariler (örneğin aynı anda bir Vision modeli ile bir Text modeli) tek LoRA altında birleştirilemez.

---

## 2. Donanımsal İzolasyon: NVIDIA MIG (Multi-Instance GPU)
**"Tek Donanımı Birden Fazla Bağımsız Sanal GPU'ya Bölme"**

### Çalışma Prensibi
NVIDIA Hopper mimarisinin sunduğu MIG özelliği sayesinde, tek bir H200 fiziksel olarak **7 adede kadar tamamen izole edilmiş bağımsız sanal GPU örneğine (instance)** bölünür. Her dilimin kendi ayrılmış VRAM'i, bellek bant genişliği ve CUDA çekirdekleri bulunur.

* **Kapasite:** **7 farklı bağımsız model** (Örn. her biri ~20 GB VRAM alanına sahip 7x 8B model).
* **Örnek Yapı:**
  * Dilim 1-2 (40 GB): Ar-Ge / Yazılım Ekibi için 14B Kodlama Modeli
  * Dilim 3 (20 GB): Müşteri Hizmetleri Chatbot (8B)
  * Dilim 4 (20 GB): Hukuk Departmanı Doküman Analiz Modeli (8B)
  * Dilim 5 (20 GB): Kurum İçi Arama / RAG Embedding Sunucusu
  * Dilim 6-7 (40 GB): Veri Analitiği ve Raporlama Modeli (14B)

### Avantajları
* **Donanımsal SLA ve Performans Garantisi:** Bir departman sunucuyu yoğun sorgularla kilitlese bile diğer departmanların performansı ve yanıt süresi asla etkilenmez.
* **Tam Güvenlik ve İzolasyon:** Farklı gizlilik seviyesindeki birimlerin verileri ve bellek alanları birbirinden fiziksel olarak yalıtılır.
* **Farklı Framework Desteği:** Her dilimde farklı yazılım yığınları (vLLM, TGI, PyTorch, Ollama) bağımsız çalıştırılabilir.

### Kısıtları & Dikkat Edilmesi Gerekenler
* GPU bölündüğünde tek parça dev modeller (örneğin 70B model ~75 GB VRAM ister) bu dilimlere sığmaz. Bölme kararı verildiğinde her dilim maksimum ~20 GB veya ~40 GB sınırında kalır.

---

## 3. Dinamik Multi-Model Serving (vLLM / Triton Inference Server)
**"Esnek Kaynak Havuzu ve Uçtan Uca Kurumsal RAG Paketi"**

### Çalışma Prensibi
H200'ün 141 GB VRAM'i bölünmeden tek bir büyük bellek havuzu olarak kullanılır. Modern çıkarım motorları (vLLM, SGLang veya NVIDIA Triton) kurularak, farklı boyut ve görevlerdeki 3-6 farklı model aynı anda VRAM'e yüklenir. PagedAttention teknolojisi ile kullanıcı yoğunluğuna göre dinamik bellek yönetimi yapılır.

* **Kapasite:** **3 – 6 farklı model** + yüzlerce eşzamanlı personel için KV-Cache havuzu.
* **Örnek Kurumsal Paket (İdeal RAG Mimarisi):**
  * **1x 70B Genel Akıl Yürütme & Asistan Modeli:** ~75 GB VRAM
  * **1x 8B Hızlı Kodlama / Yazışma Modeli:** ~12 GB VRAM
  * **1x Embedding Modeli (Kurumsal Doküman İndeksleme):** ~2-3 GB VRAM
  * **1x Reranker Modeli (Arama Doğruluğunu Artırma):** ~2-3 GB VRAM
  * **Kalan ~45-50 GB VRAM:** Eşzamanlı personelin uzun sorguları ve oturumları (KV-Cache) için ayrılır.

### Avantajları
* **Eksiksiz RAG Entegrasyonu:** Kurum içi doküman arama, yeniden sıralama ve cevap üretme bileşenlerinin tamamı tek kartta eksiksiz çalışır.
* **Dinamik Bellek Kullanımı:** Hangi modele talep çoksa bellek ve işlem gücü oraya otomatik kaydırılır.
* **Maksimum Donanım Verimliliği:** Hiçbir CUDA çekirdeği veya VRAM alanı boşta kalmaz.

### Kısıtları & Dikkat Edilmesi Gerekenler
* Yoğun kullanım anlarında (çok sayıda personelin aynı anda uzun dokümanlar yüklemesi) KV-Cache dolabilir ve kuyruk oluşabilir. Doğru kuyruk ve rate-limit yönetimi gerektirir.

---

## 📊 Dağıtım Yöntemleri Karşılaştırma Tablosu

| Yöntem | Model Çeşitliliği | İzolasyon Seviyesi | VRAM Verimliliği | İdeal Kullanım Alanı |
| :--- | :---: | :---: | :---: | :--- |
| **Multi-LoRA** | Çok Yüksek (30-50+) | Mantıksal | ⭐⭐⭐⭐⭐ (En Yüksek) | Birçok departmana özel uzman asistanlar üretmek |
| **NVIDIA MIG** | Sabit (Max 7) | Donanımsal (Tam İzolasyon) | ⭐⭐⭐ (Orta) | Birbirinden bağımsız, SLA garantili departman hizmetleri |
| **vLLM / Triton** | Dengeli (3-6 Farklı Model) | Yazılımsal Havuz | ⭐⭐⭐⭐ (Yüksek) | Kurum içi RAG (Doküman Arama) + Genel Asistan paketi |

---

## 4. Kurumsal Veri Erişimi ve Yetkilendirme Güvenliği (RBAC / ABAC)

> **Kritik İlke:** Güvenlik ve yetkilendirme kararları **ASLA yapay zeka modeline veya prompt'a bırakılamaz**. Güvenlik, arama ve veri getirme (Retrieval/Gateway) katmanında **deterministik (kodlanmış kurallarla)** çözülmelidir.

### A. Modeller Veriye Nasıl Erişir?
1. **RAG & Vektör Veritabanları (Milvus, Qdrant, PGVector):** Kurum içi dokümanlar (PDF, Word, Confluence vb.) metin parçalarına (chunks) ayrılır, vektörleştirilir ve saklanır. Soru sorulduğunda yalnızca ilgili parçalar çekilir.
2. **Fonksiyon Çağrısı (Function / Tool Calling):** Model doğrudan veritabanına bağlanmaz. İhtiyaç duyduğunda kurumun tanımladığı güvenli API uç noktalarını (REST/gRPC) tetikler.

### B. Yetkisiz Bilgi İfşası (Generative Leakage) Nasıl Engellenir?
* **1. Metadata-Based ACL Filtering (Doküman Düzeyi Güvenlik):**
  * Dokümanlar indekslenirken kaynak sistemdeki yetkiler (`allowed_roles: ["ik_muduru", "ik_uzmani"]`, `classification: "gizli"`, `tenant_id`) metadata olarak vektör veritabanına kaydedilir.
  * Kullanıcı arama yaptığında sistem **Pre-filtering** uygular: Kullanıcının yetkisi olmayan hiçbir parça veritabanından çekilmez; dolayısıyla model bu bilgiyi **asla görmez**.
* **2. Identity Propagation (Kimlik Aktarımı / On-Behalf-Of):**
  * Kullanıcının SSO / Active Directory / Keycloak kimlik belirteci (JWT/OAuth) veri katmanına kadar taşınır. Model ortak bir "Admin/Root" kullanıcısı ile değil, **sorguyu yapan personelin yetkisiyle** API ve veritabanlarına bağlanır.
* **3. Fine-Grained Authorization (FGA - OpenFGA / Cerbos):**
  * Dinamik ve ilişkisel izin kontrolleri (ReBAC) için kurumsal yetkilendirme motorları entegre edilir.
* **4. Deny-by-Default (Varsayılan Olarak Reddet):**
  * Erişim etiketi veya yetki tanımı bulunmayan/hatalı olan hiçbir doküman arama sonuçlarına dahil edilmez.
* **5. AI Güvenlik Duvarı (NeMo Guardrails / Llama Guard):**
  * Prompt Injection saldırılarını ve sistem talimatlarını aşma girişimlerini filtreler.

---

## 5. Halüsinasyon Takibi ve Gözlemlenebilirlik (LLM Observability)

> **Amaç:** Modelin kafasından uydurduğu, kaynak dokümanda yer almayan hatalı bilgileri (hallucination) anlık olarak yakalamak ve ölçmek.

### A. Canlı Üretim Ortamı İzleme (Online Observability)
* **Kullanılan Araçlar:** **Arize Phoenix**, **Langfuse**, **TruLens**, **OpenInference**.
* **RAG Triad (RAG Üçlüsü) Metrikleri:**
  1. **Groundedness (Kaynak Uyumu / Doğruluk):** Üretilen yanıtın, sistemden çekilen dokümanlara ne kadar sadık kaldığı anlık ölçülür (% skoru verilir).
  2. **Context Relevance (Bağlam Uygunluğu):** Veritabanından gelen dokümanların kullanıcının sorusuyla gerçekten alakalı olup olmadığı denetlenir.
  3. **Answer Relevance (Yanıt Uygunluğu):** Modelin cevabının sorunun amacına hizmet edip etmediği kontrol edilir.
* **NLI (Doğal Dil Çıkarımı) & LLM-as-a-Judge:**
  * Hafif ve hızlı bir denetçi model (örn. Vectara HHEM), üretilen metni kaynak metinle anlık kıyaslar. Kaynaktan sapma tespit edilirse yanıt kullanıcıya gösterilmeden engellenir ("Belirtilen kaynakta bu bilgi bulunamadı" denir).

### B. Çevrimdışı Kalite Testleri (Offline CI/CD Evaluation)
* **Kullanılan Araçlar:** **DeepEval**, **Ragas**.
* **Nasıl Çalışır?** 
  * Kuruma ait 100-500 adet onaylı soru-cevap çiftinden oluşan "Altın Doğruluk Kümesi" (Golden Dataset) hazırlanır.
  * Model veya sistem güncellendiğinde bu test seti otomatik koşturulur. Halüsinasyon skoru eşik değerin altına düşerse sistem canlıya alınmaz (Yazılım dünyasındaki Unit Test mantığı).

---

## 6. Kaynak Takibi, Atıf (Citation) ve Veri Soykütüğü (Data Lineage)

> **Soru:** "Model bu cevabı verirken tam olarak hangi dokümanın, hangi sayfasına ve hangi paragrafına bakarak verdi? Bunu nasıl belgeler ve kullanıcıya gösteririz?"

### A. Kullanıcı Arayüzü İçin Atıf Motorları (Citation Engines)
Kullanıcının gördüğü yanıtta doğrudan kaynak gösterimi ve tıklanabilir referanslar sağlayan yapılar:
* **LlamaIndex `CitationQueryEngine` & Haystack Document Store:**
  * Model ürettiği cümlenin sonuna otomatik olarak dipnot numarası ekler: `...yıllık izin süresi 20 gündür [1].`
  * Yanıtın altında referans kartı açılır:
    * `[1] Kaynak: 2025_IK_Yonetmeligi.pdf (Sayfa 14, Paragraf 3 - Benzerlik Skoru: %94)`
* **Metadata & Chunk Lineage:**
  * Vektör veritabanına veri atılırken dosya adı, sayfa numarası, oluşturulma tarihi, yazar ve orijinal metin paragrafı metaveri olarak saklanır. Arayüzde kullanıcı "Kaynağı Göster" butonuna bastığında orijinal PDF'in ilgili sayfası ekranda vurgulanmış (highlighted) olarak açılır.

### B. Yönetici & Denetim İçin Arka Plan İzleme Araçları (Traceability / Audit Trail)
* **1. Langfuse (Açık Kaynak & Kurum İçi On-Premise Kurulabilir):**
  * Tüm sistemin "röntgenini" çeker. Bir personel soru sorduğunda:
    * Kullanıcının sorduğu ham soruyu,
    * Vektör veritabanından çekilen tüm doküman parçalarını (chunk'ları),
    * Bu parçaların kaynak dosya adlarını ve getirilme milisaniyelerini,
    * Modele giden birleştirilmiş prompt'u ve modelin ürettiği cevabı tek bir **Trace ID** altında zincirleme gösterir.
* **2. Arize Phoenix (OpenTelemetry / OpenInference Standardı):**
  * Kurumsal OpenTelemetry loglama standardına sahiptir.
  * Hangi cümlenin hangi doküman parçasından türetildiğini renkli haritalandırma ile görselleştirir (Span-level tracking).

### C. Kurumsal ve Yasal Kazanımlar (Sunum İçin Vurgu Noktası)
1. **Denetim ve İspat Edilebilirlik (KVKK / ISO 42001 / EU AI Act):**
   * Yapay zekanın kurum içinde personele verdiği her tavsiyenin ve bilginin hangi resmi şirket dokümanına dayandığı geriye dönük **%100 kanıtlanabilir** (Audit Log) hale gelir.
2. **Kullanıcı Doğrulama Kolaylığı:**
   * Personel "Yapay zeka uydurdu mu?" şüphesine kapılmadan doğrudan atıf yapılan orijinal resmi belgeye tıklayarak bilgiyi teyit edebilir.

---

## 7. İç Denetim İçin Açık Kaynaklı Yapay Zeka Projeleri & Entegrasyon Mimarileri

İç Denetim fonksiyonunun ihtiyaçlarına göre projeler **hızlı kazanım (Quick Win)**, **operasyonel getiri (ROI)** ve **teknik karmaşıklık** kriterlerine göre önceliklendirilmiştir:

### 🏆 Proje Önceliklendirme Matrisi

| Öncelik Sırası | Proje Adı | Odak Alanı | Uygulama Kolaylığı | Denetim Katkısı / ROI | Canlıya Alma Zamanı |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **1. Öncelik** | **`ContractGuard` / `ClauseGuard`** | Sözleşme, Şartname & Mevzuat Denetimi | ⭐⭐⭐⭐⭐ (Kolay - RAG) | 🚀🚀🚀🚀🚀 (Hızlı Kazanım) | **Şubat 2027** |
| **2. Öncelik** | **`FraudDetection-LLM`** | Mali Hareketler, Masraf & Suiistimal | ⭐⭐⭐⭐ (Orta - SQL/ERP) | 🚀🚀🚀🚀🚀 (Yüksek Mali Etki) | **Mart - Nisan 2027** |
| **3. Öncelik** | **`LangGraph Multi-Agent Audit`** | Otonom Çalışma Kağıdı & Raporlama | ⭐⭐⭐ (İleri Ajan Mimarisi) | 🚀🚀🚀🚀 (Rapor Süresi %80 Azalır) | **Mayıs - Haziran 2027**|
| **4. Öncelik** | **`FinAI` / `FinRobot`** | Mali Tablo, Bilanço & Dipnot Çapraz Kontrol | ⭐⭐⭐ (Orta - Veri Entegrasyonu) | 🚀🚀🚀 (Makro Finansal Riskler) | **Temmuz - Ağustos 2027** |
| **5. Öncelik** | **`OpenLane` / `Admyral`** | GRC & 7/24 Sürekli Kontrol İzleme (CCM) | ⭐⭐ (Zor - Kurum Çapı API) | 🚀🚀🚀🚀 (Sürekli Güvence) | **2027 Son Çeyrek** |

---

### Proje 1: `ContractGuard & ClauseGuard` (1. Öncelik - Quick Win)
* **Odak Alanı:** Sözleşmelerin şirket satın alma yönetmeliğine, yetki matrislerine ve kanunlara uygunluğunun taranması.
* **Beslendiği Kaynaklar:** Satın alma sözleşmeleri (PDF/Word/OCR), Şirket Satın Alma Prosedürü, İmza Sirküleri Yetki Limitleri.
* **Denetçiye Katkısı:** Örneklem seçmek yerine yılda imzalanan yüzlerce sözleşmenin **%100'ünü dakikalar içinde tarar**; dengesiz cezai şartları ve yetkisiz onayları kırmızı bayrakla (**Red Flag**) listeler.

#### Entegrasyon Mimarisi (Sözleşme Denetimi):
```
[Arşiv / SharePoint / SAP] -> (PDF Sözleşmeler)
         |
         v
[openreview-cli / Presidio] -> (KVKK / PII Maskeleme - Yerel)
         |
         v
[LlamaIndex + Qdrant Vector DB] -> (Mevzuat & Standart Şartname Eşleme)
         |
         v
[H200: Llama 3.3 70B (LoRA: Hukuk)] -> (Madde Bazlı Uyumsuzluk & Risk Analizi)
         |
         v
[Çıktı:] Denetim Çalışma Kağıdı (Madde Madde Kırmızı Bayraklar ve Uyumsuzluk Tablosu)
```

---

### Proje 2: `FraudDetection-LLM-Integration` (2. Öncelik - Mali Denetim)
* **Odak Alanı:** Masraf formları, mükerrer faturalar, limit altı parçalanmış ödemeler (smurfing) ve şüpheli tedarikçi hareketleri.
* **Beslendiği Kaynaklar:** SAP/Oracle Yevmiye Tabloları (`BKPF`, `BSEG`), Masraf Giriş Sistemi, Banka MT940 Ekstreleri.
* **Denetçiye Katkısı:** Sayısal anomali tespiti (Isolation Forest/XGBoost) ile yerel LLM'in mantık yürütmesini birleştirir. Sadece sayıları listelemez; **"Bu işlem neden şüpheli, hangi şirket kuralı delinmiş?"** açıklamasını metin olarak sunar.

#### Entegrasyon Mimarisi (Mali Suiistimal Denetimi):
```
[SAP / Oracle ERP Veritabanı] -> (SQL Extraction / Batch CSV)
         |
         v
[Makine Öğrenmesi Motoru] -> (Isolation Forest Anomali Skoru & Filtreleme)
         |
         v
[H200: Qwen 2.5 32B / Llama 70B] -> (Bağlam Eşleme: Harcama Açıklaması + Satıcı + Personel Profili)
         |
         v
[Çıktı:] Gerekçeli Şüpheli İşlem Raporu ("X Personeli hafta sonu limit altı 3 parçada fatura kesmiş")
```

---

### Proje 3: `LangGraph Multi-Agent Audit Framework` (3. Öncelik - Otonom Raporlama)
* **Odak Alanı:** Denetim saha çalışmasının simülasyonu, bulguların çapraz doğrulanması ve IIA standartlarında resmi denetim raporu yazımı.
* **Beslendiği Kaynaklar:** Denetim kanıtları, saha çalışma notları, risk kontrol matrisleri (RCM), kurum içi yönergeler.
* **Denetçiye Katkısı:** Rapor yazım süresini %80 kısaltır. 5C kuralına (**Criteria, Condition, Cause, Consequence, Corrective Action**) uygun kusursuz taslak raporlar üretir.

#### Entegrasyon Mimarisi (Çok Ajanlı Denetim Ekibi):
```
[Denetim Veri Havuzu]
         |
         v
[Ajan 1: Junior Auditor] -> (Kanıtları Toplar, İlk İhlalleri Çıkarır)
         |
         v
[Ajan 2: Compliance Auditor] -> (Kurum Yönergesi ve Kanun Maddesi ile Eşleştirir)
         |
         v
[Ajan 3: Critic / QA Auditor] -> (Bulguyu Sorgular: "Kanıt yeterli mi? Halüsinasyon var mı?")
         |
         v
[Ajan 4: Lead Auditor (Raporlama)] -> (Resmi IIA Formatında 5C Denetim Raporu Üretir)
```

---

### Proje 4: `FinAI / FinRobot` (4. Öncelik - Mali Tablo & Rapor Denetimi)
* **Odak Alanı:** Bilanço, gelir tablosu, mizan ve faaliyet raporlarındaki çapraz tutarsızlıklar ve finansal oran sapmaları.
* **Beslendiği Kaynaklar:** Ayrıntılı Mizan (Trial Balance), Bilanço Dipnotları (PDF/Excel), KAP/Faaliyet Raporları.
* **Denetçiye Katkısı:** Bilanço rakamları ile dipnotlar arasındaki gizli tutarsızlıkları saniyeler içinde yakalar.

---

### Proje 5: `OpenLane / Admyral` (5. Öncelik - Sürekli Kontrol İzleme)
* **Odak Alanı:** Görevler Ayrılığı (SoD) ihlalleri, Active Directory yetki değişimleri, ISO 27001/BDDK kontrolleri.
* **Beslendiği Kaynaklar:** Active Directory, İK Çıkış Listeleri, Bulut Altyapı API'leri, Güvenlik Logları.
* **Denetçiye Katkısı:** Yıllık denetim yerine 7/24 "Sürekli Denetim" (Continuous Auditing) sağlar.

---

## 8. İç Denetim İçin Stratejik Yol Haritası (Roadmap)

```mermaid
gantt
    title H200 Öncesi ve Sonrası İç Denetim Yapay Zeka Yol Haritası
    dateFormat  YYYY-MM
    section Hazırlık Dönemi (2026)
    Veri Envanteri & Yetki Haritası      :2026-09, 1M
    Sandbox Testleri & Altın Veri Seti   :2026-10, 1M
    Prompt Kütüphanesi & Şablonlar       :2026-11, 1M
    KVKK Maskeleme & Altyapı Hazırlığı   :2026-12, 1M
    section Dağıtım & Canlı (2027)
    H200 Kurulumu & Temel Modeller       :2027-01, 1M
    Faz 1: Sözleşme Denetimi (ContractGuard) :2027-02, 1M
    Faz 2: Mali Fraud Denetimi (ERP Entegrasyonu) :2027-03, 2M
    Faz 3: Çok Ajanlı Raporlama (LangGraph) :2027-05, 2M
    Faz 4: 7/24 Sürekli Kontrol İzleme (CCM) :2027-07, 4M
```

---

### 📅 AŞAMA 1: H200 Öncesi 4 Aylık Hazırlık Dönemi (Eylül – Aralık 2026)

H200 donanımı gelmeden önce iç denetim ekibinin veri ve metodoloji hazırlığını tamamlaması gerekir:

#### 1. Eylül 2026: Veri Envanteri, Denetim Evreni ve Yetki Haritalama
* **Amaç:** Hangi denetim verilerinin yapay zekaya besleneceğinin ve erişim sınırlarının belirlenmesi.
* **Aksiyonlar:**
  * İç Denetim arşivindeki geçmiş 3 yılın sözleşmeleri, satın alma prosedürleri, imza yetki sirküleri ve yönergeler derlenir.
  * ERP (SAP/Oracle) tarafında Yevmiye Defteri (`BSEG`/`BKPF`), satıcı master datası ve masraf tablolarının şemaları çıkarılır.
  * **RBAC Matrisi:** Hangi denetçinin hangi seviyedeki gizli verilere (Örn: Yönetici bordroları, M&A sözleşmeleri) erişebileceğinin yetki haritası çıkarılır.

#### 2. Ekim 2026: Küçük Ölçekli Sandbox Testleri & "Altın Test Kümesi" (Golden Dataset)
* **Amaç:** Açık kaynaklı kütüphanelerin mevcut CPU / test sunucularında denenmesi ve test veri seti hazırlanması.
* **Aksiyonlar:**
  * Küçük açık kaynak modeller (Llama 3.1 8B, Qwen 7B) mevcut test ortamına kurulur.
  * **Altın Test Kümesi Hazırlığı:** Geçmişte tespit edilmiş 50 gerçek denetim bulgusu (20 sözleşme açığı, 20 şüpheli masraf, 10 mevzuat ihlali) referans veri seti olarak etiketlenir. (Model canlıya alındığında bu test setiyle başarısı ölçülecektir).
  * `Ragas` ve `DeepEval` kütüphaneleri kurularak halüsinasyon test scriptleri yazılır.

#### 3. Kasım 2026: Denetim Prompt Kütüphanesi & Çalışma Kağıdı Şablonları
* **Amaç:** Yapay zekaya verilecek kurumsal denetim talimatlarının ve çıktı formatlarının standartlaştırılması.
* **Aksiyonlar:**
  * **Sözleşme Denetim Kuralları:** *"Sözleşmede vade 60 günü aşıyorsa uyar"*, *"Cezai şart tek taraflı ise kırmızı bayrak kaldır"* gibi 100+ kural prompt şablonuna dökülür.
  * **IIA Uyumlu Rapor Şablonu:** 5C formatındaki resmi çalışma kağıdı Markdown/Word şablonları hazırlanır.
  * `LlamaIndex` tabanlı atıf (citation) motorunun prototip konfigürasyonu tamamlanır.

#### 4. Aralık 2026: Veri Güvenliği, Maskeleme (PII/KVKK) Pipeline'ı & BT Koordinasyonu
* **Amaç:** Veri mahremiyeti altyapısının kurulması ve H200 sunucusu için sistem odası hazırlığı.
* **Aksiyonlar:**
  * `Microsoft Presidio` veya `openreview-cli` yerel maskeleme motoru kurulur; isim, TC kimlik no, kredi kartı ve IBAN bilgilerini otomatik maskeleyen regex/NLP pipeline'ı yazılır.
  * BT ve Sistem Altyapı ekibi ile sunucu kabini, güç gereksinimleri, kurumsal ağ izolasyonu ve CUDA/Docker ortamları planlanır.

---

### 🚀 AŞAMA 2: H200 Geldikten Sonra Entegrasyon Yol Haritası (Ocak 2027 ve Sonrası)

#### 1. Ocak 2027: Altyapı Kurulumu ve Temel Modellerin Yerleştirilmesi
* **H200 Devreye Alma:** Ubuntu Server + NVIDIA CUDA + Docker + vLLM çıkarım motoru kurulur.
* **Model Dağıtımı:**
  * **1x Llama 3.3 70B (FP8):** Ana Akıl Yürütme ve Raporlama Modeli (~75 GB VRAM)
  * **1x Qwen 2.5 32B:** Kodlama ve Veri Analiz Modeli (~32 GB VRAM)
  * **1x BGE-M3:** Çok Dilli Embedding Modeli (Kurumsal Doküman İndeksleme) (~2.5 GB VRAM)
  * **1x BGE-Reranker:** Arama Doğruluğu Filtresi (~2.5 GB VRAM)
* **Gözlemlenebilirlik:** `Langfuse` ve `Arize Phoenix` yerel konteyner olarak ayağa kaldırılır.

#### 2. Şubat 2027 (Faz 1 - Quick Win): Sözleşme ve Mevzuat Denetiminin Canlıya Alınması
* `ContractGuard` & `ClauseGuard` H200 üzerinde çalıştırılır.
* Tüm iç yönergeler ve 2024-2026 dönemi sözleşmeleri `Qdrant` vektör veritabanına indekslenir.
* **Kazanım:** İç denetçiler web arayüzünden sözleşme yükleyip 30 saniye içinde mevzuata aykırılık raporunu ve atıflı dipnotlarını almaya başlar.

#### 3. Mart – Nisan 2027 (Faz 2): Mali Anomali ve Suiistimal Denetimi (ERP Entegrasyonu)
* `FraudDetection-LLM-Integration` SAP/Oracle yevmiye tablolarına (read-only güvenli servis hesabı ile) bağlanır.
* Günlük masraf formları ve son 1 yıllık yevmiye kayıtları üzerinde anomali taramaları başlatılır.
* **Kazanım:** Denetçilere haftalık *"Şüpheli İşlem ve Suiistimal Risk Bülteni"* otomatik iletilir.

#### 4. Mayıs – Haziran 2027 (Faz 3): Çok Ajanlı Otonom Saha ve Raporlama Ekibi (LangGraph)
* `LangGraph` orkestrasyonu ile 4 sanal denetçi ajanı devreye alınır.
* Saha denetim verileri yüklendiğinde Ajanlar sırasıyla kanıt toplar, mevzuatla eşleştirir, kalite kontrolü yapar ve 5C formatında resmi **Taslak Denetim Raporunu** üretir.
* **Kazanım:** Rapor yazım ve konsolidasyon süresi 2 haftadan 1 güne iner.

#### 5. 2027 2. Yarı (Faz 4): 7/24 Sürekli Kontrol İzleme (CCM / GRC) ve Tam Otonomi
* `OpenLane` ve `Admyral` entegrasyonu tamamlanır.
* Active Directory, İK çıkışları ve sistem erişimleri 7/24 dinlenerek Görevler Ayrılığı (SoD) ve yetki ihlalleri anlık olarak denetim panosuna düşürülür.
* **Kazanım:** Şirket reaktif denetimden **proaktif ve sürekli denetime** tam geçiş sağlar.

---

## 9. Yapay Zeka Modellerinin Denetimi (Model Governance, Security & Red Teaming)

> **İç Denetim İlkesi:** *"Yapay zekayı bir denetim aracı olarak kullanırken, aynı zamanda kurumda çalışan modellerin kendisi de birer iç denetim nesnesidir."* Modellerin güvenliği, tarafsızlığı, yasal uyumu ve veri gizliliği düzenli olarak denetlenmelidir.

### A. Model Güvenliği ve Zaafiyet Taraması (AI Red Teaming)
Modelin saldırganlar veya kötü niyetli kullanıcılar tarafından manipüle edilip edilemediğini test eden araçlar:

* **1. [Garak](https://github.com/leondz/garak) (Yapay Zekanın Güvenlik Tarayıcısı — "Nmap for LLMs"):**
  * **Nasıl Çalışır?** H200 üzerinde çalışan yerel modellere binlerce otomatik siber saldırı vektörü (Jailbreak, Prompt Injection, Model Hijacking, Zehirleme) gönderir.
  * **Denetim Çıktısı:** Modelin hangi güvenlik açıklarına karşı savunmasız kaldığını listeleyen detaylı **Güvenlik Açığı Denetim Raporu** üretir.
* **2. [Microsoft PyRIT](https://github.com/Azure/PyRIT) (Python Risk Identification Tool):**
  * **Nasıl Çalışır?** Çok turlu (multi-turn) gelişmiş saldırıları simüle eder. Bir insan saldırgan gibi modelle sohbet ederek modeli kandırmaya ve şirket politikalarını delmeye çalışır.
* **3. [Promptfoo](https://github.com/promptfoo/promptfoo):**
  * **Nasıl Çalışır?** CI/CD pipeline'ına entegre edilen otomatik güvenlik ve kalite test motorudur. **OWASP Top 10 for LLM** açıklarını periyodik olarak tarar.

### B. Yasal Uyum, Şeffaflık ve Regülasyon Denetimi (Regulatory Compliance)
* **1. [COMPL-AI](https://github.com/compl-ai/compl-ai):**
  * **Nasıl Çalışır?** Modelleri doğrudan **AB Yapay Zeka Yasası (EU AI Act)** ve ISO/IEC 42001 teknik standartlarına göre test eder.
  * **Denetim Çıktısı:** Modelin şeffaflık, risk yönetimi, siber dayanıklılık ve doğruluk skorlarını çıkararak resmi uyumluluk karnesi üretir.
* **2. [OWASP Top 10 for LLM](https://owasp.org/www-project-top-10-for-large-language-model-applications/) Denetim Kontrol Listesi:**
  * `LLM01: Prompt Injection` (Model talimatları bypass edilebiliyor mu?)
  * `LLM02: Sensitive Information Disclosure` (Model gizli verileri sızdırıyor mu?)
  * `LLM06: Excessive Agency` (Modele gereğinden fazla sistem yetkisi verilmiş mi?)
  * `LLM08: Vector and Embedding Weaknesses` (Vektör veritabanı manipüle edilebiliyor mu?)

### C. Önyargı, Ayrımcılık ve Etik Denetimi (Fairness, Bias & Ethics)
Modelin kararlarında (kredi onayı, İK işe alım, tedarikçi değerlendirme vb.) örtülü bir ayrımcılık yapıp yapmadığını denetleyen araçlar:

* **1. [IBM AIF360](https://github.com/Trusted-AI/AIF360) & [Microsoft Fairlearn](https://github.com/fairlearn/fairlearn):**
  * **Nasıl Çalışır?** Modelin ürettiği kararları demografik değişkenlere göre istatistiksel testlere tabi tutar. Cinsiyet, yaş veya unvana dayalı bir ayrımcılık (*Disparate Impact*) olup olmadığını ölçer.
* **2. [Stanford HELM](https://github.com/stanford-crfm/helm) (Holistic Evaluation of Language Models):**
  * Modelin doğruluk, toksisite, sağlamlık ve etik standartlarını bağımsız metriklerle puanlar.

### D. Veri Mahremiyeti ve Gizlilik Denetimi (Data Privacy & PII Leakage)
* **[Microsoft Presidio](https://github.com/microsoft/presidio) & [Guardrails AI](https://github.com/guardrails-ai/guardrails):**
  * **Nasıl Çalışır?** Modelin hem girdi hem çıktı katmanlarını 7/24 denetler. Modelin ürettiği metinlerin içinde personelin TC Kimlik No, telefon, maaş bilgisi veya şirket ticari sırlarının (KVKK/GDPR ihlali) yer almadığını garanti eder.

---

### 📋 İç Denetim İçin Model Denetim Kontrol Paketi (Audit Tool Stack)

| Denetim Alanı | Kullanılacak Araç | Denetim Amacı / Kontrol Noktası | Denetim Periyodu |
| :--- | :--- | :--- | :---: |
| **Siber Güvenlik & Zaafiyet** | **`Garak`** + **`Promptfoo`** | Prompt Injection ve Jailbreak açıklarını taramak | Aylık & Her Model Güncellemesinde |
| **Gelişmiş Saldırı Simülasyonu** | **`Microsoft PyRIT`** | Çok turlu saldırgan simülasyonu ile güvenlik duvarı testi | Çeyreklik (Quarterly) |
| **Yasal & Standart Uyumu** | **`COMPL-AI`** + **`OWASP LLM`** | EU AI Act ve ISO 42001 uyum karnesi çıkarmak | 6 Aylık |
| **Etik & Ayrımcılık** | **`AIF360`** / **`Fairlearn`** | Kararlarda önyargı ve taraflılık tespiti yapmak | Çeyreklik |
| **Veri Sızıntısı & KVKK** | **`Presidio`** / **`Guardrails AI`** | Yanıtlarda kişisel veri/şirket sırrı ifşasını denetlemek | 7/24 Gerçek Zamanlı |
