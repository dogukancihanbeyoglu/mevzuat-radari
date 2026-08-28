---
name: code-quality-auditor
description: Proje kod tabanını güvenlik, performans, temiz kod standartları ve mimari tutarlılık açısından denetler ve aksiyon raporu sunar.
---

# Kod Kalitesi ve Güvenlik Denetim Becerisi

Bu beceri, bir modül, dosya veya tüm proje üzerinde kod incelemesi (code review) yapılması istendiğinde devreye girer.

## Denetim Aşamaları

1. **Statik Kod İncelemesi**:
   - Tip güvenliği eksikleri
   - Hatalı null/undefined kontrolleri
   - Gereksiz karmaşıklık ve uzun fonksiyonlar

2. **Güvenlik Analizi**:
   - Hardcoded sırlar, anahtarlar, tokenlar
   - SQL Injection, XSS veya güvenli olmayan eval/exec kullanımları
   - Dışarıdan gelen verilerin yetersiz doğrulanması (input validation)

3. **Performans ve Kaynak Yönetimi**:
   - Bellek sızıntısı (memory leak) riskleri
   - Kapatılmamış bağlantılar veya stream'ler
   - Verimsiz döngüler ve asenkron operasyon blokajları

4. **Raporlama**:
   - Bulunan sorunları önem derecesine göre (Kritik, Yüksek, Orta, Düşük) sınıflandırın.
   - Her sorun için somut bir düzeltme önerisi ve örnek kod sunun.
