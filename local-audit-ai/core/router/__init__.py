"""
Local Audit AI - Complexity Router Agent
Görevin zorluk seviyesine göre akıllı model seçimi ve yönlendirme
"""
from typing import Dict, Any, Tuple
import yaml
import os

class ComplexityTier:
    TIER_1_LIGHT = "tier_1_light"
    TIER_2_STANDARD = "tier_2_standard"
    TIER_3_DEEP_REASONING = "tier_3_deep_reasoning"

class ComplexityAnalyzerAgent:
    """Görevin karmaşıklığını, bilişsel gereksinimini ve veri boyutunu analiz eder."""

    TASK_TIER_MAP = {
        "data_extraction": ComplexityTier.TIER_1_LIGHT,
        "walkthrough_questions": ComplexityTier.TIER_1_LIGHT,
        "quick_summary": ComplexityTier.TIER_1_LIGHT,
        
        "rcm_generation": ComplexityTier.TIER_2_STANDARD,
        "test_procedure": ComplexityTier.TIER_2_STANDARD,
        "finding_5c": ComplexityTier.TIER_2_STANDARD,
        "control_analysis": ComplexityTier.TIER_2_STANDARD,
        
        "executive_summary": ComplexityTier.TIER_2_STANDARD,
        "data_analytics": ComplexityTier.TIER_3_DEEP_REASONING,
        "audit_universe": ComplexityTier.TIER_3_DEEP_REASONING,
        "resource_competency_mapping": ComplexityTier.TIER_3_DEEP_REASONING
    }

    @classmethod
    def evaluate(cls, task_name: str, input_text: str, custom_intent: str = None) -> Dict[str, Any]:
        """
        Karmaşıklık puanı hesaplar (1-5 arası) ve uygun Tier'ı belirler.
        """
        base_tier = cls.TASK_TIER_MAP.get(task_name, ComplexityTier.TIER_2_STANDARD)
        token_estimate = len(input_text.split())
        
        complexity_score = 2
        rationale = "Standart denetim metodolojisi ve şablon eşleme."

        if base_tier == ComplexityTier.TIER_1_LIGHT:
            complexity_score = 1
            rationale = "Düşük bilişsel yük, hızlı anahtar bilgi ayıklama ve liste oluşturma."
        elif base_tier == ComplexityTier.TIER_3_DEEP_REASONING:
            complexity_score = 5
            rationale = "Çok adımlı analitik Python kodu üretimi, çoklu istisna lojiği ve derin akıl yürütme."
        else:
            # Standart görev ancak çok büyük doküman ise Tier 3'e yükselt
            if token_estimate > 3000:
                base_tier = ComplexityTier.TIER_3_DEEP_REASONING
                complexity_score = 4
                rationale = "Yüksek token hacmi ve çok paydaşlı süreç karmaşıklığı nedeniyle derin modele yükseltildi."

        return {
            "tier": base_tier,
            "complexity_score": complexity_score,
            "estimated_tokens": token_estimate,
            "rationale": rationale
        }

from core.router.model_registry import ModelRegistry

class ModelDispatcher:
    """Belirlenen Tier'a göre dinamik ModelRegistry'den güncel model ayarlarını yükler."""

    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.registry = ModelRegistry(config_path)

    def dispatch(self, evaluation: Dict[str, Any]) -> Dict[str, Any]:
        tier_key = evaluation["tier"]
        tier_models = self.registry.get_tier_models()
        tier_config = tier_models.get(tier_key, {})
        
        return {
            "tier": tier_key,
            "model_name": tier_config.get("name", "qwen2.5:7b"),
            "fallback_model": tier_config.get("fallback", "llama3.1:8b"),
            "temperature": tier_config.get("temperature", 0.2),
            "max_tokens": tier_config.get("max_tokens", 4096),
            "rationale": evaluation["rationale"]
        }
