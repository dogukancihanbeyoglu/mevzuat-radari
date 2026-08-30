"""
Local Audit AI - IIA Meta-Prompt Engine
IIA (The Institute of Internal Auditors) 8-Bileşenli Standart Prompt Üreticisi (%100 Türkçe)
"""
from typing import Dict, Any, Optional, Tuple
import yaml
import os

class IIAAuditPrompt:
    def __init__(
        self,
        role: str,
        context: str,
        task: str,
        format_spec: str,
        constraints: str,
        reasoning_step: str,
        interactive_prompt: str,
        few_shot_examples: Optional[str] = None
    ):
        self.role = role
        self.context = context
        self.task = task
        self.format_spec = format_spec
        self.constraints = constraints
        self.reasoning_step = reasoning_step
        self.interactive_prompt = interactive_prompt
        self.few_shot_examples = few_shot_examples

    def build_prompt(self, input_data: str) -> str:
        """8 bileşeni IIA standardında birleştirilmiş Türkçe meta-prompta dönüştürür."""
        prompt_parts = [
            f"# ROL VE UZMANLIK\n{self.role}\n",
            f"# KURUMSAL BAĞLAM VE ÇEVRE\n{self.context}\n",
            f"# DENETİM GÖREVİ VE HEDEF\n{self.task}\n",
            f"# DÜŞÜNME VE AKIL YÜRÜTME ADIMI (Chain-of-Thought)\n{self.reasoning_step}\n",
            f"# ÇIKTI FORMATI VE ŞABLON GEREKSİNİMLERİ\n{self.format_spec}\n",
            f"# KISITLAMALAR VE DENETİM KURALLARI\n{self.constraints}\n",
            "# KESİN DİL KURALI\n"
            "ÇIKTININ TAMAMINI, BAŞLIKLARI, TABLOLARI VE AÇIKLAMALARI KESİNLİKLE VE SADECE TÜRKÇE (TURKISH) DİLİNDE YAZ. "
            "KULLANICI AKSİNİ TALEP ETMEDİKÇE ASLA İNGİLİZCE CEVAP VERME.\n"
        ]

        if self.few_shot_examples:
            prompt_parts.append(f"# REFERANS ÖRNEKLER\n{self.few_shot_examples}\n")

        prompt_parts.append(f"# ETKİLEŞİMLİ AÇIKLAMA KURALI\n{self.interactive_prompt}\n")
        prompt_parts.append(f"# DENETİM KANITI VE SAHA GİRDİLERİ\n```\n{input_data}\n```\n")
        prompt_parts.append(
            "# HEDEF VE SONUÇ\n"
            "Yukarıdaki format ve kurallara harfiyen uyarak, profesyonel Türkçe denetim çalışma kağıdını oluştur."
        )

        return "\n".join(prompt_parts)

class PromptFactory:
    """iia_templates.yaml dosyasından şablonları yükleyip dinamik IIAAuditPrompt nesneleri üretir."""

    def __init__(self, templates_path: str = "config/iia_templates.yaml"):
        self.templates = self._load_templates(templates_path)

    def _load_templates(self, path: str) -> Dict[str, Any]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    def create_prompt(
        self,
        module_name: str,
        input_data: str,
        custom_context: str = "IIA Küresel Standartları Kapsamında Kurumsal İç Denetim Çalışması."
    ) -> Tuple[IIAAuditPrompt, str]:
        template = self.templates.get(module_name)
        if not template:
            raise ValueError(f"Bilinmeyen denetim modülü: {module_name}")

        audit_prompt = IIAAuditPrompt(
            role=template.get("role", "Sen deneyimli bir iç denetçisin."),
            context=custom_context,
            task=template.get("task", ""),
            format_spec=template.get("format", ""),
            constraints=template.get("constraints", ""),
            reasoning_step=template.get("reasoning_step", "Adım adım düşünerek analiz yap."),
            interactive_prompt=template.get("interactive_prompt", "Detaylar eksikse denetçiye soru sor."),
            few_shot_examples=template.get("few_shot_examples", None)
        )

        full_prompt_string = audit_prompt.build_prompt(input_data)
        return audit_prompt, full_prompt_string
