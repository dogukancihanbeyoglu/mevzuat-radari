"""
Local Audit AI - Kapsamlı Kalite Güvence ve Otomasyon Testleri (12/12)
Tüm güvenlik, model registry, prompt üretimi, sandbox, exporter, RAG, smart extractor ve QA modüllerini test eder.
"""
import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.security import PIIMasker, AuditTrailLogger
from core.router import ComplexityAnalyzerAgent, ModelDispatcher
from core.router.model_registry import ModelRegistry
from core.prompt_engine import PromptFactory
from core.execution.sandbox import LocalPythonSandbox
from core.export.workpaper_exporter import WorkpaperExporter
from core.knowledge.rag_engine import AuditKnowledgeBase
from core.ingestion.smart_extractor import SmartEvidenceExtractor
from core.quality.evaluator import AuditQualityEvaluator
from modules import AuditOrchestrator

def test_pii_masker():
    """Hassas verilerin (TCKN, IBAN, Kart, E-posta) maskelenip açıldığını doğrular."""
    masker = PIIMasker()
    test_text = (
        "Denetçi Ahmet (TCKN: 12345678901, E-posta: ahmet@sirket.com.tr), "
        "TR330006100511123456789012 nolu IBAN hesabına 5400123456789012 kartıyla işlem yapmıştır."
    )
    masked_text = masker.mask(test_text)
    
    assert "[TCKN_" in masked_text
    assert "[IBAN_" in masked_text
    assert "[CREDIT_CARD_" in masked_text
    assert "[EMAIL_" in masked_text
    assert len(masker.mapping) == 4

    unmasked = masker.unmask(masked_text)
    assert unmasked == test_text

def test_audit_trail_logger():
    """Kriptografik SHA-256 denetim izi kaydı üretimini doğrular."""
    record = AuditTrailLogger.create_record(
        task_name="finding_5c",
        input_data="Örnek denetim girdisi",
        generated_prompt="Örnek prompt",
        model_name="deepseek-r1:8b",
        tier="tier_2_standard",
        output_content="Örnek 5C bulgu çıktısı"
    )
    assert record["audit_trail_id"].startswith("AT-")
    assert len(record["input_data_sha256"]) == 64
    assert len(record["output_sha256"]) == 64
    assert record["dispatched_model"] == "deepseek-r1:8b"

def test_complexity_router():
    """Router ajanının doğru Tier ve model ataması yaptığını doğrular."""
    dispatcher = ModelDispatcher()

    eval_light = ComplexityAnalyzerAgent.evaluate("data_extraction", "Fatura metinlerinden verileri ayıkla.")
    model_light = dispatcher.dispatch(eval_light)
    assert "tier_1" in eval_light["tier"]
    assert "7b" in model_light["model_name"]

    eval_med = ComplexityAnalyzerAgent.evaluate("finding_5c", "Yetki aşımı tespit edilmiştir.")
    model_med = dispatcher.dispatch(eval_med)
    assert "tier_2" in eval_med["tier"]

    eval_code = ComplexityAnalyzerAgent.evaluate("data_analytics", "Pandas ile 500 satırlık veride mükerrer fatura ve SoD bul.")
    model_code = dispatcher.dispatch(eval_code)
    assert "tier_3" in eval_code["tier"]
    assert "14b" in model_code["model_name"]

def test_model_registry_dynamic_update():
    """ModelRegistry ile Tier modelleri güncellendiğinde Router'ın otomatik olarak yeni modeli seçtiğini doğrular."""
    registry = ModelRegistry()
    dispatcher = ModelDispatcher()

    # 1. Tier 1'e yeni model kaydet
    registry.update_tier_model("tier_1_light", "qwen3-coder:7b")
    eval_light = ComplexityAnalyzerAgent.evaluate("data_extraction", "Fatura ayıkla.")
    dispatched = dispatcher.dispatch(eval_light)
    assert dispatched["model_name"] == "qwen3-coder:7b"

    # 2. Eski modeline geri döndür
    registry.update_tier_model("tier_1_light", "qwen2.5-coder:7b")
    dispatched_restored = dispatcher.dispatch(eval_light)
    assert dispatched_restored["model_name"] == "qwen2.5-coder:7b"

