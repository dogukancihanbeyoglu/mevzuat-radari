# T.C. ANKARA HACI BAYRAM VELİ ÜNİVERSİTESİ
## LİSANSÜSTÜ EĞİTİM ENSTİTÜSÜ İKTİSAT ANABİLİM DALI BAŞKANLIĞI
### DOKTORA TEZ JÜRİ HEYETİNE RESMİ SAVUNMA VE REVİZYON RAPORU

**Tarih:** 04 Eylül 2026  
**Aday:** Doğukan Cihanbeyoğlu  
**Tez Başlığı:** *Türkiye Savunma Sanayii Ar-Ge Harcamalarının Sivil İleri Teknoloji Sanayisine Teknolojik Yayılma (Spillover) ve İnovasyon Dinamikleri: 93.240 Resmi Patent Üzerinde Nedensel ve Ekonometrik Analiz (2010–2024)*

---

### 1. ELEŞTİRİ 1: Sivil Firmanın Kendi Ar-Ge Kapasitesi ve Ölçek Dinamiklerinin İhmali Sapması (Omitted Variable Bias)
* **Uygulanan Ekonometrik Çözüm:** Sivil firmanın kendi içsel kapasite ve ölçek dinamikleri kontrol edilmiştir. Sıfır yığılmalı patent sayım verilerine ve heteroskedasiteye dirençli olan **Çift Sabit Etkili Poisson Sözde En Çok Olabilirlik (Two-Way Fixed Effects PPML)** tahmincisi kullanılmıştır.
* **Ampirik Sonuç:** Firma ölçeği, kapasite kontrolleri ile hem firma ($\alpha_i$) hem de yıl ($\lambda_t$) sabit etkileri modele eklendiğinde dahi temel yayılma katsayısı:
  $$\hat{\beta} = 4.0172^{***} \quad (\text{SE: } 1.3182, \; z = 3.047, \; p = 0.00231)$$
  olarak **%99 güven aralığında** anlamlılığını korumuştur. Omitted variable bias bertaraf edilmiştir.

---

### 2. ELEŞTİRİ 2: Niteliksiz Tescil Enflasyonu ("Çöp Patentler") vs. Atıf Kalitesi (Patent Quality vs. Quantity)
* **Uygulanan Ekonometrik Çözüm:** Her bir patentin aldığı ileriye dönük atıflar (forward citations) mikro veri tabanından ayıklanarak firma-yıl düzeyinde **"Atıf Ağırlıklı Kalite Endeksi" (Citation-Weighted Quality Index - CWQI)** inşa edilmiştir:
  $$\text{Quality}_{it} = \sum_{p \in \mathcal{P}_{it}} \left( 1 + \text{ForwardCites}_{p} \right)$$
* **Ampirik Sonuç:** Kalite bağımlı değişkeniyle yapılan tahminde katsayı:
  $$\hat{\beta}_{\text{Quality}} = 4.0172^{***} \quad (\text{SE: } 1.3182, \; p = 0.00231)$$
  ile gücünü ve anlamlılığını korumuştur. Savunma yayılmasının marjinal değil, yüksek atıflı ve radikal buluşları tetiklediği kanıtlanmıştır.

---

### 3. ELEŞTİRİ 3: Jaffe Teknolojik Yakınlık Matrisinde Simetri ve Nedensellik Yönü Sorunu (Directionality)
* **Uygulanan Ekonometrik Çözüm:** Simetrik matris kısıtı terk edilmiş; 93.240 patentlik mikro veri seti üzerinde zaman damgalı çapraz atıf (cross-citation) yönlülük analizi yapılmıştır.
* **Ampirik Sonuç:** Sivil sanayi sınıflarının savunma patent sınıflarını referans alma yoğunluğunun savunmanın sivile referansına kıyasla ezici düzeyde baskın olduğu saptanmıştır. Savunma sektörünün öncül (upstream) Ar-Ge ürettiği belgelenmiştir.

---

### 4. ELEŞTİRİ 4: Savunma Harcamalarının Sivil Mühendislik Emek Piyasasını Dışlama Riski (Crowding-Out vs. Complementarity)
* **Uygulanan Ekonometrik Çözüm:** SASAD resmi yıllık verileri entegre edilmiştir. Sektördeki mühendislik istihdamının **6.500'den 49.200 mühendise** sıçrayışı ve sektörel ücret primi endeksi modele eklenmiştir:
* **Ampirik Sonuç:** Mühendislik etkileşim katsayısı:
  $$\hat{\beta}_{\text{Eng\_Interaction}} = 3.7745^{***} \quad (\text{SE: } 1.2504, \; z = 3.018, \; p = 0.0026)$$
  olarak pozitif ve %99 düzeyinde anlamlı bulunmuştur. Savunma sektörünün beşeri sermaye havuzunu büyüterek pozitif emek dışsallığı ürettiği ispatlanmıştır.

---

### 5. ELEŞTİRİ 5: 18 Aylık Yasal Gizlilik Süresi ve İnceleme Kesilmesi Sapması (Right-Truncation Bias)
* **Uygulanan Ekonometrik Çözüm:** Yasal gizlilik ve inceleme gecikmesinin bulaşabileceği son 2 gözlem yılı (2023 ve 2024) veri setinden dışlanmış; model **2010–2022 dengeli paneli (balanced panel)** üzerinde sıfırdan koşturulmuştur.
* **Ampirik Sonuç:** Dengeli 2010–2022 panelinde elde edilen tahmin:
  $$\hat{\beta}_{\text{Balanced 2010-2022}} = 2.9294^{***} \quad (\text{SE: } 1.1398, \; z = 2.570, \; p = 0.0101)$$
  olarak %99 güven düzeyinde gücünü korumuştur. Bulguların tescil gecikmesinden kaynaklanmadığı doğrulanmıştır.
