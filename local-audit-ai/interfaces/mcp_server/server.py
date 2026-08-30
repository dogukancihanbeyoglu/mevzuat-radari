"""
Local Audit AI - Model Context Protocol (MCP) Server
Yerel AI İstemcileri (Cursor, Antigravity, Claude Desktop vb.) için Denetim MCP Sunucusu
"""
import sys
import json
import os

# Ana proje dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from modules import AuditOrchestrator

orchestrator = AuditOrchestrator()

def handle_request(req: dict) -> dict:
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "local-audit-ai", "version": "1.0.0"}
            }
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "generate_5c_finding",
                        "description": "IIA standartlarında 5C (Condition, Criteria, Cause, Effect, Recommendation) bulgu taslağı ve denetim izi üretir.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "factual_notes": {"type": "string", "description": "Sahadan toplanan ham bulgu ve gözlem notları."},
                                "custom_context": {"type": "string", "description": "Denetlenen süreç, mevzuat ve şirket bağlamı."}
                            },
                            "required": ["factual_notes"]
                        }
                    },
                    {
                        "name": "build_rcm_matrix",
                        "description": "Süreç anlatımından Risk ve Kontrol Matrisi (RCM) ve Walkthrough mülakat soru seti üretir.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "process_narrative": {"type": "string", "description": "Süreç prosedürü veya akış metni."}
                            },
                            "required": ["process_narrative"]
                        }
                    },
                    {
                        "name": "generate_analytics_script",
                        "description": "Sürekli denetim için mükerrer kayıt, SoD ve limit aşımı bulan Python/Pandas analiz kodu üretir.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "columns_and_rules": {"type": "string", "description": "Veri seti sütunları ve test kuralları."}
                            },
                            "required": ["columns_and_rules"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        try:
            if tool_name == "generate_5c_finding":
                res = orchestrator.run_audit_task(
                    module_name="finding_5c",
                    input_text=args.get("factual_notes", ""),
                    custom_context=args.get("custom_context", "Internal Audit Review")
                )
            elif tool_name == "build_rcm_matrix":
                res = orchestrator.run_audit_task(
                    module_name="rcm_generation",
                    input_text=args.get("process_narrative", "")
                )
            elif tool_name == "generate_analytics_script":
                res = orchestrator.run_audit_task(
                    module_name="data_analytics",
                    input_text=args.get("columns_and_rules", "")
                )
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Bilinmeyen araç: {tool_name}"}
                }

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {"type": "text", "text": res["output_content"]},
                        {"type": "text", "text": f"\n\n---\n**[IIA Audit Trail ID]**: {res['audit_trail_id']} | Model: {res['dispatched_model']['model_name']} ({res['dispatched_model']['tier']})"}
                    ]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32000, "message": str(e)}
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Geçersiz istek"}}

def main():
    """stdio üzerinden JSON-RPC loop"""
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
