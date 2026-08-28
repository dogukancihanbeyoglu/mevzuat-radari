---
name: anti-ui-slop
description: Basmakalıp, jenerik ve kalitesiz yapay zeka arayüzlerini engelleyerek; WCAG erişilebilirliği, tasarım sistemi tokenları ve gerçek kullanıcı deneyimi standartlarına uygun modern UI üretir.
---

# Anti-UI Slop: Profesyonel Arayüz Standartları

Bu beceri, yapay zekanın ürettiği tekrarlayan, ruhsuz ve jenerik bileşenler yerine gerçek bir ürün kalitesinde arayüzler tasarlamayı amaçlar.

## Temel Tasarım Kuralları

### 1. Tipografi ve Hiyerarşi
- Rastgele `px` değerleri yerine projenin font ölçeğini (Design Tokens) kullan.
- Başlıklar ve metinler arasında belirgin kontrast ve optik denge kur.
- Satır uzunluğunu (line-length) okunabilirlik için 60-75 karakter arasında sınırla.

### 2. Renk ve Kontrast
- Asla rastgele hex kodları gömme; semantik renk sınıflarını (örn: `bg-primary`, `text-muted-foreground`) tercih et.
- WCAG 2.1 AA kontrast gereksinimlerini (en az 4.5:1) sağla.
- Hem Aydınlık (Light) hem de Karanlık (Dark) tema desteğini garanti et.

### 3. Etkileşim ve Durumlar (Interactive States)
Her tıklanabilir ve veri içeren bileşen şu durumları mutlaka içermelidir:
- **Default (Varsayılan):** Temiz, anlaşılır görünüm.
- **Hover & Focus-Visible:** Klavye kullanıcıları için belirgin odak halkası (`ring-2 ring-offset-2`).
- **Active & Pressed:** Anlık geri bildirim.
- **Disabled & Loading:** Tıklama engeli ve skeleton/spinner durumu.
- **Empty & Error State:** Veri yokken veya hata anında kullanıcıyı yönlendiren mesajlar.

### 4. Boşluk (Spacing) ve Ritim
- 4px veya 8px tabanlı ızgara sistemine (spacing grid) sadık kal.
- Bileşen içi (padding) ve bileşenler arası (margin/gap) oranlarını tutarlı tut.
- Ekran boyutlarına göre (Mobile / Tablet / Desktop) akıcı responsive adaptasyon sağla.
