"""
LLM Configuration and Provider Management Module.
Supports Rule-based, OpenAI, Anthropic, Gemini, and Local (Ollama/DeepSeek) models.
"""
import os
import yaml
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
