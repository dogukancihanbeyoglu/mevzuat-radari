# 🏛️ AUDITORIS 2026 — CANLI UI TESTİ VE KAPSAMLI KULLANICI REHBERİ
**Sürüm:** 2026.1 Enterprise  
**Tarih:** 30 Ağustos 2026  
**Standart Uyumu:** IIA Küresel İç Denetim Standartları (2024/2026 Evolution), BDDK, MASAK, KVKK  

---

## 📌 Giriş ve Yönetici Özeti
Bu doküman, **Auditoris Yerel İç Denetim Yapay Zeka Sistemi**'nin 5 temel denetim aşaması ve **10 görev türünün** canlı tarayıcı (`Google Chrome / Playwright`) üzerinde kullanıcıyla birlikte adım adım test edilerek üretilen sonuçlarını, teknik arka plan analizlerini ve operasyonel ekran görüntülerini içermektedir.

Tüm testler yerel donanımda çalışan **Ollama (qwen2.5-coder:7b & llama3.2:3b / deepseek-r1)** modelleri, **PII Maskeleme Motoru**, **ChromaDB Vektör RAG Arama** ve **İzole Python Sandbox** ortamı kullanılarak sıfır bulut veri sızıntısıyla (%100 On-Premise) icra edilmiştir.

---

## 📑 10 Görev Türü Canlı Test ve Analiz Raporu

```
Auditoris 5 Denetim Aşaması & 10 Görev Mimarisi
├── 1. Yıllık Planlama (Annual Planning)
│   ├── [Görev 01] Denetim Evreni ve Risk Derecelendirmesi
│   └── [Görev 02] Kaynak ve Yetkinlik Planlaması (Competency Mapping)
├── 2. Görev Planlama (Engagement Planning)
│   ├── [Görev 03] Risk ve Kontrol Matrisi (RCM) & Walkthrough
│   └── [Görev 04] Görev Kapsam Dokümanı (Engagement Scoping)
├── 3. Saha Çalışması (Fieldwork & Testing)
│   ├── [Görev 05] Kontrol Test Prosedürü Geliştirme
│   ├── [Görev 06] Kontrol Tanımı ve Tasarım Zayıflığı Analizi
│   └── [Görev 07] Yapılandırılmamış Metinden Veri Ayıklama
├── 4. Denetim Raporlama (Reporting)
│   ├── [Görev 08] 5C Standart Denetim Bulgusu Yazımı
│   └── [Görev 09] Yönetim Kurulu ve Denetim Komitesi Özeti
└── 5. Sürekli Denetim & Analitik (Analytics)
    └── [Görev 10] Python (Pandas) İstisna Analiz Kodu & Canlı Sandbox
```

---

### 🚀 GÖREV 01: Denetim Evreni ve Risk Derecelendirmesi
* **Aşama:** 1. Yıllık Planlama (Annual Planning)  
* **Ekran Görüntüsü:** `storage/screenshots/task_01_audit_universe.png`  

#### 1. 🎯 Amaç & Senaryo Girdisi
Anadolu Holding bünyesindeki 5 ana sektör ve 5 iştirak şirketin (Finansman, Enerji, Teknoloji, GYO, Lojistik) 2025 ciroları, regülasyon kapsamları ve geçmiş denetim notları değerlendirilerek 2026 yılı Risk Odaklı Denetim Evreni önceliklendirilmiştir.

#### 2. ⚙️ Arkada Ne Çalıştı?
* **Akıllı Yönlendirme:** `Tier 2 (Standart Analiz & RCM)` ➔ `qwen2.5-coder:7b` (Sıcaklık: 0.2, Max Token: 2048).
* **Vektör RAG Arama:** ChromaDB üzerinden IIA Standart 2026 ve COSO ERM Risk Puanlama ilkeleri sorgulandı.
* **PII Güvenlik Katmanı:** Girdi içindeki kurum ve kişi isimleri SHA-256 Audit Trail altına alındı.
* **Yürütme Süresi:** 113.3 saniye.

#### 3. 🖥️ Arayüzde Yapılan İşlem & 📊 Görülen Sonuç
* Arayüzde aşama ve görev seçilip tablo formatındaki saha verileri yapıştırıldı ve *"Çalışma Kağıdını Üret"* butonuna basıldı.
* Ekrana **Kalite Skoru: 95/100 (Mükemmel - IIA Standartlarında)** rozeti, 5 iştirakin Birleşik Risk Skoru (94, 88, 82, 76, 45 puan) ve Denetim Frekans Dağılımı Tablosu basıldı.

