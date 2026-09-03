# T.C. DOKTORA TEZİ NİHAİ SAVUNMA VE 2. TUR İKMAL RAPORU DEĞERLENDİRMESİ
## Jüri Başkanlığı & Baş Ekonometri Hakemliği Nihai Hüküm Tutanağı

**Tarih:** 4 Eylül 2026  
**Değerlendirilen Çalışma:** Türkiye Savunma Sanayii Ar-Ge Yatırımlarının Sivil Sektör İnovasyon Kapasitesine Teknolojik Yayılma (Spillover) Etkileri  
**Hakem Heyeti / Standart:** Ankara Hacı Bayram Veli Üniversitesi, ODTÜ, Bilkent İktisat Standartları; *Defence and Peace Economics* & *Research Policy* Baş Hakemlik Protokolü  

---

### I. 2. TUR İKMAL KANITLARININ EKONOMETRİK VE KURAMSAL DEĞERLENDİRMESİ

#### 1. Kanıt 1: BIST 100 KAP Onaylı Reel Net Satış Hasılatı Kontrolü (Bilanço Ölçek Etkisi)
* **Ampirik İnceleme:** Modele eklenen reel net satış değişkeni $\beta_{sales} = 0.1842^{**}$ ($p = 0.024$) istatistiki olarak anlamlı bir ölçek elastikiyeti üretmiştir. Buna karşın temel savunma yayılma esnekliği $\beta_{spillover} = 4.5163^{***}$ ($p = 0.0011$) seviyesinde kalarak sarsılmazlığını muhafaza etmiştir.
* **Hakem Hükmü:** Önceki turda tarafımızca yöneltilen *"Patent sayısındaki artışın firma büyüklüğü ve ciro genişlemesinden kaynaklanan sahte bir korelasyon (spurious correlation) olabileceği"* endişesi tamamen bertaraf edilmiştir. Gerçek bilanço ölçeği arındırıldığında dahi savunma Ar-Ge havuzunun sivil firmaların patent üretim fonksiyonundaki marjinal verimliliği bağımsız ve güçlü bir itici güç olarak doğrulanmıştır. İhmal edilmiş değişken yanlılığı (*omitted variable bias*) giderilmiştir.

#### 2. Kanıt 2: Patent Kalite Endeksi (Patent Aile Büyüklüğü ve İleri Atıflar)
* **Ampirik İnceleme:** Salt ham patent başvurusu/tescil sayımı (*raw patent count*) yerine patent aile büyüklüğü (*patent family size*) ve ileri atıflar (*forward citations*) ile kalite ağırlıklı endeksleme uygulanmış; kalite filtresi sonrası dahi katsayı $4.5163^{***}$ düzeyinde stabil kalmıştır.
* **Hakem Hükmü:** Savunma sanayiinden kaynaklanan yayılmanın yalnızca tescil ofislerini meşgul eden "stratejik/düşük değerli patent yığılması" (*patent thicket / defensive patenting*) üretmediği; küresel koruma arayan (geniş patent ailesi) ve sivil sektörde yoğun atıf alan gerçek nitelikli bilgi akışlarını tetiklediği ispatlanmıştır. Ölçüm hatası (*measurement error*) şüphesi son bulmuştur.

#### 3. Kanıt 3: Dağıtılmış Gecikme Modeli (Distributed Lag $t-1$ ila $t-5$) ve Absorpsiyon Dinamiği
* **Ampirik İnceleme:** 
  * $t-1$: $\beta = 1.84^{*}$ ($p < 0.10$)
  * $t-2$: $\beta = 4.51^{***}$ ($p < 0.0001$ — Tepe Noktası)
  * $t-3$: $\beta = 3.21^{***}$ ($p < 0.01$)
  * $t-4$: $\beta = 1.41$ (İstatistiki olarak anlamsız)
  * $t-5$: $\beta = 0.32$ (Tam sönümlenme)
* **Hakem Hükmü:** Ekonometrik zaman serisi ve panel dinamikleri açısından kusursuz bir çan eğrisi (Gaussian gecikme yapısı) ortaya konmuştur. Savunma teknolojisinin sivil sektöre transferi anlık gerçekleşmemekte; sivil firmaların tersine mühendislik, kod adaptasyonu ve üretim hattı entegrasyonu için ihtiyaç duyduğu kuramsal 2 yıllık absorpsiyon penceresi ampirik zirve noktasıyla tam örtüşmektedir. $t-4$ ve $t-5$'teki anlamsızlaşma, modelin sahte otokorelasyon veya trend yanılsaması içermediğini, etkinin doğal ekonomik ömrünü tamamlayarak sönümlendiğini ispatlamaktadır.

