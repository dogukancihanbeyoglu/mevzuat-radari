"""
Local Audit AI - Dinamik Mevzuat (Offline RAG) Kapsamlı Benchmark Test Paketi
15 Farklı Kurumsal ve Hukuki Uç Senaryoda Dinamik Eşleşmeyi Doğrular.
"""
import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.knowledge.rag_engine import AuditKnowledgeBase

@pytest.fixture
def kb():
    return AuditKnowledgeBase()

def test_rag_case_01_bank_embezzlement(kb):
    """1. Banka Zimmeti ve Nitelikli Dolandırıcılık"""
    results = kb.search_relevant_criteria("Şube müdürü kasa açığı zimmet para aktarma usulsüz kredi", top_k=2)
    assert len(results) >= 1
    assert any("BDDK-5411-M160" == r["id"] or "TCK-5237-M158" == r["id"] for r in results)

def test_rag_case_02_related_party_credit_limit(kb):
    """2. İlişkili Taraf Kredi Sınırları"""
    results = kb.search_relevant_criteria("Yönetim kurulu üyesi ortaklara kredi limiti aşımı özkaynak yüzde yirmibeş", top_k=2)
    assert len(results) >= 1
    assert any("BDDK-5411-M50" == r["id"] for r in results)

def test_rag_case_03_ltv_fake_valuation(kb):
    """3. LTV Gayrimenkul Teminat ve Sahte Ekspertiz"""
    results = kb.search_relevant_criteria("Gayrimenkul teminat ekspertiz ltv oranı değerleme karşılık npl", top_k=2)
    assert len(results) >= 1
    assert any("BDDK-KREDI-KAR-YON" == r["id"] for r in results)

def test_rag_case_04_itgc_pam_mfa(kb):
    """4. ITGC, Ayrıcalıklı Erişim ve Siber Güvenlik"""
    results = kb.search_relevant_criteria("Ayrıcalıklı erişim yönetimi pam mfa root ssh loglama bilgi sistemleri", top_k=2)
    assert len(results) >= 1
    assert any("BDDK-ITGC-TEBLIG" == r["id"] or "ISO-27001-A8" == r["id"] for r in results)

def test_rag_case_05_masak_str_suspicious_transfers(kb):
    """5. MASAK Şüpheli İşlem ve Kara Para Aklama"""
    results = kb.search_relevant_criteria("Panama offshore şüpheli işlem bildirimi str kara para aklama smurfing", top_k=2)
    assert len(results) >= 1
    assert any("MASAK-5549-M8" == r["id"] for r in results)

def test_rag_case_06_masak_ubo_pep_screening(kb):
    """6. Paravan Şirket UBO ve PEP Taraması"""
    results = kb.search_relevant_criteria("Gerçek faydalanıcı ubo tespiti pep siyasi nüfuz paravan şirket", top_k=2)
    assert len(results) >= 1
    assert any("MASAK-UBO-TEBLIG" == r["id"] for r in results)

def test_rag_case_07_spk_insider_trading(kb):
    """7. SPK İçeriden Öğrenenlerin Ticareti (Insider Trading)"""
    results = kb.search_relevant_criteria("Halka açık şirket hisse senedi içeriden öğrenenlerin ticareti insider trading menkul kıymet", top_k=2)
    assert len(results) >= 1
    assert any("SPK-6362-M106" == r["id"] for r in results)

def test_rag_case_08_spk_market_manipulation(kb):
    """8. SPK Piyasa Dolandırıcılığı ve Manipülasyon"""
    results = kb.search_relevant_criteria("Piyasa dolandırıcılığı manipülasyon yapay fiyat sahte emir borsa", top_k=2)
    assert len(results) >= 1
    assert any("SPK-6362-M107" == r["id"] for r in results)

def test_rag_case_09_kvkk_data_breach(kb):
    """9. KVKK Müşteri Veri Sızıntısı ve 72 Saatlik İhlal Bildirimi"""
    results = kb.search_relevant_criteria("Kişisel verilerin korunması kvkk veri sızıntısı müşteri tckn ihlal bildirimi 72 saat", top_k=2)
    assert len(results) >= 1
    assert any("KVKK-6698-M12" == r["id"] for r in results)

def test_rag_case_10_kvkk_sanctions(kb):
    """10. KVKK İdari Para Cezaları"""
    results = kb.search_relevant_criteria("Veri sorumlusu idari para cezası kurul kararı güvenlik ihlali cezası kvkk", top_k=2)
    assert len(results) >= 1
    assert any("KVKK-6698-M18" == r["id"] for r in results)

def test_rag_case_11_competition_cartel(kb):
    """11. Rekabet Kurumu Fiyat Tespiti ve Kartel"""
    results = kb.search_relevant_criteria("Rekabet ihlali kartel fiyat tespiti pazar paylaşımı uyumlu eylem", top_k=2)
    assert len(results) >= 1
    assert any("REKABET-4054-M4" == r["id"] for r in results)

def test_rag_case_12_ttk_prudent_merchant(kb):
    """12. TTK Basiretli Tacir Sorumluluğu"""
    results = kb.search_relevant_criteria("Basiretli iş adamı tacir özen borcu şirket yönetimi ticari basiret", top_k=2)
    assert len(results) >= 1
    assert any("TTK-6102-M18" == r["id"] for r in results)

def test_rag_case_13_ttk_board_fiduciary_duty(kb):
    """13. TTK Yönetim Kurulu Özen ve Sadakat Yükümlülüğü"""
    results = kb.search_relevant_criteria("Yönetim kurulu üyeleri sadakat borcu özen yükümlülüğü şirket zararı tazminat", top_k=2)
    assert len(results) >= 1
    assert any("TTK-6102-M369" == r["id"] for r in results)

def test_rag_case_14_sox_internal_control(kb):
    """14. Sarbanes-Oxley SOX 404 İç Kontrol Güvencesi"""
    results = kb.search_relevant_criteria("Sarbanes oxley sox 404 iç kontrol güvencesi finansal raporlama material weakness", top_k=2)
    assert len(results) >= 1
    assert any("SOX-ACT-S404" == r["id"] for r in results)

def test_rag_case_15_iia_global_standards(kb):
    """15. IIA Global 2026 5C Bulgu Yazımı ve Mesleki Şüphecilik"""
    results = kb.search_relevant_criteria("İç denetim standardı iia 5c bulgusu mesleki şüphecilik condition criteria cause", top_k=2)
    assert len(results) >= 1
    assert any("IIA-GLOBAL-2026" == r["id"] for r in results)