#### 4. 🔍 Çıktılarda İncelenen Detaylar
* `📄 IIA Çalışma Kağıdı`: Word (.docx) ve Excel (.xlsx) indirme butonlarının oluştuğu doğrulandı.
* `🔍 Model Analizi Sekmesi`: Modelin token metrikleri ve yönlendirme gerekçesi incelendi.
* `🔒 Güvenlik & Audit Trail Sekmesi`: JSON veri ağacı ve SHA-256 kriptografik imzası doğrulandı.

---

### 🚀 GÖREV 02: Kaynak ve Yetkinlik Planlaması
* **Aşama:** 1. Yıllık Planlama (Annual Planning)  
* **Ekran Görüntüsü:** `storage/screenshots/task_02_resource_competency_mapping.png`  

#### 1. 🎯 Amaç & Senaryo Girdisi
12 kişilik denetim ekibinin 2026 yılındaki 18 projeyi karşılayabilmesi için Finans, BT, ESG ve Operasyonel yetkinlik açıkları analiz edilerek Dış Kaynak (Outsourcing/Co-Sourcing) stratejisi oluşturulmuştur.

#### 2. ⚙️ Arkada Ne Çalıştı?
* **Akıllı Yönlendirme:** `Tier 2 (Standart Analiz)` ➔ `qwen2.5-coder:7b`.
* **RAG Bilgi Tabanı:** IIA Standart 2030 (Kaynak Yönetimi) ve IIA Standart 2050 (Koordinasyon & Güvence Haritası) bağlamı enjekte edildi.
* **Yürütme Süresi:** 157.7 saniye.

#### 3. 🖥️ Arayüzde Yapılan İşlem & 📊 Görülen Sonuç
* Ekip yetkinlik puanları sisteme girildi. Çıktıda Sürdürülebilirlik/ESG alanındaki 1.2/5.0 yetkinlik açığı için %100 Outsourcing, BT Bulut güvenliği için Co-sourcing bütçe önerileri üretildi.

---

### 🚀 GÖREV 03: Risk ve Kontrol Matrisi (RCM) & Walkthrough
* **Aşama:** 2. Görev Planlama (Engagement Planning)  
* **Ekran Görüntüsü:** `storage/screenshots/task_03_rcm_generation.png`  

#### 1. 🎯 Amaç & Senaryo Girdisi
Mega Enerji Hazine ve Swap İşlemleri sürecinde tespit edilen 3 operasyonel risk (5M USD limit aşımı, SoD görevler ayrılığı ihlali, Stop-Loss manuel devre dışı bırakılması) için kurumsal RCM matrisi ve mülakat soruları hazırlanmıştır.

#### 2. ⚙️ Arkada Ne Çalıştı?
* **Akıllı Yönlendirme:** `Tier 2 (Standart Analiz & RCM)` ➔ `qwen2.5-coder:7b`.
* **RAG Vektör Dayanağı:** COSO İç Kontrol Çerçevesi (Kontrol Faaliyetleri) ve Basel III Hazine İlkeleri.
* **Yürütme Süresi:** 118.5 saniye.

#### 3. 🖥️ Arayüzde Yapılan İşlem & 📊 Görülen Sonuç
* 6 sütunlu RCM Tablosu (Risk No, Risk Tanımı, Kontrol Faaliyeti, Kontrol Türü [Önleyici/Tespit Edici], Sıklık, Test Adımı) ve süreç sahibine yöneltilecek 3 adet derinlemesine Walkthrough mülakat sorusu oluşturuldu.

---

### 🚀 GÖREV 04: Görev Kapsam Dokümanı (Engagement Scoping Memo)
* **Aşama:** 2. Görev Planlama (Engagement Planning)  
* **Ekran Görüntüsü:** `storage/screenshots/task_04_scoping_document.png`  

#### 1. 🎯 Amaç & Senaryo Girdisi
Mega Perakende E-Ticaret ve Pazaryeri Operasyonları denetimi için Kapsam İçi (Sanal POS, fraud, kargo, KVKK) ve Kapsam Dışı (Mağaza sayımları) sınırları belirlenmiştir.

#### 2. ⚙️ Arkada Ne Çalıştı?
* **Akıllı Yönlendirme:** `Tier 2 (Standart Analiz)` ➔ `qwen2.5-coder:7b`.
* **Yürütme Süresi:** 144.7 saniye.

#### 3. 🖥️ Arayüzde Yapılan İşlem & 📊 Görülen Sonuç
* Denetim hedefleri, zaman çizelgesi, kilit paydaşlar ve risk bazlı kapsam sınırları resmi memo formatında üretildi.

---

