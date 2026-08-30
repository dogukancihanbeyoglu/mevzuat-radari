"""
Local Audit AI - Güvenli Yerel Python Yürütme Sandbox'ı (Local Python Execution Sandbox)
Üretilen pandas analiz kodlarını yerel, izole bir ortamda çalıştırıp istisna Excel dosyalarını otomatik üretir.
"""
import os
import sys
import re
import shutil
import tempfile
import subprocess
import time
from typing import Dict, Any, List, Optional

class LocalPythonSandbox:
    def __init__(self, timeout_sec: int = 60):
        self.timeout_sec = timeout_sec

    def extract_python_code(self, raw_content: str) -> str:
        """Markdown kod blokları içindeki Python kodunu ayıklar."""
        code_blocks = re.findall(r"```(?:python)?\s*(.*?)\s*```", raw_content, re.DOTALL)
        if code_blocks:
            return "\n\n".join(code_blocks)
        
        # Kod bloğu yoksa ve kod satırları içeriyorsa doğrudan döner
        lines = [l for l in raw_content.splitlines() if not l.startswith("#") or "import" in l or "pd." in l]
        return "\n".join(lines) if "import pandas" in raw_content or "pd." in raw_content else raw_content

    def execute_script(
        self,
        script_content: str,
        input_files: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Python kodunu geçici bir dizinde çalıştırır, girdi dosyalarını ortama bağlar
        ve üretilen tüm Excel/CSV çıktılarını yakalar.
        """
        clean_code = self.extract_python_code(script_content)
        if not clean_code.strip():
            return {
                "success": False,
                "error": "Çalıştırılacak geçerli Python analitik kodu bulunamadı.",
                "stdout": "",
                "stderr": "",
                "generated_files": []
            }

        start_time = time.time()
        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Girdi dosyalarını geçici dizine kopyala
            copied_files = []
            if input_files:
                for src in input_files:
                    if os.path.exists(src):
                        dest_name = os.path.basename(src)
                        dest_path = os.path.join(temp_dir, dest_name)
                        shutil.copy2(src, dest_path)
                        copied_files.append(dest_name)

            # Kodun aradığı dosya adlarını (regex ile) tespit et ve ortamdaki ilk eşleşen dosyadan kopyala
            referenced_files = re.findall(r"['\"]([^'\"]+\.(?:xlsx|xls|csv|txt|docx))['\"]", clean_code)
            all_source_excel = [f for f in copied_files if f.endswith(('.xlsx', '.xls', '.csv'))]
            
            for ref in referenced_files:
                ref_base = os.path.basename(ref)
                target_path = os.path.join(temp_dir, ref_base)
                if not os.path.exists(target_path):
                    # 1. Öncelik: Yüklenen excel dosyasını bu isme kopyala
                    if all_source_excel:
                        shutil.copy2(os.path.join(temp_dir, all_source_excel[0]), target_path)
                    # 2. Öncelik: storage/test_data klasöründen ara
                    elif os.path.exists(f"storage/test_data/{ref_base}"):
                        shutil.copy2(f"storage/test_data/{ref_base}", target_path)
                    elif os.path.exists("storage/test_data/transactions_sample.xlsx"):
                        shutil.copy2("storage/test_data/transactions_sample.xlsx", target_path)
                    # 3. Öncelik: Proje içindeki sample_test_files klasöründen ara
                    else:
                        for root, _, files in os.walk("sample_test_files"):
                            if ref_base in files:
                                shutil.copy2(os.path.join(root, ref_base), target_path)
                                break

            # 2. Python dosyasını yaz
            script_file = os.path.join(temp_dir, "run_audit_analysis.py")
            with open(script_file, "w", encoding="utf-8") as f:
                f.write(clean_code)

            # 3. İzole subprocess ile çalıştır
            try:
                proc = subprocess.run(
                    [sys.executable, script_file],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_sec
                )
                stdout = proc.stdout
                stderr = proc.stderr
                success = (proc.returncode == 0)

            except subprocess.TimeoutExpired:
                return {
                    "success": False,
                    "error": f"Betiğin yürütülmesi {self.timeout_sec} saniyelik zaman aşımı süresini aştı.",
                    "stdout": "",
                    "stderr": "TimeoutExpired",
                    "generated_files": []
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Yürütme hatası: {str(e)}",
                    "stdout": "",
                    "stderr": str(e),
                    "generated_files": []
                }

            elapsed = round(time.time() - start_time, 2)

            # 4. Üretilen yeni çıktı dosyalarını tespit et ve kalıcı çıktı dizinine kopyala
            output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../storage/generated_reports"))
            os.makedirs(output_dir, exist_ok=True)

            generated_files = []
            for item in os.listdir(temp_dir):
                if item in copied_files or item in ["run_audit_analysis.py", "transactions.xlsx"]:
                    continue
                if item.endswith(('.xlsx', '.xls', '.csv', '.png', '.pdf')):
                    full_src = os.path.join(temp_dir, item)
                    target_dest = os.path.join(output_dir, f"audit_{int(time.time())}_{item}")
                    shutil.copy2(full_src, target_dest)
                    
                    with open(target_dest, "rb") as bf:
                        file_bytes = bf.read()

                    generated_files.append({
                        "file_name": item,
                        "file_path": target_dest,
                        "file_size_kb": round(len(file_bytes) / 1024, 2),
                        "file_bytes": file_bytes
                    })

            return {
                "success": success,
                "execution_time_sec": elapsed,
                "stdout": stdout,
                "stderr": stderr,
                "error": stderr if not success else None,
                "generated_files": generated_files
            }
