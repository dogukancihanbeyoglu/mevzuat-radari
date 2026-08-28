---
name: superpowers-workflow
description: Karmaşık mimari değişiklikler ve büyük özellik geliştirmeleri için 6 adımlı disiplinli mühendislik iş akışını (Define -> Plan -> Test -> Build -> Verify -> Ship) zorunlu kılar.
---

# Superpowers: Disiplinli Mühendislik İş Akışı

Bu beceri, karmaşık, çok adımlı veya mimari risk içeren görevlerde ajanın doğrudan koda dalmasını engelleyip yapılandırılmış bir mühendislik döngüsü izlemesini sağlar.

## İş Akışı Aşamaları

### 1. Tanımla (Define & Scope)
- Kullanıcının gereksinimlerini ve sistemin mevcut durumunu analiz et.
- Çözülmek istenen problemin sınırlarını (in-scope / out-of-scope) netleştir.
- Belirsizlik veya varsayım varsa varsayımları doğrulamadan koda geçme.

### 2. Planla (Plan & Architecture)
- Değişiklik yapılacak dosya ve modülleri tespit et.
- Veri modellerini, API sözleşmelerini ve olası yan etkileri (side effects) listele.
- Geriye dönük uyumluluk (backward-compatibility) risklerini değerlendir.

### 3. Test Tasarımı (Test First)
- Yazılacak özelliğin doğruluğunu kanıtlayacak test senaryolarını (unit, integration veya e2e) belirle.
- Hata düzeltmelerinde, hatayı yeniden üreten (reproduce eden) bir test oluştur.

### 4. Geliştirme (Incremental Build)
- Değişiklikleri atomik ve mantıksal bloklar halinde uygula.
- Tek seferde devasa, takip edilemez diff'ler yerine modüler adımlarla ilerle.
- Kod standartlarına ve tip güvenliğine sıkı sıkıya bağlı kal.

### 5. Doğrulama (Automated & Manual Verification)
- Tüm test suite'lerini ve linter/tip kontrollerini çalıştır.
- Başarısız olan senaryoları analiz et ve düzelt.
- Performans veya bellek tüketimi etkilerini gözlemle.

### 6. Teslim (Review & Ship)
- Yapılan değişiklikleri, eklenen testleri ve doğrulama sonuçlarını özetleyen açık bir rapor sun.
