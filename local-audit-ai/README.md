# 🏛️ AUDİTORİS 2026 — YEREL YAPAY ZEKA İÇ DENETİM İŞLETİM SİSTEMİ
> **IIA (The Institute of Internal Auditors) Küresel Standartları (2026 Evolution) ve COSO ERM ile Tam Uyumlu, %100 Hava Boşluklu (Air-Gapped) Kurumsal Denetim Platformu**

[![Sürüm](https://img.shields.io/badge/S%C3%BCr%C3%BCm-2026.1%20Enterprise-blue.svg)](#)
[![Güvenlik](https://img.shields.io/badge/G%C3%BCvenlik-%25100%20Yerel%20%2F%20Air--Gapped-green.svg)](#)
[![IIA Uyum](https://img.shields.io/badge/IIA%20Standartlar%C4%B1-2026%20Evolution-0f172a.svg)](#)
[![Mevzuat](https://img.shields.io/badge/Mevzuat-BDDK%20%7C%20MASAK%20%7C%20SPK%20%7C%20KVKK-indigo.svg)](#)

---

## 📌 Genel Bakış ve Temel Felsefe
**Auditoris**, kurumsal iç denetim departmanları, teftiş kurulları ve kalite güvence ekipleri için geliştirilmiş yeni nesil bir denetim işletim sistemidir.

Bankacılık, finans, holding ve kritik sektörlerde müşteri sırrı, ticari sırlar ve hassas verilerin üçüncü taraf bulut servislerine (OpenAI, Anthropic, Google Cloud vb.) aktarılması regülasyonlarca yasaktır. Auditoris, tüm muhakeme, PII maskeleme, mevzuat tarama ve kod yürütme süreçlerini **doğrudan kurum içi yerel donanımda (On-Premise / Air-Gapped)** icra ederek **Sıfır Bulut Veri Sızıntısı (%100 Zero-Telemetry)** güvencesi sağlar.

---

## 🌟 6 Çekirdek Motor ve Mimari Topoloji

Auditoris, birbirinden bağımsız çalışan 6 çekirdek motorun senkronize koordinasyonuyla çalışır:

```
AUDITORIS 6 ÇEKİRDEK MOTOR MİMARİSİ
├── 1. Smart Evidence Extractor ➔ 25.000+ satırlık tablolardan limit aşımı ve MASAK ihlallerini süzer (Token tasarrufu: %85).
├── 2. PII Masker (KVKK/GDPR) ➔ TCKN, IBAN, Kredi Kartı ve şahıs isimlerini deterministik [TCKN_1] olarak şifreler.
├── 3. Dynamic Offline Vector RAG ➔ ChromaDB ve hibrit TF-IDF ile BDDK, MASAK, SPK, TTK ve IIA kurallarını tarar.
├── 4. Complexity Router (Auto-Tiering) ➔ Görev zorluğuna göre Tier 1 (3B), Tier 2 (7B-8B) veya Tier 3 (14B) yerel model atar.
├── 5. Isolated Python Analytics Sandbox ➔ Pandas anomali analiz kodlarını AST denetimli izole subprocess içinde koşturur.
└── 6. IIA 5C QA/QC & Sistem Çıktı Motoru ➔ 0-100 Kalite Skoru üretir; Word (.docx), Zebra Excel (.xlsx) ve SHA-256 JSON üretir.
```

---

## 📋 5 Denetim Aşaması ve 10 Görev Türü

| Aşama | Görev Türü | Varsayılan Model & Tier | Temel Sistem Çıktısı |
| :--- | :--- | :--- | :--- |
| **1. Yıllık Planlama** | `audit_universe` | `qwen2.5-coder:7b` (Tier 2) | 18 İştirak Birleşik Risk Skoru ve Denetim Frekans Tablosu |
| **1. Yıllık Planlama** | `resource_competency_mapping` | `qwen2.5-coder:7b` (Tier 2) | Ekip Yetkinlik Matrisi, Adam/Gün Bütçesi ve Dış Kaynak Planı |
| **2. Görev Planlama** | `rcm_generation` | `qwen2.5-coder:7b` (Tier 2) | 6 Sütunlu Risk & Kontrol Matrisi (RCM) ve Walkthrough Mülakat Soruları |
| **2. Görev Planlama** | `scoping_document` | `qwen2.5-coder:7b` (Tier 2) | Kapsam İçi / Kapsam Dışı Sınırları ve 3 Haftalık Saha Planı |
| **3. Saha Çalışması** | `test_procedure` | `qwen2.5-coder:7b` (Tier 2) | 4-Ögeli (Amaç, Örneklem, Test Adımları, Hata Kriteri) Test Programı |
| **3. Saha Çalışması** | `control_analysis` | `qwen2.5-coder:7b` (Tier 2) | SoD Tasarım Zafiyeti Analizi ve FIDO2 Alternatif Kontrol Tasarımı |
| **3. Saha Çalışması** | `data_extraction` | `llama3.2:3b` (Tier 1) | Serbest Saha Notlarından 7 Sütunlu Yapılandırılmış İşlem Tablosu |
| **4. Denetim Raporlama** | `finding_5c` | `qwen2.5-coder:7b` (Tier 2/3) | IIA 5C Standardında (Condition, Criteria, Cause, Effect, Recommendation) Resmi Bulgu |
| **4. Denetim Raporlama** | `executive_summary` | `qwen2.5-coder:7b` (Tier 2) | Yönetim Kurulu ve Denetim Komitesi için Genel Güvence Görüşü ve Aksiyon Matrisi |
| **5. Sürekli Analitik** | `data_analytics` | `qwen2.5-coder:7b` (Tier 2/3) | Canlı Python Pandas Kod İcrası ve Çok Sekmeli `audit_exceptions.xlsx` Raporu |

---

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler
- Python 3.10 veya üzeri
- [Ollama](https://ollama.ai/) (Yerel model sunucusu)

### 2. Kurulum
```bash
# Depoyu klonlayın
git clone <repo-url>
cd local-audit-ai

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 3. Yerel Modellerin İndirilmesi (Ollama)
```bash
# Tier 1 (Hafif Veri Ayıklama)
ollama pull llama3.2:3b

# Tier 2 (Standart Muhakeme, RCM ve 5C Bulgu)
ollama pull qwen2.5-coder:7b
ollama pull deepseek-r1:8b

# Tier 3 (İleri Düzey Veri Analitiği)
ollama pull qwen2.5-coder:14b
```

### 4. Web Kokpitini Başlatma
```bash
streamlit run interfaces/web_ui/app.py
```
Tarayıcınızda **`http://localhost:8501`** adresine gidin.

---

## 📊 Sistem Çıktı Formatları ve Ham Veri Erişimi

Auditoris, denetim kanıtlarının resmi teftiş dosyalarında kullanılabilmesi için 4 farklı sistem çıktısı sunar:

1. **Word (.docx) Resmi Çalışma Kağıdı:** Kurumsal lacivert antetli, 5C hiyerarşik başlıklı ve SHA-256 dijital mühürlü.
2. **Formatlı Excel (.xlsx) Tablosu:** Koyu lacivert başlıklı, açık gri zebra satırlı ve otomatik sütun genişlikli.
3. **Sandbox İstisna Raporu (`audit_exceptions.xlsx`):** 25.000+ satırlık tablolardan filtrelenen çok sekmeli anomali dökümü.
4. **Kriptografik Audit Trail (JSON):** Girdi/Çıktı SHA-256 hash imzası, PII maskeleme sayıları, model ve çıkarım süresi metaverisi.

> **💡 Ham Veri Erişimi:** Denetçiler arayüzdeki **`🔍 Model Analizi`** sekmesinden modelin kullandığı **Saf Prompt Metnine**, **`🔒 Güvenlik & Audit Trail`** sekmesinden ise **Ham JSON Nesnesine** anlık olarak erişip kopyalayabilir.

---

## 📕 Resmi Kılavuz ve Diyagramlar
* **18 Sayfalık Master Kullanıcı Kılavuzu:** `storage/Auditoris_Kullanici_Kilavuzu_2026.pdf`
* **Sistem ve Motor Topoloji Diyagramları:** `storage/diagrams/` (7 Adet 300 DPI PNG)
* **10 Görev Canlı UI Ekran Görüntüleri:** `storage/screenshots/` (10 Adet Tam Sonuçlu PNG)
* **Sentetik Senaryo Kütüphanesi:** `storage/test_scenarios_library.json`

---

## 🧪 Test Suite ve Canlı Doğrulama
```bash
# Birim Testleri
pytest tests/ -v

# Canlı Playwright Tarayıcı Testi
python3 tests/master_live_ui_suite.py
```

---

## ⚖️ Lisans ve Standart Uyum
Bu proje **IIA Küresel İç Denetim Standartları**, **COSO İç Kontrol Bütünleşik Çerçevesi**, **BDDK**, **MASAK** ve **6698 Sayılı KVKK** ilkeleriyle tam uyumlu olarak tasarlanmıştır.

**Geliştirici & Sistem Mimarı:** Doğukan Cihanbeyoğlu
