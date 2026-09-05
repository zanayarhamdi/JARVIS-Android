from typing import Dict, Optional
from core.logger import create_logger

logger = create_logger("CONFIRMATION_MANAGER")

class ConfirmationManager:
    """Manage user confirmations"""
    
    def __init__(self):
        self.pending_confirmations: Dict[str, Dict] = {}
    
    def request_confirmation(
        self,
        task_id: str,
        message: str,
        details: Optional[Dict] = None,
        options: Optional[list] = None
    ) -> Dict:
        """Request user confirmation"""
        try:
            confirmation_request = {
                'task_id': task_id,
                'message': message,
                'details': details or {},
                'options': options or ['yes', 'no'],
                'confirmed': None
            }
            
            self.pending_confirmations[task_id] = confirmation_request
            logger.debug(f"Confirmation requested for task: {task_id}")
            
            return confirmation_request
        except Exception as e:
            logger.error(f"Error requesting confirmation: {e}")
            return {'error': str(e)}
    
    def provide_confirmation(self, task_id: str, response: str) -> bool:
        """Provide confirmation response"""
        try:
            if task_id not in self.pending_confirmations:
                logger.warning(f"No pending confirmation for task: {task_id}")
                return False
            
            confirmation = self.pending_confirmations[task_id]
            confirmation['confirmed'] = response.lower() in ['yes', 'y', 'confirm']
            
            logger.debug(f"Confirmation provided for task {task_id}: {confirmation['confirmed']}")
            return confirmation['confirmed']
        except Exception as e:
            logger.error(f"Error providing confirmation: {e}")
            return False
    
    def get_pending_confirmations(self) -> Dict:
        """Get all pending confirmations"""
        return self.pending_confirmations.copy()