def test_autonomous_auto_tiering():
    """ModelRegistry'nin yerel modelleri yeteneklerine göre otonom puanlayıp Tier 1/2/3 eşleştirmesi yaptığını doğrular."""
    registry = ModelRegistry()
    
    # Model Puanlama Testi
    score_coder = registry.classify_and_score_model("qwen2.5-coder:14b")
    assert score_coder["tier_3_score"] > score_coder["tier_1_score"]

    score_r1 = registry.classify_and_score_model("deepseek-r1:8b")
    assert score_r1["tier_2_score"] > score_r1["tier_3_score"]

    score_light = registry.classify_and_score_model("qwen2.5:7b")
    assert score_light["tier_1_score"] > score_light["tier_3_score"]

    # Otonom Konfigürasyon Testi
    auto_res = registry.auto_configure_best_tiers()
    assert auto_res["success"] is True
    assert "tier_1_light" in auto_res["selected_tiers"]
    assert "tier_2_standard" in auto_res["selected_tiers"]
    assert "tier_3_deep_reasoning" in auto_res["selected_tiers"]

def test_prompt_factory():
    """IIA 8-bileşenli Türkçe prompt üreticisinin tüm zorunlu alanları içerdiğini doğrular."""
    factory = PromptFactory(templates_path="config/iia_templates.yaml")
    prompt_obj, full_prompt = factory.create_prompt(
        module_name="finding_5c",
        input_data="14 faturada çift onay eksikliği tespit edildi.",
        custom_context="Üretim Şirketi Finans Denetimi"
    )
    assert "# ROL VE UZMANLIK" in full_prompt
    assert "# KURUMSAL BAĞLAM VE ÇEVRE" in full_prompt
    assert "# DENETİM GÖREVİ VE HEDEF" in full_prompt
    assert "# ÇIKTI FORMATI" in full_prompt
    assert "# KESİN DİL KURALI" in full_prompt

def test_python_sandbox():
    """Yerel Python sandbox'ının pandas kodunu çalıştırıp Excel ürettiğini doğrular."""
    sandbox = LocalPythonSandbox()
    sample_code = """
import pandas as pd
data = {'vendor_id': ['V1', 'V2', 'V1'], 'amount': [100, 200, 100]}
df = pd.DataFrame(data)
with pd.ExcelWriter('audit_exceptions.xlsx') as writer:
    df.to_excel(writer, sheet_name='Exceptions', index=False)
print('Analiz tamamlandi, satir sayisi:', len(df))
"""
    res = sandbox.execute_script(sample_code)
    assert res["success"] is True
    assert "Analiz tamamlandi" in res["stdout"]
    assert len(res["generated_files"]) >= 1
    assert res["generated_files"][0]["file_name"] == "audit_exceptions.xlsx"

def test_workpaper_exporter():
    """Resmi antetli Word (.docx) ve Excel (.xlsx) ihracını doğrular."""
    exporter = WorkpaperExporter()
    markdown_content = (
        "# 5C DENETİM BULGUSU\n\n"
        "| Süreç | Risk | Durum |\n"
        "| Hazine | Yüksek | Kritik |\n\n"
        "- **1. Condition:** Yetkisiz limit aşımı tespit edildi.\n"
        "- **2. Criteria:** BDDK Madde 11."
    )
    docx_bytes = exporter.export_to_docx(
        title="5C Bulgu Çalışma Kağıdı",
        content=markdown_content,
        audit_trail_id="AT-TEST-001"
    )
    assert len(docx_bytes) > 1000
    assert docx_bytes.startswith(b"PK")

    xlsx_bytes = exporter.export_to_excel(
        title="RCM Tablosu",
        content=markdown_content
    )
    assert len(xlsx_bytes) > 1000
    assert xlsx_bytes.startswith(b"PK")

def test_knowledge_base():
    """Mevzuat ve kriter bilgi tabanının dinamik semantik eşleşmesini ve çoklu otoriteleri doğrular."""
    kb = AuditKnowledgeBase()
    
    # BDDK Kredi ve Zimmet
    res_bddk = kb.search_relevant_criteria("Kredi tahsis şube müdürü yetki aşımı ve teminat ekspertiz zimmet", top_k=2)
    assert len(res_bddk) >= 1
    assert any("BDDK" in r["authority"] or "Zimmet" in r["title"] for r in res_bddk)

    # KVKK Veri Sızıntısı
    res_kvkk = kb.search_relevant_criteria("Müşteri kredi kartı ve TCKN veri sızıntısı gizlilik ihlal bildirimi", top_k=2)
    assert len(res_kvkk) >= 1
    assert any("KVKK" in r["authority"] for r in res_kvkk)

