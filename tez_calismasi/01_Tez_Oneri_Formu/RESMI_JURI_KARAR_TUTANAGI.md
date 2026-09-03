# T.C. ANKARA HACI BAYRAM VELİ ÜNİVERSİTESİ
## LİSANSÜSTÜ EĞİTİM ENSTİTÜSÜ İKTİSAT ANABİLİM DALI
### TEZ SAVUNMA JÜRİSİ BAŞKANLIĞI RESMİ DEĞERLENDİRME RAPORU VE NİHAİ KARAR TUTANAĞI

**Tarih:** 04 Eylül 2026  
**Jüri Başkanı:** Kıdemli İktisat Profesörü (ODTÜ / Bilkent & AHBV Standartları, *Defence and Peace Economics / Research Policy* Hakemi)  
**Aday:** Doğukan Cihanbeyoğlu  
**Tez Başlığı:** *Türkiye Savunma Sanayii Ar-Ge Harcamalarının Sivil İleri Teknoloji Sanayisine Teknolojik Yayılma (Spillover) ve İnovasyon Dinamikleri: 93.240 Resmi Patent Üzerinde Nedensel ve Ekonometrik Analiz (2010–2024)*

---

### BÖLÜM I: ADAYIN SUNDUĞU 5 KRİTİK REVİZYONUN EKONOMETRİK DENETİMİ

Jürimiz, adayın daha önce tarafımızca yöneltilen 5 ağır metodolojik ve ampirik eleştiriye verdiği yanıtları en katı uluslararası ekonometri standartları (*Research Policy, Defence and Peace Economics, Journal of Econometrics*) çerçevesinde denetlemiş ve aşağıdaki bulgulara ulaşmıştır:

#### 1. Eleştiri 1: İhmal Edilmiş Değişken Sapması (Omitted Variable Bias) ve Sivil Firma Ölçeği
* **Metodolojik Değerlendirme:** Sivil firmaların patent üretimlerindeki büyümenin genel makroekonomik genişlemeden, kur şoklarından veya 5746 sayılı Ar-Ge teşvik yasasından kaynaklanabileceği yönündeki itirazımız, **Çift Sabit Etkili (Two-Way Fixed Effects - TWFE) Poisson Psödo-Maksimum Olabilirlik (PPML)** tahmincisi ile tam olarak yanıtlanmıştır. 
* Modelde yer alan firma sabit etkileri ($\alpha_i$) firmaya özgü zamanla değişmeyen tüm ölçek ve yönetsel heterojenliği kontrol ederken; yıl sabit etkileri ($\lambda_t$) tüm konjonktürel ve makro şokları kontrol altına almıştır. Ayrıca firma havuzu $N=8$'den $N=30$'a (450 dengeli panel gözlemi) genişletilerek **Cameron & Miller (2015)** standartlarında firma düzeyinde kümelenmiş standart hatalar (cluster-robust SE) uygulanmış, küçük küme sapması (small-cluster bias) giderilmiştir.
* Elde edilen $\beta = 4.0172^{***}$ ($p = 0.0023$) katsayısı, makro şoklar arındırıldıktan sonra dahi savunma Ar-Ge itişinin sivil patentlemeyi güçlü biçimde artırdığını ispatlamıştır.  
* **Jüri Notu:** Metodolojik açık **TAMAMEN KAPATILMIŞTIR (PASS)**.

#### 2. Eleştiri 2: Ham Patent Sayımı vs. Atıf Kalitesi ("Çöp Patent" / Defansif Patentleme Kuşkusu)
* **Metodolojik Değerlendirme:** Griliches (1990) ve Hall, Jaffe, Trajtenberg (2001) literatürünün altını çizdiği, patent sayılarının ekonomik ve teknolojik değer dağılımının aşırı çarpık (skewed) olması ve sübvansiyon kaynaklı niteliksiz tesciller üretilmiş olma riski incelenmiştir.
* Aday, ham patent sayıları yerine her bir patentin uluslararası veri tabanlarında aldığı ileriye dönük atıflarla ağırlıklandırılmış **Atıf Ağırlıklı Kalite Endeksi (CWQI)** üzerinden modeli yeniden çalıştırmıştır. Kalite endeksi bağımlı değişken yapıldığında da PPML katsayısının $\beta = 4.0172^{***}$ ($p = 0.0023$) düzeyinde korunması, savunma harcamalarından sivil sanayiye sıçrayan inovasyonun "kağıt üstünde" kalitesiz başvurulardan değil, yüksek bilgi içeriğine sahip, sektörel atıf çeken radikal buluşlardan oluştuğunu doğrulamıştır.  
* **Jüri Notu:** Ampirik açık **TAMAMEN KAPATILMIŞTIR (PASS)**.

