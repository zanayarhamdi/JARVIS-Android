from typing import Dict, Any, Optional
from datetime import datetime
from core.logger import create_logger
from brain.nlu import NLUEngine
from planner.task_planner import TaskPlanner
from agent.executor import TaskExecutor
from agent.reasoning import ReasoningEngine
from agent.decision_maker import DecisionMaker
from memory.memory_manager import get_memory_manager
from core.config import get_config

logger = create_logger("AGENT_CORE")

class JARVISAgent:
    """Core JARVIS Agent"""
    
    def __init__(self):
        self.nlu = NLUEngine()
        self.planner = TaskPlanner()
        self.executor = TaskExecutor()
        self.reasoning = ReasoningEngine()
        self.decision_maker = DecisionMaker()
        self.memory = get_memory_manager()
        self.config = get_config()
        
        logger.info("JARVIS Agent initialized")
    
    def process_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input through agent pipeline"""
        try:
            # Record input
            input_time = datetime.now()
            logger.info(f"Processing input: {user_input}")
            
            # Stage 1: NLU
            nlu_result = self.nlu.process(user_input)
            
            if nlu_result.get('requires_clarification'):
                response = self._request_clarification(user_input, nlu_result)
                return response
            
            # Stage 2: Planning
            plan = self.planner.plan(
                nlu_result['intent'],
                nlu_result['entities'],
                nlu_result['context']
            )
            
            # Stage 3: Reasoning
            reasoning_result = self.reasoning.reason(plan, nlu_result)
            
            # Stage 4: Decision Making
            decision = self.decision_maker.decide(plan, reasoning_result)
            
            if decision.get('requires_confirmation'):
                response = self._request_confirmation(plan, decision)
                return response
            
            # Stage 5: Execution
            execution_result = self.executor.execute_plan(plan)
            
            # Prepare response
            response = {
                'success': execution_result.get('success', False),
                'nlu': nlu_result,
                'plan': plan,
                'execution_result': execution_result,
                'response': self._format_response(execution_result),
                'execution_time': (datetime.now() - input_time).total_seconds()
            }
            
            # Log to memory
            self.memory.record_event('input_processed', response)
            
            logger.info(f"Processed input in {response['execution_time']:.2f}s")
            return response
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            return {
                'success': False,
                'error': str(e),
                'response': 'متأسفانه خطایی رخ داد.'
            }
    
    def _request_clarification(self, user_input: str, nlu_result: Dict) -> Dict[str, Any]:
        """Request clarification from user"""
        logger.debug(f"Requesting clarification for: {user_input}")
        return {
            'success': False,
            'requires_clarification': True,
            'clarification_question': f'منظورت از "{user_input}" چیست؟',
            'possible_intents': list(nlu_result.get('scores', {}).keys())
        }
    
    def _request_confirmation(self, plan: Dict, decision: Dict) -> Dict[str, Any]:
        """Request confirmation for risky operations"""
        logger.debug(f"Requesting confirmation for plan: {plan['task_id']}")
        return {
            'success': False,
            'requires_confirmation': True,
            'confirmation_message': decision.get('message', 'آیا می‌خواهی ادامه دهم؟'),
            'task_id': plan['task_id'],
            'risky_steps': decision.get('risky_steps', [])
        }
    
    def _format_response(self, execution_result: Dict) -> str:
        """Format execution result into human-readable response"""
        if execution_result.get('success'):
            return execution_result.get('message', 'کار انجام شد.')
        else:
            return f"خطا: {execution_result.get('error', 'خطای نامشخص')}"
    
    def confirm_action(self, task_id: str, confirmed: bool) -> Dict[str, Any]:
        """Confirm or reject an action"""
        logger.debug(f"Action confirmation - Task: {task_id}, Confirmed: {confirmed}")
        # Implementation for handling confirmation
        return {'task_id': task_id, 'confirmed': confirmed}
