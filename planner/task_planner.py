from typing import Dict, List, Optional, Any
from core.logger import create_logger
from memory.memory_manager import get_memory_manager

logger = create_logger("TASK_PLANNER")

class TaskPlanner:
    """Decompose complex tasks into actionable steps"""
    
    def __init__(self):
        self.memory = get_memory_manager()
    
    def plan(self, intent: str, entities: Dict[str, Any], context: Optional[Dict] = None) -> Dict[str, Any]:
        """Create task plan from intent and entities"""
        try:
            plan = {
                'task_id': self._generate_task_id(),
                'intent': intent,
                'entities': entities,
                'steps': [],
                'status': 'planning'
            }
            
            # Generate steps based on intent
            if intent == 'file_operation':
                plan['steps'] = self._plan_file_operation(entities)
            elif intent == 'system_info':
                plan['steps'] = self._plan_system_info(entities)
            elif intent == 'code_generation':
                plan['steps'] = self._plan_code_generation(entities)
            elif intent == 'self_improvement':
                plan['steps'] = self._plan_self_improvement(entities)
            else:
                plan['steps'] = self._plan_generic_task(intent, entities)
            
            # Log plan
            self.memory.record_event('task_planned', plan)
            
            logger.info(f"Planned task {plan['task_id']}: {intent} with {len(plan['steps'])} steps")
            return plan
        except Exception as e:
            logger.error(f"Error planning task: {e}")
            return {'task_id': None, 'error': str(e)}
    
    def _generate_task_id(self) -> str:
        """Generate unique task ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _plan_file_operation(self, entities: Dict) -> List[Dict[str, Any]]:
        """Plan file operation steps"""
        steps = [
            {
                'step_id': 1,
                'action': 'find_target_file',
                'params': {'target': entities.get('source', [None])[0]},
                'verify': True
            },
            {
                'step_id': 2,
                'action': 'perform_operation',
                'params': {
                    'operation': entities.get('operation', [''])[0],
                    'source': entities.get('source', [None])[0],
                    'destination': entities.get('destination', [None])[0]
                },
                'verify': True
            },
            {
                'step_id': 3,
                'action': 'verify_result',
                'params': {'operation': entities.get('operation', [''])[0]},
                'verify': True
            }
        ]
        return steps
    
    def _plan_system_info(self, entities: Dict) -> List[Dict[str, Any]]:
        """Plan system info gathering"""
        steps = [
            {
                'step_id': 1,
                'action': 'collect_system_info',
                'params': {},
                'verify': False
            },
            {
                'step_id': 2,
                'action': 'format_response',
                'params': {},
                'verify': False
            }
        ]
        return steps
    
    def _plan_code_generation(self, entities: Dict) -> List[Dict[str, Any]]:
        """Plan code generation"""
        steps = [
            {
                'step_id': 1,
                'action': 'analyze_requirements',
                'params': {'description': entities.get('description', [''])[0]},
                'verify': False
            },
            {
                'step_id': 2,
                'action': 'generate_code',
                'params': {'language': entities.get('language', ['python'])[0]},
                'verify': True
            },
            {
                'step_id': 3,
                'action': 'syntax_check',
                'params': {},
                'verify': True
            },
            {
                'step_id': 4,
                'action': 'create_file',
                'params': {},
                'verify': True
            }
        ]
        return steps
    
    def _plan_self_improvement(self, entities: Dict) -> List[Dict[str, Any]]:
        """Plan self-improvement"""
        steps = [
            {
                'step_id': 1,
                'action': 'backup_system',
                'params': {},
                'verify': True
            },
            {
                'step_id': 2,
                'action': 'analyze_improvement',
                'params': {'description': entities.get('description', [''])[0]},
                'verify': False
            },
            {
                'step_id': 3,
                'action': 'generate_changes',
                'params': {},
                'verify': True
            },
            {
                'step_id': 4,
                'action': 'apply_changes',
                'params': {},
                'verify': True
            },
            {
                'step_id': 5,
                'action': 'test_changes',
                'params': {},
                'verify': True
            },
            {
                'step_id': 6,
                'action': 'log_changes',
                'params': {},
                'verify': False
            }
        ]
        return steps
    
    def _plan_generic_task(self, intent: str, entities: Dict) -> List[Dict[str, Any]]:
        """Plan generic task"""
        return [
            {
                'step_id': 1,
                'action': 'execute_task',
                'params': {'intent': intent, 'entities': entities},
                'verify': True
            }
        ]
