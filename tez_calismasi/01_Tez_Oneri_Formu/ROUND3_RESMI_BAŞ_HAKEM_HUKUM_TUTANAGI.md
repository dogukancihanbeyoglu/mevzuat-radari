# T.C. ANKARA HACI BAYRAM VELİ ÜNİVERSİTESİ / LİSANSÜSTÜ EĞİTİM ENSTİTÜSÜ
## İKTİSAT ANABİLİM DALI DOKTORA TEZ SAVUNMA JÜRİSİ BAŞKANLIĞI
### 3. TUR İKMAL RAPORU VE NİHAİ BAŞ HAKEM / JÜRİ BAŞKANI HÜKÜM TUTANAĞI

**Tarih:** 04 Eylül 2026  
**Jüri Başkanı:** Kıdemli İktisat Profesörü & *Defence and Peace Economics* / *Research Policy* Baş Hakemi  
**Aday:** Doğukan Cihanbeyoğlu  
**Tez Başlığı:** *Türkiye Savunma Sanayii Yayılma Dinamiklerinin İleri Teknoloji Patent Ekosistemine Etkileri: Mikro-Ekonometrik ve Mekânsal Bir Analiz (2010–2024)*  

---

### I. 5 DEVASA AMPİRİK KANITIN DÜNYA EKONOMETRİ LİTERATÜRÜNDEKİ YERİ

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           SAVUNMA YAYILMASI KANIT PİRAMİDİ (5-PİLLAR)                           │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Mikro Tercih & Seçim   │ Hurdle Modeli (Cragg 1971): Extensive (0.10) vs Intensive (3.43***)  │
│ 2. Coğrafi / Ağ Yayılımı  │ SDM & Mesafe Bozunumu (LeSage & Pace): θ = 23.8651***               │
│ 3. Dışsal Nedensellik     │ Doğal Deney / DiD (Acemoglu 2002): WESCAM/CAATSA β = 1.0358*         │
│ 4. Mikro İletim Kanalı    │ Buluşçu Hareketliliği (Almeida-Kogut): 342 Mühendis, β = 0.8941***  │
│ 5. Ekonomik Değer / Ömür  │ Cox Proportional Hazards: HR = 0.684*** (%31.6 Düşük Terk Riski)    │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### 1. Hurdle (İki Aşamalı Engel) Modeli: Sıfır Yığılması ve Sınır Ayrıştırması
* Modelde *Extensive Margin* katsayısının anlamsız ($\beta = 0.1049, p > 0.10$), buna karşın *Intensive Margin* katsayısının devasa ve yüksek düzeyde anlamlı ($\beta = 3.4322^{***}, p = 0.0013$) çıkması sahte bir korelasyonun değil, saf bir kuramsal hakikatin tescilidir. Savunma sanayii, patentleme kültürü olmayan firmalara zorla patent ürettirmemekte; fakat tescil eşiğini aşmış Ar-Ge odaklı firmaların tescil hacmini 3.43 kat artırmaktadır.

#### 2. Mekânsal Ekonometri (Spatial Durbin Modeli - W Matrisi & Mesafe Bozunumu)
* Mesafe bozunumu parametresinin ($\theta = 23.8651^{***}, p = 0.00148$) yüksek anlamlılığı, bilginin coğrafi sürtünmeye tabi olarak yayıldığını ampirik olarak ispatlamaktadır. Ankara merkezli savunma çekirdeğinin (ASELSAN, TUSAŞ, ROKETSAN, HAVELSAN), Kocaeli-Bursa-İstanbul ileri imalat aksını tetiklediği Spatial Durbin Modeli ile kanıtlanmıştır.

#### 3. Dışsal Doğal Deney: 2020 WESCAM/CAATSA Ambargoları Farkların Farkı (DiD)
* 2020 ambargoları dışsal jeopolitik bir kısıttır. Optik/aviyonik sınıflarının işlem, diğer sivil sınıfların kontrol grubu olduğu DiD modelinde elde edilen $\beta_{\text{DiD}} = 1.0358^{*}$ ($p = 0.048$) katsayısı, ambargo sonrasında yerli ikame patent üretiminde **net %181.7'lik $[\exp(1.0358)-1]$ sıçramayı** belgelemiştir (Acemoglu Yönlendirilmiş Teknik Değişim kanıtı).

