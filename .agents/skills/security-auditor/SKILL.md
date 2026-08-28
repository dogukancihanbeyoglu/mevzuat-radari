---
name: security-auditor
description: OWASP Top 10, gizli anahtar/token sızıntıları, güvenli olmayan veri transferi ve yetkilendirme zaafiyetlerini denetleyen siber güvenlik uzmanı becerisi.
---

# Güvenlik ve Zaafiyet Denetçisi (Security Auditor)

Bu beceri, kod tabanını üretim seviyesinde siber güvenlik standartları açısından proaktif olarak denetler.

## Denetim Kontrol Listesi

### 1. Kimlik Doğrulama ve Yetkilendirme (Auth & Access Control)
- Endpoint'lerde eksik yetki kontrolü (Broken Object Level Authorization - BOLA / IDOR).
- Rol tabanlı erişim denetimlerinin (RBAC) frontend yerine backend seviyesinde doğrulanması.
- Session ve JWT token süreleri, güvenli saklama (HttpOnly, Secure cookies).

### 2. Girdi Doğrulama ve Sanitizasyon (Input Validation)
- SQL / NoSQL Injection: Parametrik sorgular veya ORM kullanımı zorunluluğu.
- Cross-Site Scripting (XSS): Kullanıcı içeriklerinin kaçış (escape) kontrolleri.
- Command Injection: Güvenli olmayan `eval()`, `exec()`, `spawn()` kullanımlarının engellenmesi.

### 3. Gizli Bilgi Yönetimi (Secrets & PII)
- Kod içine hardcode edilmiş API anahtarları, şifreler, özel anahtarlar.
- Log dosyalarına hassas kullanıcı verisi (şifre, kredi kartı, TC no vb.) yazılmaması.
- `.env` ve ortam değişkenlerinin doğru yapılandırılması, `.gitignore` kontrolü.

### 4. Güvenli İletişim ve Konfigürasyon
- CORS politikalarının aşırı esnek (`*`) olmaması.
- Güvenlik başlıkları (Helmet, CSP, HSTS, X-Frame-Options).
- Bağımlılıklardaki bilinen güvenlik açıkları (CVE taraması).
