# 🏛️ Resmî Gazete İç Denetim & Uyum Radarı (`mevzuat-radari`)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![MCP Compliant](https://img.shields.io/badge/MCP-Standard%20v1.0-8A2BE2.svg)](https://modelcontextprotocol.io/)
[![Tests Passing](https://img.shields.io/badge/tests-15%20passed-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **T.C. Resmî Gazete'yi** günlük ve geriye dönük (arşiv) olarak tarayan; şirketin unvanı, sermaye büyüklüğü, çalışan sayısı, Ar-Ge/ihracat yetkinlikleri ve tabi olduğu regülatörlere göre derinlemesine analiz eden **Model Context Protocol (MCP)** tabanlı kurumsal iç denetim ve uyum platformu.

---

## 🌟 Öne Çıkan Yetenekler

* 🏛️ **4 Kademeli Normlar Hiyerarşisi & Sistemik Uyum:** Sadece dar sektörel anahtar kelimeleri değil; *Cumhurbaşkanlığı Kararnameleri*, *Anayasa Mahkemesi İptal Kararları*, *Yüksek Yargı İçtihatları*, *Vergi/Maliye*, *İş Hukuku/İK*, *KVKK/Siber Güvenlik*, *Kamu İhale/Fiyat Farkı*, *Yatırım Teşvik*, *Dış Ticaret/Gümrük* ve *Çevre/Sürdürülebilirlik* boyutlarını eksiksiz kapsar.
* 🏢 **Çoklu Sektör & Hibrit Faaliyet Modeli (Multi-Sector Conglomerate Mode):** Savunma, FinTech, Yazılım/SaaS, E-Ticaret ve Enerji alanlarında aynı anda faaliyet gösteren holding ve büyük teknoloji şirketleri için **otomatik çelişki gidermeli (Conflict-Free)** şablon birleştirme motoru.
* 🧠 **Derin Karar Metni & Şirket Profili Etki Analizi:** Alarm üretilen kararların PDF ve HTML metin gövdelerini (`pypdf` bellek içi akışıyla) ayrıştırarak kararın **şirket ölçeği, cirosu ve projeleri açısından operasyonel anlamını**, **madde bazlı özetlerini** ve **kesin yürürlük takvimini** çıkarır.
* 🛡️ **Evrensel Gürültü Sınıflandırıcısı:** Üniversite sınavları, memur atamaları ve yerel belediye bütçesi gibi gürültüleri otomatik eler; ticari/yasal zorunlulukları istisna koruma kurallarıyla güvenceye alır.
* 📑 **İç Denetim Perspektifli Çıktılar:** Yalnızca metin özeti sunmaz; **Risk Seviyesi (Kritik/Yüksek/Orta)**, **Hukuki Yaptırım & Ceza Riski**, **Etkilenen Departmanlar** ve **Aksiyon Kontrol Listesi (Checklist)** üretir.
* 🌐 **Modern Web Yönetim Dashboard'u:** FastAPI ve Tailwind CSS ile canlı fihrist tarama, arşiv taraması (örn: 2024-2026), interaktif şirket profili düzenleme ve tek tıkla PDF bülten indirme.
* 🤖 **MCP (Model Context Protocol) Server:** Claude Desktop, Cursor IDE ve Antigravity AI asistanlarına sıfır konfigürasyonla bağlanan yerel zeka katmanı.
* 📄 **Kurumsal PDF & E-Posta Dağıtımı:** Türkçe tipografi (Arial TTF) destekli profesyonel bülten üretimi ve şirket içi paydaşlara otomatik e-posta gönderimi.

---

## 🏗️ Proje Mimarisi & Dosya Yapısı

Detaylı teknik mimari, algoritmalar ve karar matrisleri için lütfen [**`COMPLIANCE_ARCHITECTURE.md`**](COMPLIANCE_ARCHITECTURE.md) dosyasını inceleyiniz.

```text
mevzuat-radari/
├── COMPLIANCE_ARCHITECTURE.md     # 8 Bölümlük Kapsamlı Uyum ve Regülasyon Mimarisi
├── README.md                      # Proje genel tanıtımı ve kullanım kılavuzu
├── config/
│   ├── company_profile.yaml       # Şirket profili, NACE kodları ve kural parametreleri
│   └── llm_config.json            # YZ modeli sağlayıcı ve API yapılandırması
├── src/
│   ├── models.py                  # Pydantic v2 veri modelleri
│   ├── scraper.py                 # Resmî Gazete fihrist ve PDF/HTML karar metni çekici
│   ├── evaluator.py               # 4 Kademeli eşleştirme, puanlama ve derin etki analiz motoru
│   ├── sector_templates.py        # Çoklu sektör şablonları ve çelişki giderme motoru
│   ├── web_app.py                 # FastAPI web dashboard ve REST API (Port: 8000)
│   ├── pdf_generator.py           # ReportLab Türkçe tipografili PDF raporlayıcı
│   ├── email_sender.py            # SMTP e-posta rapor dağıtım servisi
│   ├── notifier.py                # Dağıtım orkestrasyon motoru
│   ├── templates.py               # Markdown ve HTML bülten şablonları
│   ├── llm_engine.py              # LLM çağrı köprüsü ve sağlayıcı yönetimi
│   └── server.py                  # FastMCP / MCP Server araç sağlayıcısı
├── reports/                       # Üretilen günlük denetim raporları arşivi
├── tests/
│   └── test_all.py                # 15/15 Uçtan Uca Birim & Entegrasyon Testleri
├── run_web.py                     # Web dashboard başlatıcı (port: 8000)
├── run_daily_audit.py             # CLI çalıştırma scripti
└── requirements.txt               # Bağımlılıklar
```

---

## 🚀 Hızlı Başlangıç

### 1. Kurulum
```bash
git clone https://github.com/<kullanici_adi>/mevzuat-radari.git
cd mevzuat-radari

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Web Yönetim Paneli
```bash
python run_web.py --port 8000
```
Tarayıcınızdan `http://localhost:8000` adresini açarak:
* Günlük veya tarih aralıklı Resmî Gazete taraması yapabilir,
* Şirketinizin faaliyet sektörlerini tek tıkla birleştirebilir (Savunma + FinTech + SaaS + E-Ticaret),
* YZ modelinizi seçebilir (Yerel Kural Tabanlı Motor / GPT-4o / Claude 3.5 / Gemini / DeepSeek),
* Kurumsal PDF denetim bültenini indirebilir veya e-posta ile dağıtabilirsiniz.

### 3. CLI Üzerinden Günlük Tarama
```bash
# Bugünün Resmî Gazetesini tara:
python run_daily_audit.py

# Belirli bir tarihi tara (Örn: 2026-08-29):
python run_daily_audit.py --date 2026-08-29 --min-score 30
```

---

## 🔌 MCP (Model Context Protocol) Entegrasyonu

Claude Desktop, Cursor veya Antigravity IDE içerisine eklemek için konfigürasyon JSON dosyanıza ekleyin:

```json
{
  "mcpServers": {
    "mevzuat-radari": {
      "command": "python",
      "args": ["/tam/proje/yolu/mevzuat-radari/src/server.py"]
    }
  }
}
```

### Kullanılabilir MCP Araçları:
| Tool Adı | Açıklama |
| :--- | :--- |
| `get_company_profile()` | Aktif şirket profilini, NACE kodlarını ve parametrelerini getirir. |
| `fetch_gazette_fihrist(date)` | Belirtilen tarihin Resmî Gazete fihristini listeler. |
| `read_regulation_text(url)` | İlgili karar/tebliğin tam metnini (PDF/HTML) bellek içinde okur. |
| `evaluate_daily_gazette(date, min_score)` | Günlük bülteni tarar, derin analizini yapar ve Markdown rapor üretir. |
| `test_regulation_relevance(title, category)` | Verilen bir başlığın şirket profili üzerindeki etkisini anlık test eder. |

---

## 🧪 Testleri Çalıştırma

Tüm modüller (scraper, scoring, deep content analyzer, horizontal compliance, negative noise filtering, multi-sector merge, MCP server) 15 otomatik test ile doğrulanmaktadır:

```bash
pytest tests/ -v
```

---

## 📄 Lisans
MIT License - Açık Kaynak ve Kurumsal Kullanıma Uygundur.

