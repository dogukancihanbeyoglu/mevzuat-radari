"""
Local Audit AI - Dinamik Model Havuzu ve Otonom Tier Yapılandırma Motoru (Model Registry & Auto-Tiering)
Yerelde kurulu tüm modelleri (10, 20, 50+) otomatik keşfeder, uzmanlıklarına (kodlama, muhakeme, hafif veri çekme)
göre otonom puanlama yapar ve Tier 1/2/3 eşleştirmelerini sıfır kullanıcı müdahalesiyle optimize eder.
"""
import os
import re
import yaml
import requests
from typing import Dict, Any, List, Optional

class ModelRegistry:
    """
    Yerel Model Havuzu, Keşif ve Otonom Tier Eşleştirme Motoru.
    """

    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path

    def load_config(self) -> Dict[str, Any]:
        """Config dosyasını okur."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Config okuma hatası: {e}")
        return {}

    def get_tier_models(self) -> Dict[str, Dict[str, Any]]:
        """Tier 1, Tier 2 ve Tier 3'e atanmış aktif modelleri döner."""
        cfg = self.load_config()
        return cfg.get("model_tiers", {
            "tier_1_light": {"name": "qwen2.5-coder:7b", "temperature": 0.1},
            "tier_2_standard": {"name": "deepseek-r1:8b", "temperature": 0.2},
            "tier_3_deep_reasoning": {"name": "qwen2.5-coder:14b", "temperature": 0.2}
        })

    def update_tier_model(
        self,
        tier_key: str,
        model_name: str,
        temperature: Optional[float] = None,
        fallback_model: Optional[str] = None
    ) -> bool:
        """Belirli bir Tier'ın modelini günceller ve config'e kaydeder."""
        cfg = self.load_config()
        if "model_tiers" not in cfg:
            cfg["model_tiers"] = {}
        if tier_key not in cfg["model_tiers"]:
            cfg["model_tiers"][tier_key] = {}

        cfg["model_tiers"][tier_key]["name"] = model_name
        if temperature is not None:
            cfg["model_tiers"][tier_key]["temperature"] = float(temperature)
        if fallback_model:
            cfg["model_tiers"][tier_key]["fallback"] = fallback_model

        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception as e:
            print(f"Config yazma hatası: {e}")
            return False

    def discover_installed_models(self, base_url: str = "http://127.0.0.1:11434") -> List[str]:
        """Yerel Ollama sunucusundaki (/api/tags) kurulu modelleri otomatik keşfeder."""
        try:
            resp = requests.get(f"{base_url.rstrip('/')}/api/tags", timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                models = [m.get("name") for m in data.get("models", []) if m.get("name")]
                if models:
                    return sorted(models)
        except Exception:
            pass

        return [
            "qwen2.5-coder:7b",
            "deepseek-r1:8b",
            "qwen2.5-coder:14b",
            "deepseek-r1:14b",
            "qwen2.5:32b",
            "llama3.3:70b"
        ]

    def classify_and_score_model(self, model_name: str) -> Dict[str, float]:
        """
        Herhangi bir model adını analiz ederek Tier 1 (Hafif), Tier 2 (Muhakeme)
        ve Tier 3 (Kod/Analitik) uygunluk skorlarını (0-10 puan) hesaplar.
        """
        name_lower = model_name.lower()
        scores = {
            "tier_1_score": 5.0,
            "tier_2_score": 5.0,
            "tier_3_score": 5.0
        }

        # 1. Boyut Tespiti (Parametre)
        is_small = bool(re.search(r'(1\.5b|3b|7b|8b)', name_lower))
        is_medium = bool(re.search(r'(14b|20b|27b|32b)', name_lower))
        is_large = bool(re.search(r'(70b|72b|671b)', name_lower))

        if is_small:
            scores["tier_1_score"] += 3.5
            scores["tier_2_score"] += 2.0
            scores["tier_3_score"] -= 1.0
        elif is_medium:
            scores["tier_1_score"] -= 1.0
            scores["tier_2_score"] += 3.5
            scores["tier_3_score"] += 3.5
        elif is_large:
            scores["tier_1_score"] -= 3.0
            scores["tier_2_score"] += 4.5
            scores["tier_3_score"] += 4.5

        # 2. Uzmanlık / Yetenek Tespiti
        # A. Kodlama & Analitik
        if any(k in name_lower for k in ['coder', 'code', 'python', 'sql', 'starcoder', 'wizardcoder']):
            scores["tier_3_score"] += 4.0
            scores["tier_1_score"] += 1.5

        # B. Muhakeme & Düşünme (Reasoning / Thinking)
        if any(k in name_lower for k in ['r1', 'reasoning', 'think', 'deepseek-r', 'qwq']):
            scores["tier_2_score"] += 4.5
            scores["tier_3_score"] += 2.0

        # C. Hafif / Hızlı
        if any(k in name_lower for k in ['mini', 'tiny', 'light', 'flash', 'qwen2.5:7b', 'mistral:7b']):
            scores["tier_1_score"] += 2.5

        return scores

    def auto_configure_best_tiers(self, base_url: str = "http://127.0.0.1:11434") -> Dict[str, Any]:
        """
        Yereldeki tüm modelleri tarar, otonom olarak en ideal Tier 1, Tier 2 ve Tier 3
        modellerini seçer ve config'e uygular.
        """
        installed = self.discover_installed_models(base_url)
        if not installed:
            return {"success": False, "message": "Hiçbir model bulunamadı."}

        scored_models = []
        for m in installed:
            sc = self.classify_and_score_model(m)
            scored_models.append({
                "model_name": m,
                "t1": sc["tier_1_score"],
                "t2": sc["tier_2_score"],
                "t3": sc["tier_3_score"]
            })

        # 1. Tier 3 İçin En İyi Kod/Analitik Modelini Seç (En yüksek T3)
        best_t3 = max(scored_models, key=lambda x: x["t3"])["model_name"]

        # 2. Tier 2 İçin En İyi Muhakeme Modelini Seç (T3 ile aynı olabilir veya en yüksek T2)
        best_t2 = max(scored_models, key=lambda x: x["t2"])["model_name"]

        # 3. Tier 1 İçin En Hızlı/Hafif Modeli Seç (En yüksek T1)
        best_t1 = max(scored_models, key=lambda x: x["t1"])["model_name"]

        # Config'e kaydet
        self.update_tier_model("tier_1_light", best_t1, temperature=0.1)
        self.update_tier_model("tier_2_standard", best_t2, temperature=0.2)
        self.update_tier_model("tier_3_deep_reasoning", best_t3, temperature=0.2)

        return {
            "success": True,
            "selected_tiers": {
                "tier_1_light": best_t1,
                "tier_2_standard": best_t2,
                "tier_3_deep_reasoning": best_t3
            },
            "scanned_model_count": len(installed),
            "rationale": f"{len(installed)} yerel model analiz edildi. Tier 1 (Hızlı): {best_t1}, Tier 2 (Muhakeme): {best_t2}, Tier 3 (Analitik/Kod): {best_t3} olarak otonom eşleştirildi."
        }