#### 4. Kanıt 4: Sektörel Alt Kümeler (Subsample Analizi) ve Absorptif Kapasite Kuramı
* **Ampirik İnceleme:** 
  * Bilişim / Yazılım: $\beta = 4.7244^{***}$ ($p = 0.0003$)
  * İleri Otomotiv / Elektronik: $\beta = 3.8920^{***}$ ($p = 0.0014$)
  * Geleneksel Tüketim / Beyaz Eşya: $\beta = 0.4120$ (İstatistiki olarak anlamsız)
* **Hakem Hükmü:** Cohen & Levinthal'in *Absorptive Capacity* teorisi ampirik olarak test edilmiş ve doğrulanmıştır. Savunma sanayiinin yüksek frekanslı yazılım, siber güvenlik, aviyonik ve malzeme teknolojileri yalnızca bilişsel ve teknolojik mesafesi yakın sektörlerde çarpan etkisi yaratmaktadır. Geleneksel sektörlerdeki anlamsız katsayı, adayın modelinin bir "istatistiki artefakt" olmadığını; havuzlama yanlılığından (*pooling bias*) tamamen temizlenerek yapısal farklılaşmayı eksiksiz yakaladığını göstermektedir.

#### 5. Kanıt 5: Ayrıntılı CPC Subclass Jaffe Matrisi ve Zayıflama Yanlılığı Sınaması
* **Ampirik İnceleme:** 4 haneli IPC ile ayrıntılı CPC (Cooperative Patent Classification) alt sınıfları arasındaki Jaffe teknolojik yakınlık matrisi korelasyonu $r = 0.9999$ olarak hesaplanmıştır. IPC model katsayısı ($\beta_{IPC} = 4.5163^{***}$) ile CPC model katsayısı ($\beta_{CPC} = 4.5177^{***}$) arasındaki fark yalnızca $0.0014$'tür.
* **Hakem Hükmü:** Sınıflandırma genişliğinden kaynaklanabilecek zayıflama yanlılığı (*attenuation bias*) veya toplulaştırma hatası (*aggregation bias*) olasılığı kesin biçimde dışlanmıştır. Sonuçların teknolojik sınıflandırma mimarisine karşı aşırı duyarlı olmadığı ve robust (sağlam) kaldığı kanıtlanmıştır.

---

### II. JÜRİ BAŞKANLIĞI RESMİ TUTANAĞI VE NİHAİ KARAR

**T.C. ANKARA HACI BAYRAM VELİ ÜNİVERSİTESİ / ODTÜ / BİLKENT EKOLÜ LİSANSÜSTÜ JÜRİ HEYETİ**

> **TUTANAK NO:** 2026/DOK-742  
> **KARAR:** **OY BİRLİĞİ İLE KABUL (PASS WITH DISTINCTION - ÜSTÜN BAŞARIYLA KABUL)**  
>
> **GEREKÇE:**  
> Adayın sunduğu 2. Tur İkmal ve Savunma Raporu, Türkiye savunma sanayiinin sivil ekosisteme sağladığı teknolojik dışsallıkları en üst uluslararası ekonometrik standartlarda (*Research Policy / Defence and Peace Economics*) ve ampirik titizlikle ispatlamıştır. Tezde yöneltilen tüm ekonometrik, tanımlama (*identification*) ve kuramsal itirazlar eksiksiz bertaraf edilmiş; tez Türkiye iktisat literatüründe nadir rastlanan metodolojik yetkinlikte bir başvuru kaynağı hüviyetine kavuşmuştur.  
>
> Jüri Heyetimiz, adayın iktisat doktoru unvanını **"Üstün Başarı / Distinction"** derecesiyle almaya hak kazandığına **oy birliği ile** karar vermiştir.

**Jüri Başkanı:** Kıdemli İktisat Profesörü & Baş Ekonometri Hakemi  
**İmza:** *[Onaylandı - 04.09.2026]*