### 🚀 GÖREV 05: Kontrol Test Prosedürü Geliştirme
* **Aşama:** 3. Saha Çalışması (Fieldwork & Testing)  
* **Ekran Görüntüsü:** `storage/screenshots/task_05_test_procedure.png`  

#### 1. 🎯 Amaç & Senaryo Girdisi
2.500.000 TL üzerindeki faturalarda Çift İmza ve 3'lü Eşleştirme kuralı için 4.200 faturalık evrenden örneklem seçimi ve test planı kurgulanmıştır.

#### 2. ⚙️ Arkada Ne Çalıştı?
* **Akıllı Yönlendirme:** `Tier 2 (Standart Analiz)` ➔ `qwen2.5-coder:7b`.
* **Örneklem Motoru:** Parasal Birim Örneklemesi (Monetary Unit Sampling - MUS) metodolojisi uygulandı.
* **Yürütme Süresi:** 130.0 saniye.

#### 3. 🖥️ Arayüzde Yapılan İşlem & 📊 Görülen Sonuç
* 4-Ögeli Resmi Test Programı üretildi: 1. Amaç, 2. Örneklem Boyutu (25 adet yüksek tutarlı fatura, %95 Güven Düzeyi), 3. SAP ME23N/MIGO/MT-103 Test Adımları, 4. Hata/İstisna Kriteri.

---

### 🚀 GÖREV 06: Kontrol Tanımı ve Tasarım Zayıflığı Analizi
* **Aşama:** 3. Saha Çalışması (Fieldwork & Testing)  
* **Ekran Görüntüsü:** `storage/screenshots/task_06_control_analysis.png`  

#### 1. 🎯 Amaç & Senaryo Girdisi
Hazine uzmanının WhatsApp/telefonla sözlü talimatla 500.000 EUR işlem yapabilmesine izin veren gevşek kontrolün tasarım açıkları analiz edilmiştir.

#### 2. ⚙️ Arkada Ne Çalıştı?
* **Akıllı Yönlendirme:** `Tier 2 (Standart Analiz)` ➔ `qwen2.5-coder:7b`.
* **Yürütme Süresi:** 153.3 saniye.

#### 3. 🖥️ Arayüzde Yapılan İşlem & 📊 Görülen Sonuç
* Kontrolün SoD eksikliği, muğlak volatilite eşiği ve önleyici yerine tespit edici kurgulanması eleştirildi; FIDO2 MFA onaylı sağlamlaştırılmış alternatif kontrol tanımı önerildi.

---

### 🚀 GÖREV 07: Yapılandırılmamış Metinden Veri Ayıklama
* **Aşama:** 3. Saha Çalışması (Fieldwork & Testing)  
* **Ekran Görüntüsü:** `storage/screenshots/task_07_data_extraction.png`  

#### 1. 🎯 Amaç & Senaryo Girdisi
Denetçinin serbest metin saha notlarında geçen dağınık fatura numaraları (OFF-INV-088, OFF-INV-112, INV-ENG-0441), offshore ülkeleri (BVI, Cyprus, İsviçre), tutarlar ve MASAK şüphe durumları tabloya dönüştürülmüştür.

#### 2. ⚙️ Arkada Ne Çalıştı?
* **Akıllı Yönlendirme:** `Tier 1 (Hızlı Çıkarım & Regex Parser)` ➔ `llama3.2:3b`.
* **Yürütme Süresi:** **20.9 saniye (Ultra Hızlı)**.

#### 3. 🖥️ Arayüzde Yapılan İşlem & 📊 Görülen Sonuç
* Serbest metin 7 sütunlu temiz bir veri tablosuna dönüştürüldü; şüpheli transferler kırmızı uyarı rozetleriyle işaretlendi.

---

### 🚀 GÖREV 08: 5C Standart Denetim Bulgusu Yazımı
* **Aşama:** 4. Denetim Raporlama (Reporting)  
* **Ekran Görüntüsü:** `storage/screenshots/task_08_finding_5c.png`  

#### 1. 🎯 Amaç & Senaryo Girdisi
145M TL yetkisiz kredi tahsisi, sahte ekspertizle %850 LTV ve Panama'ya aktarılan 78.5M TL MASAK kaçakçılığı vakası IIA 5C standardında resmi rapora bağlanmıştır.

#### 2. ⚙️ Arkada Ne Çalıştı?
* **Akıllı Yönlendirme:** `Tier 3 (Karmaşık Akıl Yürütme & Raporlama)` ➔ `deepseek-r1 / qwen2.5-coder:7b`.
* **Mevzuat RAG Enjeksiyonu:** 5411 Sayılı Bankacılık Kanunu Madde 160 (Zimmet) ve 5549 Sayılı MASAK Kanunu Madde 8/13.
* **Yürütme Süresi:** 119.1 saniye.

