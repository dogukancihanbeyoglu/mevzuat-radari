"""
Local Audit AI - Zeki Kanıt ve Anomali Ayıklayıcı (Smart Evidence Extractor)
Devasa boyutlu Excel tablolarından ve onlarca sayfalık prosedürlerden kritik riskli satırları,
limit aşımlarını, MASAK/BDDK ihlallerini ve istisnaları ayıklayıp model için öncelikli kanıt özeti hazırlar.
"""
import re
from typing import Dict, Any, List, Optional
import pandas as pd

class SmartEvidenceExtractor:
    """
    Büyük veri setleri ve dokümanlar için hiyerarşik kanıt ayıklama motoru.
    Modellerin devasa metinlerde kaybolmasını önleyerek en kritik anomalilere odaklanmasını sağlar.
    """

    CRITICAL_KEYWORDS = [
        "yetkisiz", "unauthorized", "override", "bypass", "zarar", "loss", "kayıp",
        "masak", "bddk", "şüpheli", "suspicious", "sahte", "fraud", "hırsızlık",
        "kara para", "kara_para", "offshore", "npl", "teminatsız", "açık", "ceza",
        "tolerans aşımı", "fire", "discrepancy", "sod ihlali", "mükerrer", "duplicate"
    ]

    def extract_critical_evidence(self, raw_text: str, max_evidence_items: int = 15) -> Dict[str, Any]:
        """
        Ham metin veya tablo çıktısından en kritik risk göstergelerini ayıklar.
        """
        lines = raw_text.splitlines()
        found_evidences: List[Dict[str, str]] = []
        total_amount_signals: List[float] = []

        for line in lines:
            line_lower = line.lower()
            
            # Parasal tutarları tespit et (örn: 14.800.000 USD, 45.000.000 TL)
            amounts = re.findall(r"(\d+(?:[.,]\d+)*(?:\.\d+)?)\s*(?:milyon|m|bin|k)?\s*(?:tl|usd|eur|\$|€)", line_lower)
            
            # Kritik anahtar kelime eşleşmesi
            matched_keywords = [kw for kw in self.CRITICAL_KEYWORDS if kw in line_lower]
            
            if matched_keywords:
                # Satırı temizle ve formatla
                clean_line = line.strip().strip("|").strip()
                if len(clean_line) > 15:
                    found_evidences.append({
                        "category": matched_keywords[0].upper(),
                        "evidence_text": clean_line[:300],
                        "keywords": matched_keywords
                    })

        # Benzersizleştir ve sınırla
        unique_evidences = []
        seen = set()
        for ev in found_evidences:
            if ev["evidence_text"] not in seen:
                seen.add(ev["evidence_text"])
                unique_evidences.append(ev)
            if len(unique_evidences) >= max_evidence_items:
                break

        # Öncelikli Kanıt Özeti (Executive Brief) Oluştur
        if unique_evidences:
            brief_lines = ["\n### ⚡ AKILLI AYIKLANAN ÖNCELİKLİ DENETİM KANITLARI (KEY EVIDENCE BRIEF):"]
            for idx, ev in enumerate(unique_evidences, 1):
                brief_lines.append(f"{idx}. [{ev['category']}] {ev['evidence_text']}")
            brief_text = "\n".join(brief_lines)
        else:
            brief_text = ""

        return {
            "evidence_count": len(unique_evidences),
            "evidences": unique_evidences,
            "brief_text": brief_text
        }
