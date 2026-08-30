# Auditoris — Master Kullanıcı Kılavuzu, Senaryo ve Çıktı Rehberi
**Sistem:** Auditoris (Next-Gen Autonomous AI Audit OS)  
**Sürüm:** 3.5 Enterprise AI  
**Geliştirici & Sistem Mimarı:** Doğukan Cihanbeyoğlu  
**Metodoloji:** IIA Global Internal Audit Standards (2026)  
**Güvenlik Modu:** %100 Yerel / Çevrimdışı (Zero Data Leakage / Air-Gapped)

---

## 1. Sistemin Temel Vizyonu ve 6 Çekirdek Motoru

Auditoris; kurumsal iç denetim departmanları, teftiş kurulları ve risk yöneticileri için geliştirilmiş, IIA Küresel Standartları ile tam uyumlu yeni nesil bir denetim işletim sistemidir. On binlerce satırlık veri tablolarını ve yüzlerce sayfalık kurumsal prosedürleri yerel olarak analiz eder, yasal mevzuatları dinamik eşleştirir ve resmi çalışma kağıtları üretir.

| Çekirdek Motor | Teknik İşlevi (Arkada Ne Çalışır?) | Denetçiye Sağladığı Katkı |
| :--- | :--- | :--- |
| **1. Smart Evidence Extractor** | 25.000+ satırlık tablolardan limit aşımlarını, sahte ekspertizleri ve MASAK ihlallerini önceden süzer. | Modelin dikkat kaybı yaşamasını önler; kritik risk kanıtlarını önceliklendirir. |
| **2. PII Masker (KVKK/GDPR)** | TCKN, IBAN, Kredi Kartı ve E-posta verilerini yerel deterministik regex ile `[TCKN_1]` olarak şifreler ve geri çözer. | Hassas müşteri ve şirket verilerinin gizliliğini %100 güvenceye alır. |
| **3. Dynamic Offline RAG** | TF-IDF ve Cosine Similarity vektörleriyle BDDK, MASAK, SPK, KVKK, TTK ve SOX kurallarını tarar. | Denetim bulgularına tartışmasız yasal dayanak (Criteria) sağlar. |
| **4. Complexity Router & Tier** | Görev karmaşıklığına göre Tier 1 (Hafif), Tier 2 (Muhakeme) veya Tier 3 (Analitik/Kod) atar. | Doğru göreve doğru yerel yapay zeka modelinin otomatik atanmasını sağlar. |
| **5. Audit QA/QC Evaluator** | Üretilen çalışma kağıdını 5C eksiksizliği üzerinden 100 puan üzerinden değerlendirir. | IIA Tier-1 kalitesinde denetim güvencesi sunar. |
| **6. Local Python Sandbox** | Model tarafından üretilen Pandas analitik kodlarını izole subprocess içinde çalıştırarak Excel raporlarını üretir. | Büyük verilerde sıfır hata ile anomali tabloları döker. |

---

## 2. 5 Denetim Yaşam Döngüsü Aşaması ve Uygulamalı Ekran Akışı

### 📊 AŞAMA 1: Yıllık Planlama (Annual Planning)
* **Görev:** Denetim Evreni ve Risk Derecelendirmesi
* **Senaryo:** Holding bünyesindeki 18 iştirak ve 25 kritik sürecin risk skorlaması ve 2026 Denetim Planı önceliklendirmesi.
* **Açılan Sonuç Alanları:** IIA Standart Uyum Skoru (95/100), Süreç Risk Puanı Tablosu, Frekans Planı, Antetli Word/Excel indirme butonları.

---

### 📑 AŞAMA 2: Görev Planlama (Engagement Planning)
* **Görev:** Risk ve Kontrol Matrisi (RCM) & Walkthrough Mülakat Soruları
* **Senaryo:** Hazine ve Döviz Swap Operasyonları süreci için Yetkisiz Spot FX ve SoD çakışması riskleri.
* **Açılan Sonuç Alanları:** Kontrol Faaliyeti Tablosu, Test Adımları, Süreç Sahibi Walkthrough Soruları, Eşleşen BDDK & SPK Hazine Tebliğleri (%95+ Eşleşme).

---

### 🔍 AŞAMA 3: Saha Çalışması (Fieldwork & Testing)
* **Görev:** Kontrol Tanımı ve Tasarım Zayıflığı Analizi
* **Senaryo:** Hazine sözlü döviz alımları ve akaryakıt deniz nakliyesinde %2.5 fire toleransı kuralı zafiyetleri.
* **Açılan Sonuç Alanları:** Tasarım Zafiyeti ve SoD İhlali Tespiti, Muğlak İfadeler Analizi, Önerilen FIDO2 MFA Sağlam Kontrol Tasarımı.

---

