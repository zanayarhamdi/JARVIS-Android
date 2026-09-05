from typing import Dict, Any, Optional
from core.logger import create_logger
from core.config import get_config

logger = create_logger("DECISION_MAKER")

class DecisionMaker:
    """Make decisions about action execution"""
    
    def __init__(self):
        self.config = get_config()
    
    def decide(self, plan: Dict[str, Any], reasoning: Dict[str, Any]) -> Dict[str, Any]:
        """Decide whether and how to execute plan"""
        try:
            decision = {
                'plan_id': plan.get('task_id'),
                'execute': True,
                'requires_confirmation': False,
                'risky_steps': []
            }
            
            # Check if plan is feasible
            if not reasoning.get('feasible'):
                decision['execute'] = False
                decision['message'] = 'طرح قابل اجرا نیست.'
                return decision
            
            # Check for risky operations
            risky_steps = reasoning.get('risks', [])
            if risky_steps:
                decision['requires_confirmation'] = True
                decision['risky_steps'] = risky_steps
                decision['message'] = 'این عملیات ممکن است خطرناک باشد. آیا می‌خواهی ادامه دهم؟'
            
            # Check confidence level
            if reasoning.get('confidence', 1.0) < 0.5:
                decision['requires_confirmation'] = True
                decision['message'] = 'اعتماد من به این طرح کم است. آیا می‌خواهی ادامه دهم؟'
            
            logger.debug(f"Decision: execute={decision['execute']}, confirm={decision['requires_confirmation']}")
            return decision
        except Exception as e:
            logger.error(f"Error making decision: {e}")
            return {'execute': False, 'error': str(e)}