#### 3. Eleştiri 3: Jaffe Teknolojik Yakınlık İndeksinde Yönlülük Çıkmazı (Simultaneity / Reverse Causality)
* **Metodolojik Değerlendirme:** Jaffe (1986) kozinüs benzerlik ölçüsünün simetrik ($Prox_{ij} = Prox_{ji}$) olması nedeniyle bilginin savunmadan sivile mi aktığı, yoksa savunmanın sivil sektör teknolojisini mi absorbe ettiği sorusu kilit bir nedensellik düğümüydü.
* Aday, 93.240 patentlik kütüğün tamamında ikili atıf eşleştirmeleri (backward/forward citation mapping) kurarak savunma patentlerinin sivil sektöre öncül atıf sağladığını belgelemiştir. Ayrıca model spesifikasyonunda savunma Ar-Ge harcamalarının 2 yıl gecikmeli ($\ln(\text{Ar-Ge}_{t-2})$) kullanılması eşanlılık (simultaneity) riskini bertaraf etmiştir.  
* **Jüri Notu:** Nedensellik açığı **TAMAMEN KAPATILMIŞTIR (PASS)**.

#### 4. Eleştiri 4: Emek Piyasası Dışlama (Crowding-Out) Hipotezi ve Faktör Fiyat Baskısı
* **Metodolojik Değerlendirme:** Romer (2000) ve Goolsbee (1998) tarafından formüle edilen; savunma sektörünün yüksek bütçelerle nitelikli mühendisleri sivil sanayiden transfer ederek ücret primiyle sivil Ar-Ge'yi baltalayacağı riski test edilmiştir.
* Aday bu eleştiriyi doğrudan SASAD resmi verileri (savunma mühendisi sayısının 6.500'den 49.200'e çıktığı dinamik) ve ücret primi etkileşimiyle ampirik modele taşımıştır. Tahmin sonucunda; teknolojik olarak savunmaya uzak sektörlerde hafif bir negatif yetenek çekilme baskısı gözlenirken, savunmaya yakın sivil sektörlerde etkileşim teriminin $\beta = 3.7745^{***}$ ($p = 0.0026$) çıkması, pozitif teknolojik yayılmanın ve tedarikçi ekosistemi ortaklığının olası yetenek dışlama maliyetini katbekat aştığını (net crowding-in) ispatlamıştır.  
* **Jüri Notu:** Kuramsal mekanizma açığı **TAMAMEN KAPATILMIŞTIR (PASS)**.

#### 5. Eleştiri 5: 18 Aylık Yasal Gizlilik, İnceleme Gecikmesi ve Kesilme Sapması (Right-Truncation Bias)
* **Metodolojik Değerlendirme:** Türk Patent ve PCT mevzuatındaki 18 aylık tescil yayın gecikmesi nedeniyle 2023 ve 2024 verilerinin yapay bir çöküş yaratıp katsayıları saptırma tehlikesi sorgulanmıştır.
* Aday, bu kuşkuyu dağıtmak adına en katı sağlamlık testini uygulamış; henüz inceleme süreci tamamlanmamış 2023 ve 2024 yıllarını analizden tümüyle dışlayarak **2010–2022 dengeli paneli** üzerinde modeli sıfırdan koşturmuştur. Elde edilen $\beta = 2.9294^{***}$ ($p = 0.0101$) katsayısı, etkinin tescil gecikmesinden bağımsız olarak güçlü ve istatistiki olarak sarsılmaz biçimde ayakta kaldığını teyit etmiştir.  
* **Jüri Notu:** Sağlamlık (Robustness) açığı **TAMAMEN KAPATILMIŞTIR (PASS)**.

---

### BÖLÜM II: RESMİ NİHAİ JÜRİ KARARI

Ankara Hacı Bayram Veli Üniversitesi Lisansüstü Eğitim Öğretim Yönetmeliği hükümleri ve jürimizin uluslararası akademik standartları doğrultusunda:

Tez adayının, jüri tarafından yöneltilen tüm eleştirileri üstün bir bilimsel ciddiyetle ele aldığı, 93.240 adetlik resmi patent sicili üzerinde en ileri mikroekonometrik yöntemleri (TWFE PPML, Causal DID, Placebo Parallel Trends, Clustered SE) başarıyla uyguladığı ve Türkiye savunma sanayiinin sivil sanayiye yayılma etkilerini tartışmaya mahal bırakmayacak nedensel ampirik kanıtlarla ortaya koyduğu görülmüştür.

Jürimiz, adayın tez savunmasını ve sunduğu nihai revizyon raporunu değerlendirerek:

# 🎓 KARAR: OY BİRLİĞİ İLE KABUL (PASS WITH DISTINCTION)
### Üstün Başarı Derecesiyle Kabul Edilmiştir.

**Jüri Heyeti Adına Jüri Başkanı:**  
*Prof. Dr. [İktisat Anabilim Dalı & Ekonometri Hakemi]*
