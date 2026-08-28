---
name: mcp-server-builder
description: Model Context Protocol (MCP) standartlarına uygun olarak yeni tool, resource ve prompt sağlayan TypeScript veya Python tabanlı MCP sunucuları geliştirir.
---

# MCP Server Builder: Entegrasyon ve Araç Geliştirme

Bu beceri, harici API'ler, veritabanları veya yerel servisler için standartlara tam uyumlu Model Context Protocol (MCP) sunucuları üretir.

## MCP Geliştirme Standartları

### 1. Mimari Seçimi
- **TypeScript (Önerilen):** `@modelcontextprotocol/sdk` ve Zod kullanarak tip güvenli ve performanslı araçlar.
- **Python:** `mcp` kütüphanesi ve Pydantic kullanarak veri odaklı entegrasyonlar.
- **İletişim Katmanı:** Stdio (yerel CLI/IDE araçları için) veya SSE (Server-Sent Events - uzak servisler için).

### 2. Araç (Tool) Tasarımı
- **İsimlendirme:** Açıklayıcı ve snake_case formatında (örn: `fetch_user_profile`, `query_order_status`).
- **Açıklama (Description):** Ajanın bu aracı ne zaman ve hangi amaçla çağıracağını açıkça belirten detaylı dokümantasyon.
- **Girdi Şeması (Input Schema):** Zod/Pydantic ile kesin tip tanımları, default değerler ve zorunlu alanlar.

### 3. Hata Yönetimi
- Sunucu çökmelerini önlemek için her tool handler'ını `try-catch` bloğuna al.
- Hata durumunda ajana anlaşılır bir `isError: true` yanıtı ve düzeltici ipucu içeren `content` dön.

### 4. Kaynaklar ve Şablonlar (Resources & Prompts)
- Sık okunan veriler için `resources` (örn: `file://` veya `db://` URI şemaları).
- Yeniden kullanılabilir akışlar için `prompts` tanımları.
