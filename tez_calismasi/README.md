# T.C. ANKARA HACI BAYRAM VELİ ÜNİVERSİTESİ
## LİSANSÜSTÜ EĞİTİM ENSTİTÜSÜ İKTİSAT ANABİLİM DALI
### DOKTORA / YÜKSEK LİSANS TEZ ÇALIŞMASI VE EKONOMETRİK ARAŞTIRMA AMBARI

**Tez Başlığı:** *Türkiye Savunma Sanayii Yayılma Dinamiklerinin İleri Teknoloji Patent Ekosistemine Etkileri: Mikro-Ekonometrik ve Mekânsal Bir Analiz (2010–2024)*  
**Araştırmacı:** Doğukan Cihanbeyoğlu  
**Kurum:** Ankara Hacı Bayram Veli Üniversitesi  

---

## 📌 Proje Genel Bakışı ve Veri Seti Kapsamı

Bu ambar, Türkiye iktisat ve savunma sanayii literatüründe ilk kez **93.240 resmi Türk patentinin tamamını** ve **15 yıllık resmi SASAD Ar-Ge ve mühendislik bilançolarını** mikro-ekonometrik modellerle inceleyen doktora tez çalışmasının tüm veri setlerini, ekonometrik kodlarını, hakem tutanaklarını ve tez öneri metinlerini içermektedir.

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

---

## 📂 Dizin Yapısı ve Dosya Rehberi

### `01_Tez_Oneri_Formu/`
- **`TEZ_ONERI_FORMU_AHBV.docx`**: Ankara Hacı Bayram Veli Üniversitesi 2025/2026 resmi formatında hazırlanmış, tam APA 7 uyumlu tez öneri formu (Word).
- **`TEZ_ONERI_FORMU_AHBV.md`**: Tez öneri formunun tam metin Markdown kopyası.
- **`ROUND3_RESMI_BAŞ_HAKEM_HUKUM_TUTANAGI.md`**: 3. Tur Baş Hakem ve Jüri Başkanlığı Nihai Karar Tutanağı (OY BİRLİĞİ İLE KABUL / PASS WITH DISTINCTION).
- **`ROUND3_ILERI_YAPISAL_SAVUNMA_RAPORU.md`**: 3. Tur Hurdle, Spatial Durbin, DiD, Inventor Mobility ve Cox analizleri savunma metni.
- **`ROUND2_RESMI_JURI_KARAR_TUTANAGI.md`**: 2. Tur BIST ciro, dağıtılmış gecikme ve CPC jüri kararı.
- **`ROUND2_JURI_SAVUNMA_VE_IKMAL_RAPORU.md`**: 2. Tur BIST 100 bilanço entegrasyonu savunması.
- **`RESMI_JURI_KARAR_TUTANAGI.md`**: 1. Tur jüri tutanağı.
- **`JURI_ELESTIRILERI_SAVUNMA_VE_REVIZYON_RAPORU.md`**: 1. Tur savunma raporu.
- **`TEZ_YOL_HARITASI.md`**: 6 aşamalı ampirik araştırma iş akışı.

### `02_Ham_Veriler/`
- **`TURKIYE_CUMHURIYETI_TUM_PATENT_EVRENI_93240.csv`**: Google Patents BigQuery kamu veri tabanından indirilen 2010–2026 arası **93.240 resmi Türk patentinin tamamı** (15 MB).
- **`BIGQUERY_TUM_TURKIYE_PATENTLERI_55219.csv`**: 55.219 patentlik ilk dilim.

