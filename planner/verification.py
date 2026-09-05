from typing import Dict, Any, Optional, List
from core.logger import create_logger
from memory.memory_manager import get_memory_manager

logger = create_logger("VERIFIER")

class Verifier:
    """Verify task execution results"""
    
    def __init__(self):
        self.memory = get_memory_manager()
    
    def verify(self, task_result: Dict[str, Any], expected_outcome: Optional[str] = None) -> Dict[str, Any]:
        """Verify task result"""
        try:
            verification = {
                'task_result': task_result,
                'verified': False,
                'confidence': 0.0,
                'issues': []
            }
            
            # Check if task succeeded
            if task_result.get('success'):
                verification['verified'] = True
                verification['confidence'] = 0.9
            elif task_result.get('error'):
                verification['issues'].append(f"Task failed: {task_result['error']}")
                verification['confidence'] = 0.0
            
            # Store verification result
            self.memory.record_event('task_verified', verification)
            
            logger.debug(f"Verified task: {verification['verified']} (confidence: {verification['confidence']})")
            return verification
        except Exception as e:
            logger.error(f"Error verifying task: {e}")
            return {'verified': False, 'error': str(e)}