### 📝 AŞAMA 4: Denetim Raporlama (Reporting)
* **Görev:** 5C Standart Denetim Bulgusu Yazımı
* **Senaryo:** 145M USD sahte ekspertizli teminatsız kredi zimmeti ve 78.5M USD Panama MASAK transferi.
* **Açılan Sonuç Alanları:** Condition (Durum), Criteria (Kriter), Cause (Kök Neden), Effect (Etki), Recommendation (Öneri), BDDK Madde 160 & MASAK Madde 8 Hukuki Dayanakları.

---

### ⚡ AŞAMA 5: Sürekli Denetim ve Analitik (Analytics)
* **Görev:** Python (Pandas) İstisna Analiz Kodu & Canlı Sandbox
* **Senaryo:** 25.000 satırlık bankacılık tablosunda LTV > 0.75 ve MASAK bypass anomalilerinin filtrelenmesi.
* **Açılan Sonuç Alanları:** Python Kod Bloğu, `⚡ Kodu Sandbox'ta Çalıştır` Butonu, Üretilen `audit_exceptions.xlsx` Dosyasını Tek Tıkla İndirme Alanı.

---

## 3. Resmi Çıktılar, Formatlar ve İhraç Dosyaları Analizi

| Çıktı Formatı | Teknik Format Yapısı ve Görsel Standartları | Kullanım Amacı & Hedef Kitle |
| :--- | :--- | :--- |
| **1. Word (.docx) Çalışma Kağıdı** | • Kurumsal lacivert (`#0f172a`) antet başlığı<br/>• Denetçi, Tarih ve Görev meta bilgi kutusu<br/>• IIA 5C Hiyerarşisi (Condition, Criteria...)<br/>• SHA-256 Kriptografik Denetim İzi Mührü ve "ÇOK GİZLİ" damgası. | Denetim Komitesi, Yönetim Kurulu ve Cumhuriyet Savcılığı resmi teftiş dosyaları. |
| **2. Formatlı Excel (.xlsx) Tablosu** | • Koyu lacivert (`#0f172a`) başlık hücreleri (Beyaz kalın yazı)<br/>• Açık gri alternatif zebra satırları (`#f8fafc` / `#ffffff`)<br/>• İnce gri kenarlıklar ve otomatik sütun genişlik optimizasyonu. | Risk ve Kontrol Matrisleri (RCM), Denetim Evreni ve sayısal kontrol listeleri. |
| **3. Sandbox İstisna Raporu (.xlsx)** | • Pandas ile 25.000 satırdan filtrelenen anomaliler<br/>• Çok sekmeli (Multi-Sheet) istisna listesi (Örn: LTV_Breach, MASAK_Bypass)<br/>• Orijinal veri satır referansları ve anomali tutarları. | Sürekli denetim, fraud inceleme ve veri analitiği saha ekipleri. |
| **4. Kriptografik Audit Trail (JSON)** | • Girdi ve çıktı SHA-256 hash imzaları<br/>• Kullanılan model adı, çalışma süresi ve zaman damgası<br/>• IIA Standardı 2026 Uyum Deklarasyonu. | Kalite güvence gözden geçirmeleri (QAR) ve bağımsız regülasyon denetimleri. |

---

## 4. Otonom Model Havuzu ve Tier Yönetimi (Auto-Tiering)

Auditoris, yerel bilgisayarınızda kurulu olan tüm yapay zeka modellerini (10, 20 veya 50 model) otonom olarak tarayan ve uzmanlıklarına göre en ideal Tier eşleştirmesini yapan akıllı bir Model Registry motoruna sahiptir.

* **Tier 1 (Hızlı / Veri Ayıklama Modeli):** Küçük boyutlu (3B-8B), hafif ve hızlı modellere (`qwen2.5-coder:7b`) atanır. Basit metin ve fatura ayıklama görevlerinde çalışır.
* **Tier 2 (Standart / 5C & Muhakeme Modeli):** Akıl yürütme (reasoning/r1) modellerine (`deepseek-r1:8b`) atanır. RCM, kapsam dokümanı ve 5C bulgu yazımında çalışır.
* **Tier 3 (İleri Düzey / Python & Analitik Modeli):** Kodlama uzmanı veya büyük modellere (`qwen2.5-coder:14b`) atanır. Pandas analitik kodları ve yıllık planlamada çalışır.
* **🪄 Otonom En İyi Modelleri Eşle Butonu:** Sol kenar çubuğundaki bu butona basıldığında sistem makinedeki tüm modelleri $0-10$ arası puanlar ve en ideal modelleri ilgili Tier'lara sıfır kod değişikliğiyle otomatik atar.

---
*Auditoris Enterprise AI | Geliştirici & Sistem Mimarı: Doğukan Cihanbeyoğlu*