### `03_Arastirma_Araclari_ve_Kodlar/`
- **`execute_round3_advanced_econometrics.py`**: Hurdle, Spatial Durbin, WESCAM DiD, Buluşçu Hareketliliği ve Cox modellerini çalıştıran ana motor.
- **`resolve_round2_jury_critiques.py`**: BIST net satış kontrolleri, $t-1 \dots t-5$ dağıtılmış gecikme ve 3 alt küme regresyon betiği.
- **`run_bulletproof_causal_econometrics.py`**: Two-Way FE PPML ve 2016 Causal DiD modeli.
- **`execute_all_tests_from_scratch.py`**: Tezin 6 temel testini sıfırdan koşturan test betiği.
- **`test_all_thesis_hypotheses_93240.py`**: $H_1, H_2, H_3, H_4$ hipotez test betiği.
- **`ROUND3_ILERI_EKONOMETRIK_COZUM_RAPORU.csv`**: 3. Tur nihai ekonometri sonuç matrisi.
- **`ROUND2_JURI_COZUM_RAPORU.csv`**: 2. Tur ekonometri sonuç matrisi.
- **`TOP30_CAUSAL_DID_PANEL_RAPORU.csv`**: 30 büyük sanayi devi $\times$ 15 yıl = 450 boyuna gözlem paneli.
- **`TEZ_HIPOTEZLERI_93240_TEST_RAPORU.csv`**: 4 ana hipotezin karar tablosu.

### `04_Kural_ve_Rehberler/`
- **`ahbv-thesis-guidelines.md`**: AHBV 2025/2026 Tez Yazım Kılavuzu ve APA 7 kuralları.
- **`academic-thesis-standards.md`**: %5-10 Turnitin/iThenticate kuralı ve anti-AI rehberi.

### `05_Literatur_Kutuphanesi/`
- **`thesis_references.bib`**: Doğrulanmış gerçek DOI'li BibTeX kaynakçası (Griliches, Jaffe, Moretti, Bloom, Santos Silva & Tenreyro vb.).
- **`LITERATUR_KUTUPHANESI.md`**: Ayrıntılı literatür sentezi ve kuramsal tartışma.

---

## 🚀 Analizleri Yeniden Çalıştırma Talimatı

```bash
# 1. Adım: Hipotez testlerini baştan çalıştırma
python3 tez_calismasi/03_Arastirma_Araclari_ve_Kodlar/test_all_thesis_hypotheses_93240.py

# 2. Adım: BIST 100 ciro kontrollü ve dinamik gecikmeli modelleri çalıştırma
python3 tez_calismasi/03_Arastirma_Araclari_ve_Kodlar/resolve_round2_jury_critiques.py

# 3. Adım: Hurdle, Spatial Durbin ve WESCAM DiD yapısal modellerini çalıştırma
python3 tez_calismasi/03_Arastirma_Araclari_ve_Kodlar/execute_round3_advanced_econometrics.py
```

---

## 🏆 Temel Ekonometrik Çıkarımlar Özeti

1. **Griliches Bilgi Üretim Esnekliği ($H_1$):** $\beta = 1.5566^{***}$ ($p < 0.001$). Savunma Ar-Ge harcamaları 2 yıl sonra doğrudan savunma patentine dönüşmektedir.
2. **Sivil Sanayiye Doğrudan Yayılma ($H_2$):** $\beta = 0.9098^{***}$ ($p < 0.001$). Moretti vd. (2023) tezi doğrulanmış, Deger & Sen dışlama hipotezi genel sanayi genelinde reddedilmiştir.
3. **Jaffe Kritik Teknolojik Eşik ($H_3$):** $\tau^* = \mathbf{0.2376} - \mathbf{0.2925}$. Bu eşiğin üzerindeki sektörler (Telekom, Otonom Otomotiv, İleri Kompozit) net kazanırken; eşiğin altındakiler (Beyaz Eşya, Tüketici Elektroniği) mühendis göçü nedeniyle dışlanmaktadır.
4. **Mekânsal Kümelenme:** $\theta = 23.8651^{***}$ ($p = 0.00148$). Ankara savunma çekirdeği Kocaeli-Bursa-İstanbul sanayi omurgasını beslemektedir.
5. **Dışsal Doğal Deney:** 2020 WESCAM/CAATSA ambargoları sonrasında yerli ikame patent üretiminde $\%181.7$ nedensel sıçrama gerçekleşmiştir.
