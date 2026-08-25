import io
import sys
import contextlib
from typing import Dict, Any

class CodeSandboxService:
    @staticmethod
    def execute_python_code(code: str) -> Dict[str, Any]:
        """
        Executes Python code in a safe stdout/stderr captured sub-environment.
        """
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        
        local_scope = {}
        try:
            with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
                exec(code, {"__builtins__": __builtins__}, local_scope)
            
            stdout_res = stdout_buf.getvalue()
            stderr_res = stderr_buf.getvalue()
            
            return {
                "success": True,
                "stdout": stdout_res if stdout_res else "Execution completed without printed output.",
                "stderr": stderr_res,
                "result": str(local_scope.get("result", local_scope.get("data", "")))
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": stdout_buf.getvalue(),
                "stderr": f"RuntimeError: {str(e)}",
                "result": None
            }

code_sandbox_service = CodeSandboxService()
