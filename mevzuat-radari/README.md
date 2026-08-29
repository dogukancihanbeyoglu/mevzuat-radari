# 🏛️ Resmî Gazete İç Denetim & Uyum Radarı (`mevzuat-radari`)

> T.C. Resmî Gazete'yi günlük olarak tarayan, şirketin faaliyet alanı, ölçeği ve tabi olduğu regülasyonlara göre alaka analizi yapan, **Model Context Protocol (MCP)** tabanlı yapay zeka uyum ve iç denetim asistanı.

---

## 🌟 Öne Çıkan Özellikler

* 🏛️ **4 Kademeli Uyum & Normlar Hiyerarşisi:** Yalnızca dar sektörel kelimeleri değil; Cumhurbaşkanlığı Kararnameleri, Anayasa Mahkemesi Kararları, Yüksek Yargı İçtihatları, Yatırım Teşvikleri, Vergi/Maliye, İK/İSG, KVKK/Siber, Kamu İhale, Çevre/ESG ve Sanayi/TSE standartlarını kapsar. *(Detaylar için: [`COMPLIANCE_ARCHITECTURE.md`](file:///Users/dogukancihanbeyoglu/Gemini/mevzuat-radari/COMPLIANCE_ARCHITECTURE.md))*
* 🎯 **Şirket Odaklı Akıllı Filtreleme:** Kararları genel olarak değil; şirketin NACE kodlarına, cirosuna, düzenleyici otoritelerine ve operasyonel özelliklerine göre puanlar (0-100).
* 🛡️ **Evrensel Gürültü Süzgeci:** Resmî Gazete'deki öğrenci sınav, memur terfi ve yerel belediye bütçesi gibi gürültüleri otomatik eler; ticari/yasal zorunlulukları istisna kapısıyla korur.
* ⚡ **Hazır Sektörel Uyum Şablonları:** Savunma Sanayii, FinTech, E-Ticaret, Yazılım/SaaS ve Enerji sektörleri için 1-tıkla yüklenebilen ön-tanımlı uyum profilleri.
* 📑 **İç Denetim Perspektifi:** Yalnızca metin özeti sunmaz; **Risk Derecesi (Kritik/Yüksek/Orta)**, **Yaptırım & Ceza Riski**, **Etkilenen Departmanlar** ve **Aksiyon Kontrol Listesi (Checklist)** üretir.
* 🌐 **Modern Web Yönetim Paneli:** FastAPI ve Tailwind CSS ile canlı tarama, tarih aralığı sorgulama, şirket profili kalibrasyonu ve PDF rapor indirme.
* 🤖 **MCP Sunucu Desteği:** Claude Desktop, Cursor, Antigravity IDE gibi yapay zeka araçlarına doğrudan bağlanabilir.
* 📄 **Kurumsal PDF & E-Posta:** Türkçe tipografi (Arial TTF) destekli profesyonel bülten üretimi ve dağıtımı.

---

## 🏗️ Proje Mimarisi

```text
mevzuat-radari/
├── COMPLIANCE_ARCHITECTURE.md     # 4 Kademeli Regülasyon ve Uyum Mimarisi Dokümantasyonu
├── config/
│   └── company_profile.yaml       # Şirket profili, NACE kodları ve kural parametreleri
├── src/
│   ├── models.py                  # Pydantic veri modelleri
│   ├── scraper.py                 # Resmî Gazete fihrist ve karar metni çekici
│   ├── evaluator.py               # 4 Kademeli eşleştirme, puanlama ve etki analiz motoru
│   ├── sector_templates.py        # Sektörel şablonlar ve gürültü taksonomisi
│   ├── web_app.py                 # FastAPI web dashboard ve REST API
│   ├── pdf_generator.py           # ReportLab Türkçe tipografili PDF raporlayıcı
│   ├── email_sender.py            # SMTP e-posta rapor dağıtım servisi
│   ├── templates.py               # Markdown ve HTML rapor şablonları
│   └── server.py                  # FastMCP / MCPServer araç sağlayıcısı
├── reports/                       # Üretilen günlük denetim raporları arşivi
├── tests/                         # Birim ve entegrasyon testleri (13 test)
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

### 2. Şirket Profilini Düzenleme
`config/company_profile.yaml` dosyasını kendi şirketinizin sektör ve yasal kriterlerine göre güncelleyin:
```yaml
company_profile:
  general:
    name: "Şirketinizin Adı A.Ş."
    scale: "Büyük Ölçekli"
    employee_count: 500
    annual_turnover_tl: "500M+"
  sectors_and_nace:
    primary_sector: "Perakende & E-Ticaret"
    nace_codes:
      - "47.91.00"
  regulatory_bodies:
    - "Ticaret Bakanlığı"
    - "Hazine ve Maliye Bakanlığı"
    - "KVKK"
```

### 3. Günlük Taramayı Çalıştırma
```bash
# Bugünün Resmî Gazetesini tara ve rapor üret:
python run_daily_audit.py

# Belirli bir tarihi tara (Örn: 2026-08-29):
python run_daily_audit.py --date 2026-08-29 --min-score 30
```

---

## 🔌 MCP (Model Context Protocol) Sunucusu Olarak Kullanım

Yapay zeka asistanınıza (Claude Desktop, Cursor, Antigravity) eklemek için konfigürasyonunuza şunu ekleyin:

```json
{
  "mcpServers": {
    "mevzuat-radari": {
      "command": "python",
      "args": ["/tam/yol/mevzuat-radari/src/server.py"]
    }
  }
}
```

### Sunulan MCP Araçları (Tools):
* `get_company_profile()`: Şirket profilini döner.
* `fetch_gazette_fihrist(date)`: Belirtilen tarihin gazete fihristini listeler.
* `read_regulation_text(url)`: Belirtilen kararın/tebliğin tam metnini okur.
* `evaluate_daily_gazette(date, min_score)`: Günün gazetesini tarayıp analiz eder ve eksiksiz Markdown denetim bülteni üretir.
* `test_regulation_relevance(title, category)`: Belirli bir mevzuat başlığının şirket üzerindeki etkisini anlık test eder.

---

## 🧪 Testleri Çalıştırma
```bash
pytest tests/
```

---

## 📄 Lisans
MIT License.
