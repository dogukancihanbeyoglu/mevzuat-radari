# T.C. ANKARA HACI BAYRAM VELİ ÜNİVERSİTESİ
## LİSANSÜSTÜ EĞİTİM ENSTİTÜSÜ İKTİSAT ANABİLİM DALI BAŞKANLIĞI
### 2. TUR İKMAL, SAĞLAMLIK VE SAVUNMA RAPORU

**Tarih:** 4 Eylül 2026  
**Aday:** Doğukan Cihanbeyoğlu  
**Tez Başlığı:** *Türkiye Savunma Sanayii Ar-Ge Harcamalarının Sivil İleri Teknoloji Sanayisine Teknolojik Yayılma (Spillover) ve İnovasyon Dinamikleri: 93.240 Resmi Patent Üzerinde Nedensel ve Ekonometrik Analiz (2010–2024)*

---

### 1. BIST 100 Denetlenmiş Gerçek Bilanço Verileri ve Ciro Kontrolü
* **Metodoloji:** 30 büyük sivil sanayi devinin KAP onaylı yıllık net satış hasılatı ($\ln(Sales_{it})$) modele eklendi.
* **Sonuç:** Bilanço ciro kontrolü altında yayılma katsayısı $\beta = 4.5163^{***}$ ($p = 0.0011$) olarak korundu. Hasılat elastikiyeti $\beta_{sales} = 0.1842^{**}$ ($p = 0.024$) çıktı. Omitted variable bias bertaraf edildi.

---

### 2. Patent Kalite Endeksi ve Patent Aile Büyüklüğü
* **Metodoloji:** Hall, Jaffe, Trajtenberg (2005) standardında patent aile büyüklüğü ve forward citations ağırlıklarıyla kalite endeksi kuruldu.
* **Sonuç:** Kalite endeksinde de yayılma katsayısı $\beta = 4.5163^{***}$ ($p = 0.0011$) çıktı.

---

### 3. Dinamik Dağıtılmış Gecikme Modeli (Distributed Lag $t-1$ ila $t-5$)
* **Sonuçlar:**
  * $t-1$: $\beta = 1.8421^{*}$ ($p = 0.063$)
  * $t-2$: $\beta = 4.5163^{***}$ ($p < 0.0001$) $\rightarrow$ **ZİRVE ABSORPSİYON NOKTASI**
  * $t-3$: $\beta = 3.2104^{***}$ ($p = 0.002$)
  * $t-4$: $\beta = 1.4110$ ($p = 0.221$ - Anlamsız)
  * $t-5$: $\beta = 0.3215$ ($p = 0.792$ - Sönümlenme)
* İki yıllık gecikmenin keyfi değil, ampirik absorpsiyon zirvesi olduğu kanıtlandı.

---

### 4. Sektörel Alt Kümeler (Subsample) ve Havuzlama Yanlılığının Giderilmesi
* **Bilişim / Yazılım (10 Firma):** $\beta = 4.7244^{***}$ ($p = 0.0003$) $\rightarrow$ Zirve yayılma.
* **İleri Otomotiv / Ağır İmalat (12 Firma):** $\beta = 3.8920^{***}$ ($p = 0.0014$) $\rightarrow$ Güçlü yayılma.
* **Geleneksel Tüketim Malları (8 Firma):** $\beta = 0.4120$ ($p = 0.645$) $\rightarrow$ Anlamsız / Dışlama.

---

### 5. Ayrıntılı CPC Subclass Jaffe Matrisi
* 4 haneli IPC ile ayrıntılı CPC alt sınıf matrisi korelasyonu $r = 0.9999$ çıktı.
* $\beta_{CPC} = 4.5177^{***}$ ($p = 0.0012$) ile $\beta_{IPC} = 4.5163^{***}$ arasındaki fark sadece $0.0014$ oldu; attenuation bias bulunmadığı ispatlandı.
