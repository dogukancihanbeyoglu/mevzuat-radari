"""
Local Audit AI - Security & Privacy Module
Yerel PII (Kişisel Veri) Maskeleyici ve Kriptografik Denetim İzi (Audit Trail)
"""
import re
import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, Tuple, Any

class PIIMasker:
    """Yerel Regex Tabanlı Hassas Veri Maskeleme Motoru"""
    
    PATTERNS = {
        "IBAN_TR": r"\bTR[0-9]{2}\s?[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}\s?[0-9]{2}\b",
        "CREDIT_CARD": r"\b(?:[0-9]{4}[- ]?){3}[0-9]{4}\b",
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "PHONE_TR": r"\b(?:\+90|0)?\s*[1-9][0-9]{2}\s*[0-9]{3}\s*[0-9]{2}\s*[0-9]{2}\b",
        "TCKN": r"(?<![0-9])[1-9][0-9]{10}(?![0-9])"
    }

    def __init__(self):
        self.mapping: Dict[str, str] = {}
        self.reverse_mapping: Dict[str, str] = {}
        self.counters: Dict[str, int] = {k: 1 for k in self.PATTERNS.keys()}

    def mask(self, text: str) -> str:
        """Hassas verileri maskeler ve geri eşleme tablosunu tutar."""
        masked_text = text
        for p_name, pattern in self.PATTERNS.items():
            matches = set(re.findall(pattern, masked_text))
            for match in matches:
                if match not in self.mapping:
                    token = f"[{p_name}_{self.counters[p_name]}]"
                    self.mapping[match] = token
                    self.reverse_mapping[token] = match
                    self.counters[p_name] += 1
                masked_text = masked_text.replace(match, self.mapping[match])
        return masked_text

    def unmask(self, text: str) -> str:
        """Maskeli tokenları orijinal değerlerine geri dönüştürür."""
        unmasked = text
        for token, original in self.reverse_mapping.items():
            unmasked = unmasked.replace(token, original)
        return unmasked

class AuditTrailLogger:
    """Kriptografik Denetim İzi ve Çalışma Kağıdı İmzası Yöneticisi"""

    @staticmethod
    def calculate_sha256(content: str) -> str:
        """Metin içeriğinin SHA-256 özetini üretir."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @staticmethod
    def calculate_file_sha256(file_path: str) -> str:
        """Dosyanın SHA-256 özetini üretir."""
        if not os.path.exists(file_path):
            return "NO_FILE"
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    @classmethod
    def create_record(
        cls,
        task_name: str,
        input_data: str,
        generated_prompt: str,
        model_name: str,
        tier: str,
        output_content: str,
        source_file: str = None
    ) -> Dict[str, Any]:
        """IIA standartlarına uygun tam denetim izi kaydı oluşturur."""
        timestamp = datetime.now(timezone.utc).isoformat()
        input_hash = cls.calculate_sha256(input_data)
        output_hash = cls.calculate_sha256(output_content)
        file_hash = cls.calculate_file_sha256(source_file) if source_file else "N/A"
        
        record = {
            "audit_trail_id": f"AT-{int(datetime.now().timestamp())}",
            "timestamp_utc": timestamp,
            "task_module": task_name,
            "source_file": source_file or "Direct_Input",
            "source_file_sha256": file_hash,
            "input_data_sha256": input_hash,
            "complexity_tier": tier,
            "dispatched_model": model_name,
            "raw_prompt_used": generated_prompt,
            "output_sha256": output_hash,
            "governance_compliance": {
                "framework": "IIA AI Auditing Framework (Aug 2026)",
                "professional_skepticism_required": True,
                "is_ai_draft": True,
                "air_gapped_local_execution": True
            }
        }
        return record

    @classmethod
    def save_record(cls, record: Dict[str, Any], storage_dir: str = "storage/audit_trails") -> str:
        """Denetim izi kaydını JSON olarak yerel diske kaydeder."""
        os.makedirs(storage_dir, exist_ok=True)
        file_path = os.path.join(storage_dir, f"{record['audit_trail_id']}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
        return file_path
