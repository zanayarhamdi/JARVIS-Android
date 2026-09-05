from typing import Optional, Any, Dict
from core.logger import create_logger
import subprocess
import os

logger = create_logger("SANDBOX")

class Sandbox:
    """Execute code in sandboxed environment"""
    
    def __init__(self):
        self.timeout = 30
        self.allowed_modules = [
            'os', 'sys', 're', 'json', 'datetime',
            'pathlib', 'subprocess', 'threading'
        ]
    
    def execute_code(
        self,
        code: str,
        timeout: Optional[int] = None,
        allowed_imports: Optional[list] = None
    ) -> Dict[str, Any]:
        """Execute code in sandbox"""
        try:
            timeout = timeout or self.timeout
            allowed = allowed_imports or self.allowed_modules
            
            # Validate code for dangerous operations
            if not self._validate_code(code, allowed):
                return {
                    'success': False,
                    'error': 'Code contains dangerous operations',
                    'output': ''
                }
            
            # Execute with timeout
            result = subprocess.run(
                ['python3', '-c', code],
                capture_output=True,
                timeout=timeout,
                text=True
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'return_code': result.returncode
            }
        except subprocess.TimeoutExpired:
            logger.error("Code execution timeout")
            return {'success': False, 'error': 'Execution timeout', 'output': ''}
        except Exception as e:
            logger.error(f"Error executing code: {e}")
            return {'success': False, 'error': str(e), 'output': ''}
    
    def _validate_code(self, code: str, allowed_modules: list) -> bool:
        """Validate code for security"""
        dangerous_operations = [
            'exec', 'eval', '__import__', 'open',
            'input', 'compile', 'delattr', 'setattr',
            'os.system', 'subprocess.call', 'commands'
        ]
        
        for op in dangerous_operations:
            if op in code:
                return False
        
        return True
