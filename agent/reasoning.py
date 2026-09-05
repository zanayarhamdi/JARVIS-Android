from typing import Dict, Any, Optional, List
from core.logger import create_logger
from memory.memory_manager import get_memory_manager

logger = create_logger("REASONING_ENGINE")

class ReasoningEngine:
    """Reasoning engine for decision making"""
    
    def __init__(self):
        self.memory = get_memory_manager()
    
    def reason(self, plan: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Reason about plan feasibility and risks"""
        try:
            reasoning = {
                'plan_id': plan.get('task_id'),
                'feasible': True,
                'confidence': 1.0,
                'risks': [],
                'assumptions': [],
                'dependencies': []
            }
            
            # Analyze plan steps
            for step in plan.get('steps', []):
                if step.get('verify'):
                    reasoning['assumptions'].append({
                        'step': step['step_id'],
                        'assumption': f"Step {step['step_id']} will complete successfully"
                    })
                
                # Identify risky steps
                if self._is_risky_action(step['action']):
                    reasoning['risks'].append({
                        'step': step['step_id'],
                        'action': step['action'],
                        'risk_level': 'HIGH'
                    })
                    reasoning['confidence'] -= 0.1
            
            # Check memory for similar past actions
            similar_events = self.memory.search_events(plan['intent'])
            if similar_events:
                reasoning['similar_past_actions'] = len(similar_events)
            
            logger.debug(f"Reasoning complete: {reasoning['feasible']} (confidence: {reasoning['confidence']})")
            return reasoning
        except Exception as e:
            logger.error(f"Error reasoning: {e}")
            return {'feasible': False, 'error': str(e)}
    
    def _is_risky_action(self, action: str) -> bool:
        """Determine if action is risky"""
        risky_actions = ['delete', 'modify_system', 'install_package', 'apply_changes']
        return action in risky_actions