def test_smart_evidence_extractor():
    """Büyük metinlerden kritik riskli satırları ayıklama motorunu doğrular."""
    extractor = SmartEvidenceExtractor()
    sample_text = (
        "Normal işlem 100 TL.\n"
        "Levent şubesinde 45.000.000 USD yetkisiz kredi tahsisi yapıldı ve sahte ekspertiz kullanıldı.\n"
        "Panama hesaplarına MASAK filtresi bypass edilerek 32.500.000 USD şüpheli transfer yapıldı.\n"
        "Rutin kırtasiye alımı 500 TL."
    )
    res = extractor.extract_critical_evidence(sample_text)
    assert res["evidence_count"] >= 2
    assert "AKILLI AYIKLANAN ÖNCELİKLİ DENETİM KANITLARI" in res["brief_text"]

def test_audit_quality_evaluator():
    """Model çıktısının IIA standartları kalite puanlamasını (0-100) doğrular."""
    evaluator = AuditQualityEvaluator()
    sample_output = (
        "# 5C DENETİM BULGUSU\n\n"
        "- **1. Condition (Mevcut Durum):** 45.000.000 USD sahte teminatla yetkisiz kredi tahsisi yapılmıştır.\n"
        "- **2. Criteria (Kriter):** 5411 Sayılı Bankacılık Kanunu ve BDDK Yönetmeliği Madde 8.\n"
        "- **3. Cause (Kök Neden):** Şube Müdürünün yetki sınırlarını kasıtlı olarak aşması.\n"
        "- **4. Effect (Risk ve Etki):** Bankanın 45M USD batık kredi zararına ve MASAK cezalarına maruz kalması.\n"
        "- **5. Recommendation (Öneri):** Cumhuriyet Başsavcılığına suç duyurusu ve SAP blokajı."
    )
    res = evaluator.evaluate_output_quality("finding_5c", sample_output)
    assert res["score"] >= 90
    assert res["is_high_quality"] is True

def test_model_override_execution():
    """Kullanıcının seçtiği özel modelin (model_override) başarıyla devreye girdiğini doğrular."""
    orchestrator = AuditOrchestrator(config_path="config/config.yaml")
    result = orchestrator.run_audit_task(
        module_name="finding_5c",
        input_text="Test girdisi.",
        model_override="llama3.3:70b",
        custom_temperature=0.35
    )
    assert result["dispatched_model"]["model_name"] == "llama3.3:70b"
    assert result["dispatched_model"]["is_override"] is True
    assert result["dispatched_model"]["temperature"] == 0.35

def test_orchestrator_end_to_end():
    """Tüm sistemin uçtan uca çalışıp kalite skoruyla birlikte rapor ürettiğini doğrular."""
    orchestrator = AuditOrchestrator(config_path="config/config.yaml")
    result = orchestrator.run_audit_task(
        module_name="finding_5c",
        input_text="Levent şubesinde 45.000.000 USD yetkisiz kredi tahsisi ve sahte ekspertiz saptandı.",
        custom_context="Global Yatırım Bankası A.Ş."
    )
    assert result["success"] is True
    assert "output_content" in result
    assert result["audit_trail_id"].startswith("AT-")
    assert "quality_evaluation" in result

def test_orchestrator_export_methods():
    """Orchestrator'ın Word ve Excel ihraç metotlarının parametre uyumluluğunu doğrular."""
    orchestrator = AuditOrchestrator(config_path="config/config.yaml")
    sample_content = "# Test Başlık\n\n- Durum: 100 TL anomali tespit edildi."
    
    # 1. Varsayılan context ile Word İhracı
    docx_bytes_default = orchestrator.export_workpaper_docx(
        title="Test Çalışma Kağıdı",
        content=sample_content,
        audit_trail_id="AT-2026-TEST"
    )
    assert len(docx_bytes_default) > 0
    assert isinstance(docx_bytes_default, bytes)

    # 2. Özel context ile Word İhracı
    docx_bytes_custom = orchestrator.export_workpaper_docx(
        title="Test Çalışma Kağıdı",
        content=sample_content,
        audit_trail_id="AT-2026-TEST",
        context="Özel Holding A.Ş."
    )
    assert len(docx_bytes_custom) > 0

    # 3. Excel İhracı
    xlsx_bytes = orchestrator.export_workpaper_excel(
        title="Test Tablosu",
        content="| Sütun 1 | Sütun 2 |\n| --- | --- |\n| Veri A | Veri B |"
    )
    assert len(xlsx_bytes) > 0
    assert isinstance(xlsx_bytes, bytes)
