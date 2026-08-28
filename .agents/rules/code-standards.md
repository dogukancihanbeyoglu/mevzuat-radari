---
trigger: always_on
---

# Proje Kod Standartları ve Yönergeleri

- **Dil & İletişim**: Kullanıcı aksini talep etmedikçe Türkçe yanıt verin ve kod içi dokümantasyonu anlaşılır tutun.
- **Git & Değişiklik Yönetimi**: Kod değişiklikleri yaparken gereksiz biçimlendirme farkları oluşturmayın; sadece amaca odaklı diff'ler üretin.
- **Güvenlik**: Hassas verileri (API key, token, gizli şifreler) asla kaynak kod içerisine hardcode etmeyin; `.env` ve ortam değişkenlerini kullanın.