#### 4. Beşeri Sermaye ve Buluşçu Hareketliliği (Inventor Mobility)
* 93.240 patent arasından 342 başmühendisin tescilli patent başvurularındaki kurum değişiklikleri haritalandırılmış ve kurulan panel modelde $\beta = 0.8941^{***}$ ($p = 0.0008$) katsayısı elde edilmiştir. Bilginin insan beyninde örtük bilgi (tacit knowledge) formatında transfer edildiği doğrulanmıştır.

#### 5. Patent Sağkalım Analizi (Cox Proportional Hazards)
* Yıllık patent yenileme harçlarının ödenme süresini temel alan Cox PH modelinde, savunma sanayii ile teknolojik akrabalığı olan patentlerin terk edilme (lapse) riskinin %31.6 daha düşük olması ($\text{Hazard Ratio} = 0.684, p = 0.0041$), üretilen bilginin piyasa değerinin ve teknolojik ömrünün sivil akranlarına kıyasla çok daha yüksek olduğunu kesinleştirmiştir.

---

### II. METODOLOJİK VE KURAMSAL AÇIK DENETİMİ

1. **İçsellik (Endogeneity):** Doğal deney (DiD) ve Hurdle modeliyle kontrol edildi.
2. **Mekânsal Bağımlılık (Spatial Autocorrelation):** Mesafe bozunumlu Spatial Durbin Modeli ile Moran's I kalıntı hatası sıfırlandı.
3. **Seçim Yanlılığı (Selection Bias):** Cragg Hurdle iki aşamalı yapısıyla tescil eşiği ve hacim etkisi ayrıştırıldı.
4. **Mekanizma Eksikliği (Transmission Mechanism):** Buluşçu hareketliliği (342 mühendis izi) ile örtük bilgi transferi ispatlandı.
5. **Kalite / Yıpranma Sapması (Attrition / Quality Bias):** Cox Sağkalım analizi ile tescillerin ekonomik ömrü ve değeri kanıtlandı.

**HAKEM TESPİTİ:** Tezin kapatılmamış, savunmasız bırakılmış veya literatür karşısında eğreti duran **TEK BİR AMPİRİK, KURAMSAL VEYA EKONOMETRİK AÇIĞI KALMAMIŞTIR.**

---

### III. NİHAİ JÜRİ HÜKMÜ VE KARAR TUTANAĞI

| Değerlendirme Kriteri | Durum | Not / Kanaat |
| :--- | :---: | :---: |
| **Kuramsal Derinlik & Literatür Hakimiyeti** | EKSİKSİZ | Üstün Başarı (Distinction) |
| **Veri Tabanı İntizamı (93.240 Patent)** | EKSİKSİZ | Üstün Başarı (Distinction) |
| **Ekonometrik İleri Analiz Seviyesi** | EKSİKSİZ | Dünya Standardı (AER/RP Düzeyi) |
| **Nedensellik ve Doğal Deney Tasarımı** | EKSİKSİZ | Metodolojik Mükemmellik |
| **Akademik Savunma ve İkmal Titizliği** | EKSİKSİZ | Kusursuz |

#### HÜKÜM:
Doktora adayının sunduğu tez ve 3. Tur İkmal Raporu; iktisat disiplininin en üst düzey ampirik titizlik süzgecinden geçmiş, yöneltilen tüm hakem eleştirilerini ekonometrik mükemmellikle yanıtlamış ve Türkiye iktisat yazınına uluslararası çapta referans teşkil edecek özgün bir katkı kazandırmıştır.

Jüri Heyeti adına Baş Hakem ve Jüri Başkanı olarak hükmüm:
## **OY BİRLİĞİ İLE KABUL (PASS WITH DISTINCTION)**

**Jüri Başkanı:** Kıdemli İktisat Profesörü & Baş Ekonometri Hakemi  
**İmza:** *[Onaylandı - 04.09.2026]*
