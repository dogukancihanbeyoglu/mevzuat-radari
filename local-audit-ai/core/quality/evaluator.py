"""
Local Audit AI - Denetim Kalite Güvence ve Olgunluk Değerlendirici (Audit QA/QC Evaluator)
Model çıktısının IIA Küresel Standartlarına (5C eksiksizliği, sayısal kanıt oranı,
mevzuat atfı ve profesyonel şüphecilik) uygunluğunu 100 üzerinden puanlar ve kalite raporu üretir.
"""
import re
from typing import Dict, Any, List

class AuditQualityEvaluator:
    """
    IIA Standartlarında Denetim Çıktısı Kalite Güvence ve Olgunluk Değerlendiricisi.
    """

    def evaluate_output_quality(self, task_module: str, output_text: str) -> Dict[str, Any]:
        """
        Üretilen denetim çalışma kağıdını çok boyutlu olarak analiz eder ve puanlar.
        """
        score = 0
        checks: Dict[str, bool] = {}
        recommendations: List[str] = []

        # 1. 5C Bileşenleri Kontrolü (40 Puan)
        has_condition = bool(re.search(r"(?:condition|mevcut durum|tespit)", output_text, re.IGNORECASE))
        has_criteria = bool(re.search(r"(?:criteria|kriter|olması gereken|mevzuat|madde|standart)", output_text, re.IGNORECASE))
        has_cause = bool(re.search(r"(?:cause|kök neden|neden)", output_text, re.IGNORECASE))
        has_effect = bool(re.search(r"(?:effect|etki|risk|maruziyet|zarar)", output_text, re.IGNORECASE))
        has_recommendation = bool(re.search(r"(?:recommendation|öneri|aksiyon|iyileştirme)", output_text, re.IGNORECASE))

        five_c_count = sum([has_condition, has_criteria, has_cause, has_effect, has_recommendation])
        score += five_c_count * 8 # Her biri 8 puan (Toplam 40)

        checks["5C_Condition"] = has_condition
        checks["5C_Criteria"] = has_criteria
        checks["5C_Cause"] = has_cause
        checks["5C_Effect"] = has_effect
        checks["5C_Recommendation"] = has_recommendation

        if five_c_count < 5:
            recommendations.append(f"5C Bulgusu tam değildir ({five_c_count}/5 bileşen bulundu).")

        # 2. Sayısal Veri & Parasal Tutar Varlığı (20 Puan)
        has_monetary_figures = bool(re.search(r"\b\d+(?:[.,]\d+)*(?:\s*(?:TL|USD|EUR|Milyon|Bin|\$|€))\b", output_text, re.IGNORECASE))
        if has_monetary_figures:
            score += 20
            checks["Monetary_Evidence"] = True
        else:
            checks["Monetary_Evidence"] = False
            recommendations.append("Çıktıda somut parasal tutar veya sayısal anomali büyüklüğü tespit edilemedi.")

        # 3. Yasal Mevzuat ve Standart Atıfları (20 Puan)
        has_regulation_citation = bool(re.search(r"(?:BDDK|MASAK|SOX|TTK|ISO|SPK|IIA|Kanun|Tebliğ|Yönetmelik)", output_text))
        if has_regulation_citation:
            score += 20
            checks["Regulation_Citation"] = True
        else:
            checks["Regulation_Citation"] = False
            recommendations.append("Mevzuat veya uluslararası standart atfı (BDDK, MASAK, SOX, IIA) bulunamadı.")

        # 4. Yapılandırılmış Tablo / Format Zenginliği (10 Puan)
        has_table = bool(re.search(r"\|.*?\|.*?\|", output_text))
        if has_table or task_module in ["data_analytics", "finding_5c"]:
            score += 10
            checks["Structured_Layout"] = True
        else:
            checks["Structured_Layout"] = False

        # 5. Profesyonel Şüphecilik ve Dil Olgunluğu (10 Puan)
        has_skepticism_terms = bool(re.search(r"(?:usulsüzlük|zafiyet|çelişki|kontrol eksikliği|ihlal|suiistimal|risk)", output_text, re.IGNORECASE))
        if has_skepticism_terms:
            score += 10
            checks["Professional_Skepticism"] = True
        else:
            checks["Professional_Skepticism"] = False

        # Derecelendirme
        if score >= 90:
            rating = "🏆 Mükemmel (IIA Global Tier-1 Standartlarında)"
            badge_color = "green"
        elif score >= 75:
            rating = "🟢 Güçlü ve Yeterli (Professional Standard)"
            badge_color = "blue"
        elif score >= 60:
            rating = "🟡 Gelişime Açık (Moderate Quality)"
            badge_color = "orange"
        else:
            rating = "🔴 Yetersiz (Insufficient Evidence & Depth)"
            badge_color = "red"

        return {
            "score": score,
            "rating": rating,
            "badge_color": badge_color,
            "checks": checks,
            "recommendations": recommendations,
            "is_high_quality": score >= 80
        }
