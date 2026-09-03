# AKADEMİK İKTİSAT TEZİ VE ARAŞTIRMA KURALLARI (AGENTS.MD)

Bu çalışma alanı, iktisat alanında yüksek lisans/doktora tezi ve akademik makale yazımı için yapılandırılmıştır. Tüm analiz ve metin üretimlerinde aşağıdaki kurallar istisnasız uygulanır:

---

## 1. AKADEMİK DÜRÜSTLÜK & %5 - %10 KURALI (MUTLAK KISIT)

1. **Benzerlik & İntihal Oranı (Turnitin/iThenticate Sınırı):**
   - Asla internetten, makalelerden veya kitaplardan doğrudan blok kopyalama yapma.
   - Fikirleri ve bulguları mutlaka derinlemesine yeniden ifade et (*deep paraphrasing*).
   - **Tekil kaynak benzerliği maksimum %3**, **toplam benzerlik oranı maksimum %10** olacak şekilde sentezleme yap.

2. **Doğrudan Alıntı Kuralı:**
   - Tezin veya makalenin toplam hacminin en fazla **%5'i** tırnak içi veya blok doğrudan alıntı olabilir. Alıntılar yerine kavramsal tartışma ve yazarın kendi analizi ön planda tutulmalıdır.

3. **Yapay Zekâ Kullanımı & Tespit Skoru (AI Detection - GPTZero / Turnitin):**
   - Yapay zekâ metin dedektörlerinin yakaladığı mekanik kalıplardan kesinlikle kaçın:
     - *Yasaklı/Aşırı Klişe Kelimeler:* "Delve into", "tapestry", "crucial role", "testament to", "pivotal", "beacon", "furthermore/moreover" (ardı ardına kullanımı).
   - Cümle boylarını dramatik biçimde çeşitlendir (kısa, orta, uzun ve bileşik cümle dengesi - yüksek *burstiness*).
   - Ekonometrik ve teknik terminolojiyi organik bağlamında kullan; genelleyici ve süslü boş laflardan kaçın.

4. **Atıf ve Kaynakça Doğruluğu (Sıfır Halüsinasyon):**
   - Asla hafızadan uydurma kaynak, hayali makale veya sahte DOI yazma.
   - Tüm atıflar Crossref, OpenAlex, Semantic Scholar veya kullanıcının Zotero kütüphanesinden doğrulanmış gerçek yayınlar olmalıdır.
   - Emin olunmayan veya doğrulanamayan hiçbir kaynağı metne dahil etme.

---

## 2. EKONOMETRİK METODOLOJİ VE AMPİRİK STANDARTLAR

1. **Nedensel Tanımlama (Causal Identification):**
   - Ampirik çalışmalarda sadece korelasyona değil, nedenselliğe odaklan.
   - İlgili stratejiyi (Farkların Farkı / DID, Regresyon Süreksizliği / RDD, Araç Değişkenler / IV-2SLS, Panel Sabit Etkiler, Sentetik Kontrol veya Zaman Serisi VAR/VECM) Angrist-Pischke ve Wooldridge standartlarına göre temellendir.
   - İçsellik (endogeneity), seçilim yanlılığı (selection bias) ve ters nedensellik (reverse causality) risklerini açıkça tartış ve test et.

2. **Kodlama ve Tekrarlanabilirlik (Reproducibility):**
   - Ekonometrik kodlar R, Stata veya Python kullanılarak yazılmalıdır.
   - Regresyon tabloları akademik standartlarda (katsayı, kümelenmiş standart hatalar / clustered SE, t/z değerleri, gözlem sayısı, R2, F-istatistiği) sunulmalıdır.

---

## 3. AKADEMİK YAZIM MİMARİSİ (JOHN COCHRANE & DEIRDRE MCCLOSKEY İLKELERİ)

1. **Giriş Bölümü (Introduction):**
   - İlk paragrafta konuyu doğrudan araştırma sorusuna bağla; gereksiz tarihsel girişlerden kaçın.
   - Makalenin literatüre sağladığı **somut 3 katkıyı (contribution)** açıkça maddeler halinde belirt.
   - Ana bulguları Giriş bölümünde gizleme; ilk birkaç sayfada ana sonucu doğrudan ver.

2. **Literatür Taraması:**
   - Makaleleri tek tek özetleyen bir "katalog" yazma; literatürü temalar, metodolojiler ve birbiriyle çelişen bulgular üzerinden **sentezle**.

3. **LaTeX Standartları:**
   - Tüm matematiksel model ve denklemleri standart LaTeX notasyonuyla (`amsmath`, `booktabs`) yaz.
