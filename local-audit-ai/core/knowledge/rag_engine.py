"""
Local Audit AI - Dinamik Yerel Mevzuat ve Kriter Bilgi Tabanı Motoru (Offline RAG)
BDDK, MASAK, SPK, KVKK, Rekabet Kurumu, TTK, TCK, SOX, COSO, ISO 27001 ve IIA mevzuatlarını
yerel bellekte indeksler ve dinamik semantik benzerlik (Cosine/TF-IDF) ile en alakalı kriter maddelerini sunar.
"""
import os
import json
import re
import math
from typing import List, Dict, Any, Optional

class AuditKnowledgeBase:
    """
    Yerel Dinamik Mevzuat ve Kriter Arama Motoru (Offline RAG Engine).
    """

    def __init__(self, db_path: str = "config/regulations_knowledge_base.json"):
        self.db_path = db_path
        self.regulations: List[Dict[str, Any]] = self._load_database()

    def _load_database(self) -> List[Dict[str, Any]]:
        """Mevzuat JSON veritabanını yükler."""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Mevzuat tabanı yüklenemedi: {e}")
        return []

    def _tokenize(self, text: str) -> List[str]:
        """Metni küçük harfe çevirir ve Türkçe karakterleri destekleyerek kelimelere böler."""
        clean = text.lower()
        # Türkçe karakter dönüşümü
        clean = clean.replace("i̇", "i").replace("ı", "i").replace("ğ", "g").replace("ü", "u").replace("ş", "s").replace("ö", "o").replace("ç", "c")
        tokens = re.findall(r"\b[a-z0-9]{3,}\b", clean)
        return tokens

    def _compute_tf_vector(self, tokens: List[str]) -> Dict[str, float]:
        """Terim sıklığı (Term Frequency) vektörü hesaplar."""
        tf = {}
        total = len(tokens) if tokens else 1
        for t in tokens:
            tf[t] = tf.get(t, 0) + 1 / total
        return tf

    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """İki seyrek kelime frekans vektörü arasındaki Cosine Benzerliğini hesaplar."""
        intersection = set(vec1.keys()) & set(vec2.keys())
        dot_product = sum(vec1[k] * vec2[k] for k in intersection)
        
        norm1 = math.sqrt(sum(v**2 for v in vec1.values()))
        norm2 = math.sqrt(sum(v**2 for v in vec2.values()))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)

    def search_relevant_criteria(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Sorgu metnini (vaka açıklaması, saha notları veya bulgular) mevzuat tabanında
        dinamik olarak arar ve en yüksek alaka skoruna sahip ilk top_k maddeyi döndürür.
        """
        if not self.regulations or not query.strip():
            return []

        query_tokens = self._tokenize(query)
        if not query_tokens:
            return self.regulations[:top_k]

        query_vec = self._compute_tf_vector(query_tokens)
        scored_results = []

        for reg in self.regulations:
            # Belge metni (başlık + içerik + anahtar kelimeler)
            doc_text = f"{reg.get('title', '')} {reg.get('category', '')} {' '.join(reg.get('keywords', []))} {reg.get('content', '')}"
            doc_tokens = self._tokenize(doc_text)
            doc_vec = self._compute_tf_vector(doc_tokens)

            # Cosine Benzerlik Skoru
            base_sim = self._cosine_similarity(query_vec, doc_vec)

            # Anahtar kelime tam eşleşme bonusu
            keyword_bonus = 0.0
            for kw in reg.get("keywords", []):
                if kw.lower() in query.lower():
                    keyword_bonus += 0.15

            total_score = min(base_sim * 2.5 + keyword_bonus, 1.0)

            if total_score > 0.05:
                scored_results.append({
                    "id": reg["id"],
                    "authority": reg["authority"],
                    "title": reg["title"],
                    "category": reg["category"],
                    "content": reg["content"],
                    "match_score_pct": round(total_score * 100, 1),
                    "raw_score": total_score
                })

        # Skora göre büyükten küçüğe sırala
        scored_results.sort(key=lambda x: x["raw_score"], reverse=True)
        return scored_results[:top_k]
