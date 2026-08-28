---
name: tdd-enforcer
description: Test-Driven Development (TDD) metodolojisini uygulayarak önce başarısız testi (Red), ardından minimum çalışan kodu (Green) ve son olarak refactoring adımlarını yürütür.
---

# Test-Driven Development (TDD) Enforcer

Bu beceri, kodun test edilebilirliğini ve hatasızlığını garanti altına almak için klasik TDD döngüsünü zorunlu kılar.

## TDD Döngüsü

### 1. Kırmızı Aşama (Red Phase)
- İstenen davranış veya giderilecek hata için bir test dosyası / senaryosu oluştur.
- Testi çalıştır ve **beklenen nedenden ötürü başarısız olduğunu (Failed / Red)** teyit et.
- Testin geçtiğini görmeden asıl iş kodunu yazmaya başlama.

### 2. Yeşil Aşama (Green Phase)
- Testin başarılı olmasını (Passed / Green) sağlayacak **yalnızca gerekli minimum kodu** yaz.
- Erken optimizasyon veya testin kapsamadığı ekstra özellikleri bu aşamada ekleme.
- Testi çalıştırarak yeşile döndüğünü doğrula.

### 3. İyileştirme Aşaması (Refactor Phase)
- Testler yeşilken kodu temizle:
  - Kod tekrarlarını (DRY) temizle.
  - İsimlendirmeleri ve okunabilirliği iyileştir.
  - Fonksiyonel bütünlüğü ve tip tanımlarını sıkılaştır.
- Refactoring sonrası testleri tekrar çalıştırarak bozulma olmadığını onayla.

## Test Kapsamı Yönergeleri
- **Happy Path:** Normal girdi ve başarılı durumlar.
- **Edge Cases:** Boş diziler, null/undefined, sınır değerler, çok büyük veri kümeleri.
- **Error Handling:** Geçersiz argümanlar, ağ/veritabanı hataları ve istisna fırlatma senaryoları.