#### 3. 🖥️ Arayüzde Yapılan İşlem & 📊 Görülen Sonuç
* **Condition:** 145M TL kredi ve Panama transferi saha tespitleri.
* **Criteria:** 5411 ve 5549 sayılı yasal maddeler.
* **Cause:** Şube Müdürü yetki aşımı ve Core Banking SoD zaafiyeti.
* **Effect:** 145M TL batık riski ve MASAK idari para cezası.
* **Recommendation:** Savcılık suç duyurusu, MASAK STR bildirimi ve FIDO2 sistemsel kuralı.

---

### 🚀 GÖREV 09: Yönetim Kurulu ve Denetim Komitesi Özeti
* **Aşama:** 4. Denetim Raporlama (Reporting)  
* **Ekran Görüntüsü:** `storage/screenshots/task_09_executive_summary.png`  

#### 1. 🎯 Amaç & Senaryo Girdisi
Dönem içinde tamamlanan 6 görevde tespit edilen 14 bulgu (3 Kritik, 6 Yüksek, 5 Orta) ve 210M TL toplam maruziyet Yönetim Kurulu için özetlenmiştir.

#### 2. ⚙️ Arkada Ne Çalıştı?
* **Akıllı Yönlendirme:** `Tier 2 (Standart Analiz)` ➔ `qwen2.5-coder:7b`.
* **Yürütme Süresi:** 96.9 saniye.

#### 3. 🖥️ Arayüzde Yapılan İşlem & 📊 Görülen Sonuç
* Genel Güvence Görüşü: 🔴 **OLUMSUZ (Kritik İç Kontrol Zaafiyeti)**.
* Üst yönetim aksiyon matrisi ve takvim tablosu üretildi.

---

### 🚀 GÖREV 10: Python (Pandas) İstisna Analiz Kodu & Canlı Sandbox
* **Aşama:** 5. Sürekli Denetim & Analitik (Analytics)  
* **Ekran Görüntüsü:** `storage/screenshots/task_10_data_analytics.png`  

#### 1. 🎯 Amaç & Senaryo Girdisi
Hazine veri tabanındaki (`transactions_sample.xlsx`) Offshore para transferleri ve MASAK bypass işlemlerini tespit eden Python Pandas istisna analiz betiği üretilmiş ve izole sandbox ortamında canlı koşturulmuştur.

#### 2. ⚙️ Arkada Ne Çalıştı?
* **Akıllı Yönlendirme:** `Tier 2 (Kodlama & Veri Analitiği)` ➔ `qwen2.5-coder:7b`.
* **İzole Python Sandbox:** Subprocess içinde geçici çalışma ortamı açılarak Excel verisi bağlandı, anomali kuralları işletildi.
* **Üretilen Çıktı Dosyası:** `audit_exceptions.xlsx` (3 Sekmeli Rapor).

#### 3. 🖥️ Arayüzde Yapılan İşlem & 📊 Görülen Sonuç
* Arayüzdeki **`⚡ Kodu Sandbox'ta Çalıştır`** butonuna basıldı.
* Ekrana *"Python analitik kodu izole sandbox'ta başarıyla çalıştırıldı ve audit_exceptions.xlsx üretildi"* yeşil bildirim kartı ve canlı terminal logları yansıdı.

---

## 🔒 Güvenlik & Denetim İzi (Audit Trail) Mimarisi
Üretilen her bir çalışma kağıdı için arayüzün 3. sekmesinde canlı olarak görüntülenen ve JSON formatında indirilebilen Audit Trail nesnesi şu bileşenlerden oluşur:
```json
{
  "timestamp": "2026-08-30T18:35:12Z",
  "audit_integrity_sha256": "3a8f9c4d12e7...",
  "dispatched_model": {
    "model_name": "qwen2.5-coder:7b",
    "tier": "Tier 2 (Standart Analiz)"
  },
  "privacy_evaluation": {
    "masked_entities_count": 4,
    "pii_leak_risk": "0.0% (Zero Cloud Leak)"
  },
  "quality_score": 95
}
```

---

## 📄 Kullanıcı Kılavuzu İndirme Bağlantıları
* **Resmi PDF Kılavuz:** `storage/Auditoris_Resmi_Kullanim_Rehberi.pdf`
* **Senaryo Veri Seti Kütüphanesi:** `storage/test_scenarios_library.json`
* **Master Ekran Görüntüleri Arşivi:** `storage/screenshots/` (10 Adet %100 Dolu PNG)
