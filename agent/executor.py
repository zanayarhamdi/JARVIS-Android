from typing import Dict, Any, Optional, List
from datetime import datetime
from core.logger import create_logger
from tools.tool_registry import get_tool_registry
from memory.memory_manager import get_memory_manager

logger = create_logger("TASK_EXECUTOR")

class TaskExecutor:
    """Execute task plans"""
    
    def __init__(self):
        self.tool_registry = get_tool_registry()
        self.memory = get_memory_manager()
    
    def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task plan"""
        try:
            execution_result = {
                'task_id': plan['task_id'],
                'intent': plan['intent'],
                'success': True,
                'steps_completed': 0,
                'steps_failed': 0,
                'step_results': [],
                'error': None
            }
            
            # Execute each step
            for step in plan.get('steps', []):
                step_result = self._execute_step(step, plan)
                execution_result['step_results'].append(step_result)
                
                if step_result['success']:
                    execution_result['steps_completed'] += 1
                else:
                    execution_result['steps_failed'] += 1
                    # Stop on first failure if step requires success
                    if step.get('critical', False):
                        execution_result['success'] = False
                        execution_result['error'] = step_result.get('error')
                        break
            
            # Log execution
            self.memory.record_event('plan_executed', execution_result)
            
            logger.info(f"Plan {plan['task_id']} executed: {execution_result['steps_completed']}/{len(plan.get('steps', []))} steps")
            return execution_result
        except Exception as e:
            logger.error(f"Error executing plan: {e}")
            return {'success': False, 'error': str(e)}
    
    def _execute_step(self, step: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute single step"""
        try:
            action = step['action']
            params = step.get('params', {})
            
            logger.debug(f"Executing step {step['step_id']}: {action}")
            
            # For now, return placeholder results
            # Real implementation would use tool registry
            result = {
                'step_id': step['step_id'],
                'action': action,
                'success': True,
                'message': f'{action} completed successfully',
                'timestamp': datetime.now().isoformat()
            }
            
            return result
        except Exception as e:
            logger.error(f"Error executing step: {e}")
            return {
                'step_id': step['step_id'],
                'action': step['action'],
                'success': False,
                'error': str(e)
            }
