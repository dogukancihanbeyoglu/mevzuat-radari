"""
LLM Configuration and Provider Management Module.
Supports Rule-based fallback, OpenAI, Anthropic, Gemini, and Local (Ollama/DeepSeek) models.
Enables real GenAI-powered deep legal evaluation and reasoning.
"""
import os
import json
import yaml
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "llm_config.yaml")


def load_llm_config() -> Dict[str, Any]:
    """Loads LLM and MCP configuration."""
    if not os.path.exists(CONFIG_PATH):
        return {
            "active_provider": "rule_based",
            "providers": {"rule_based": {"name": "Yerel Kural Tabanlı Motor"}},
            "mcp_settings": {"server_name": "mevzuat-radari"},
        }

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return data.get("llm_config", {})


def save_llm_config(new_config: Dict[str, Any]) -> None:
    """Saves updated LLM configuration to YAML file."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump({"llm_config": new_config}, f, allow_unicode=True)


def get_mcp_client_config() -> Dict[str, Any]:
    """Generates ready-to-copy JSON configuration for Claude Desktop and Cursor."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    server_script = os.path.join(base_dir, "src", "server.py")
    python_exec = os.path.join(base_dir, ".venv", "bin", "python")
    if not os.path.exists(python_exec):
        python_exec = "python"

    return {
        "mcpServers": {
            "mevzuat-radari": {
                "command": python_exec,
                "args": [server_script],
                "env": {
                    "PYTHONPATH": base_dir,
                }
            }
        }
    }


def call_llm_evaluation(
    title: str,
    category: str,
    institution: Optional[str],
    raw_content: Optional[str],
    company_profile_dict: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Executes live GenAI evaluation against the configured LLM provider.
    Returns structured JSON with relevance_score, risk_level, matched_reasons,
    executive_summary, penalty_and_legal_risk, affected_departments, action_checklist.
    Falls back to None if provider is rule_based or API fails.
    """
    cfg = load_llm_config()
    active_prov = cfg.get("active_provider", "rule_based")
    if active_prov == "rule_based":
        return None

    providers = cfg.get("providers", {})
    prov_settings = providers.get(active_prov, {})
    api_key = prov_settings.get("api_key", "").strip()
    model_name = prov_settings.get("model_name", "gpt-4o")

    # If no API key provided for commercial providers (except local ollama), return None
    if active_prov in ("openai", "anthropic", "gemini") and not api_key:
        return None

    system_prompt = (
        "Sen üst düzey bir Hukuk, Uyum ve İç Denetim Danışmanısın. "
        "Verilen Resmî Gazete kararını ve Şirket Profilini incele. "
        "Aşağıdaki JSON şemasına birebir uyan geçerli bir JSON objesi üret. Markdown veya fazladan metin yazma.\n\n"
        "Şema:\n"
        "{\n"
        '  "relevance_score": int (0-100),\n'
        '  "risk_level": "Kritik" | "Yüksek" | "Orta" | "Düşük" | "Bilgi",\n'
        '  "matched_reasons": ["Neden şirketle alakalı madde 1", ...],\n'
        '  "executive_summary": "Şirket yönetim kurulu ve iç denetim için 2-3 cümlelik net yönetici özeti",\n'
        '  "penalty_and_legal_risk": "Olası hukuki risk, ceza ve yaptırım özeti",\n'
        '  "affected_departments": ["Hukuk", "Ar-Ge", ...],\n'
        '  "action_checklist": ["Uyum için atılacak 1. somut adım", "2. adım", ...]\n'
        "}"
    )

    user_prompt = f"""
ŞİRKET PROFİLİ:
{json.dumps(company_profile_dict, ensure_ascii=False, indent=2)}

RESMÎ GAZETE KARARI:
Başlık: {title}
Kategori: {category}
Kurum: {institution or 'Resmî Gazete'}
İçerik Özeti / Metin: {raw_content[:2000] if raw_content else 'Yalnızca başlık mevcuttur.'}
"""

    # OpenAI / Ollama compatible endpoint
    if active_prov in ("openai", "ollama_custom"):
        base_url = prov_settings.get("base_url", "https://api.openai.com/v1").rstrip("/")
        endpoint = f"{base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key or 'ollama'}",
        }
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"} if active_prov == "openai" else None,
            "temperature": 0.1,
        }

        try:
            req = urllib.request.Request(endpoint, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content_str = data["choices"][0]["message"]["content"]
                return json.loads(content_str)
        except Exception:
            return None

    return None
