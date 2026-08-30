"""
Local Audit AI - Audit Modules Orchestrator
5 Temel IIA Denetim Modülünün Uçtan Uca Yürütücüsü (Next-Gen Audit OS)
"""
import os
import yaml
import time
from typing import Dict, Any, Optional, List, Union

from core.ingestion import parse_document, parse_multiple_documents
from core.ingestion.smart_extractor import SmartEvidenceExtractor
from core.quality.evaluator import AuditQualityEvaluator
from core.security import PIIMasker, AuditTrailLogger
from core.router import ComplexityAnalyzerAgent, ModelDispatcher
from core.prompt_engine import PromptFactory
from core.execution import LocalLLMClient
from core.execution.sandbox import LocalPythonSandbox
from core.export.workpaper_exporter import WorkpaperExporter
from core.knowledge.rag_engine import AuditKnowledgeBase

class AuditOrchestrator:
    """
    Yerel Yapay Zeka Denetim Orkestratörü (Next-Gen Audit OS).
    Tüm denetim yaşam döngüsünü, güvenlik katmanını, model yönlendiricisini,
    akıllı kanıt ayıklayıcısını, kalite güvence motorunu ve sandbox'ı koordine eder.
    """

    def _load_config(self, path: str) -> dict:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}

    def __init__(self, config_path: str = "config/config.yaml"):
        self.config = self._load_config(config_path)
        self.masker = PIIMasker()
        self.dispatcher = ModelDispatcher(config_path)
        self.prompt_factory = PromptFactory(self.config.get("system", {}).get("templates_path", "config/iia_templates.yaml"))
        self.llm_client = LocalLLMClient(
            base_url=self.config.get("system", {}).get("ollama_base_url", "http://127.0.0.1:11434"),
            timeout=self.config.get("system", {}).get("request_timeout", 180)
        )
        self.sandbox = LocalPythonSandbox(timeout_sec=60)
        self.exporter = WorkpaperExporter()
        self.knowledge_base = AuditKnowledgeBase()
        self.smart_extractor = SmartEvidenceExtractor()
        self.quality_evaluator = AuditQualityEvaluator()

    def run_audit_task(
        self,
        module_name: str,
        input_text: str = "",
        file_path: Optional[str] = None,
        file_paths: Optional[list] = None,
        custom_context: str = "Corporate Internal Audit Engagement under IIA Global Standards.",
        enable_masking: bool = True,
        model_override: Optional[str] = None,
        custom_temperature: Optional[float] = None
    ) -> Dict[str, Any]:
        # 1. Girdi verisini ve çoklu/tekil dosyaları topla
        raw_data = input_text
        all_files = []
        if file_path:
            all_files.append(file_path)
        if file_paths:
            all_files.extend(file_paths)

        if all_files:
            parsed_docs = parse_multiple_documents(all_files)
            raw_data = f"{raw_data}\n\n{parsed_docs}".strip()

        if not raw_data.strip():
            raise ValueError("Denetim görevi için hiçbir veri veya dosya sağlanmadı.")

        # 2. Akıllı Öncelikli Kanıt Ayıklama (Smart Evidence Extraction)
        evidence_data = self.smart_extractor.extract_critical_evidence(raw_data)
        if evidence_data.get("brief_text"):
            enriched_input = f"{raw_data}\n\n{evidence_data['brief_text']}".strip()
        else:
            enriched_input = raw_data

        # 3. Hassas Veri Maskeleme (PII Protection)
        if enable_masking:
            masked_input = self.masker.mask(enriched_input)
        else:
            masked_input = enriched_input

        # 4. Karmaşıklık Analizi & Model Yönlendirme (Router veya Manuel Override)
        evaluation = ComplexityAnalyzerAgent.evaluate(module_name, enriched_input)
        dispatched_model = self.dispatcher.dispatch(evaluation)

        if model_override and model_override != "auto":
            dispatched_model["model_name"] = model_override
            dispatched_model["is_override"] = True
            dispatched_model["rationale"] = f"Kullanıcı tarafından özel model atandı ({model_override})."
        else:
            dispatched_model["is_override"] = False

        if custom_temperature is not None:
            dispatched_model["temperature"] = float(custom_temperature)

        # 5. IIA 8-Bileşenli Prompt Üretimi
        audit_prompt_obj, full_prompt_string = self.prompt_factory.create_prompt(
            module_name=module_name,
            input_data=masked_input,
            custom_context=custom_context
        )

        # 6. Yerel Model Yürütmesi
        start_time = time.time()
        execution_result = self.llm_client.generate(
            model_name=dispatched_model["model_name"],
            prompt=full_prompt_string,
            temperature=dispatched_model.get("temperature", 0.2),
            max_tokens=dispatched_model.get("max_tokens", 4096),
            task_module=module_name
        )
        elapsed_time = round(time.time() - start_time, 2)

        # 7. Maskeleri Çöz (Unmask)
        if enable_masking:
            unmasked_output = self.masker.unmask(execution_result.get("content", ""))
        else:
            unmasked_output = execution_result.get("content", "")

        # 8. Denetim Kalite ve Olgunluk Değerlendirmesi (QA/QC Score)
        qa_result = self.quality_evaluator.evaluate_output_quality(module_name, unmasked_output)

        # 9. Denetim İzi (Audit Trail) Üret ve Kaydet
        source_label = ", ".join([os.path.basename(f) for f in all_files]) if all_files else None
        audit_record = AuditTrailLogger.create_record(
            task_name=module_name,
            input_data=raw_data,
            generated_prompt=full_prompt_string,
            model_name=dispatched_model["model_name"],
            tier=dispatched_model["tier"],
            output_content=unmasked_output,
            source_file=source_label
        )
        saved_trail_path = AuditTrailLogger.save_record(audit_record)

        # 10. Yanıtı Döndür
        is_successful = bool(unmasked_output and len(unmasked_output.strip()) > 10)
        return {
            "success": is_successful,
            "output_content": unmasked_output,
            "dispatched_model": dispatched_model,
            "complexity_tier": dispatched_model["tier"],
            "execution_time_sec": elapsed_time,
            "audit_trail_id": audit_record["audit_trail_id"],
            "audit_trail_file": saved_trail_path,
            "masked_fields_count": len(self.masker.mapping) if enable_masking else 0,
            "is_simulation": execution_result.get("is_simulation", False),
            "input_hash": audit_record["input_data_sha256"],
            "prompt_used": full_prompt_string,
            "extracted_evidence_count": evidence_data.get("evidence_count", 0),
            "quality_evaluation": qa_result
        }

    def execute_analytics_code(self, script_code: str, input_files: Optional[Union[list, str]] = None) -> Dict[str, Any]:
        """Üretilen Python analitik kodunu yerel sandbox içinde güvenle çalıştırır."""
        files_list = [input_files] if isinstance(input_files, str) else (input_files or [])
        return self.sandbox.execute_script(script_code, files_list)

    def execute_analytics_script(self, script_code: str, data_file_path: Optional[str] = None, input_files: Optional[list] = None) -> Dict[str, Any]:
        """Arayüz ve testlerle geriye dönük uyumlu analitik yürütme arayüzü."""
        files = []
        if data_file_path:
            files.append(data_file_path)
        if input_files:
            files.extend(input_files)
        return self.sandbox.execute_script(script_code, files)

    def export_workpaper_docx(
        self,
        title: str,
        content: str,
        audit_trail_id: str = "AT-2026-LOCAL",
        context: str = "Mega Holding A.Ş. — Kurumsal İç Denetim"
    ) -> bytes:
        """Çalışma kağıdını resmi Word (.docx) formatına dönüştürür."""
        return self.exporter.export_to_docx(title, content, audit_trail_id, context)

    def export_workpaper_excel(self, title: str, content: str) -> bytes:
        """Tabloları ve çalışma kağıdını biçimlendirilmiş Excel (.xlsx) formatına dönüştürür."""
        return self.exporter.export_to_excel(title, content)

    def search_regulations(self, query: str, top_k: int = 3) -> list:
        """Sorgu ile ilgili BDDK/MASAK/SOX/ISO mevzuat maddelerini getirir."""
        return self.knowledge_base.search_relevant_criteria(query, top_k)
