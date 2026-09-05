from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from memory.memory_manager import get_memory_manager
from core.logger import create_logger

logger = create_logger("CONTEXT_TRACKER")

class ContextTracker:
    """Track conversation context"""
    
    def __init__(self, context_window: int = 10):
        self.context_window = context_window
        self.memory = get_memory_manager()
        self.current_context = {}
    
    def get_current_context(self) -> Dict[str, Any]:
        """Get current conversation context"""
        try:
            # Get recent conversation history
            recent_events = self.memory.recall_recent_events(self.context_window)
            
            context = {
                'current_task': self.current_context.get('current_task'),
                'previous_inputs': [e.get('content') for e in recent_events if 'input' in str(e)],
                'previous_actions': [e.get('content') for e in recent_events if 'action' in str(e)],
                'timestamp': datetime.now().isoformat()
            }
            
            return context
        except Exception as e:
            logger.error(f"Error getting context: {e}")
            return {}
    
    def update(self, user_input: str, intent: str, entities: Dict):
        """Update context with new information"""
        try:
            self.current_context = {
                'last_input': user_input,
                'last_intent': intent,
                'last_entities': entities,
                'timestamp': datetime.now().isoformat()
            }
            
            # Update task context if applicable
            if intent == 'self_improvement' or intent == 'code_generation':
                self.current_context['current_task'] = {
                    'type': intent,
                    'started_at': datetime.now().isoformat(),
                    'entities': entities
                }
            
            logger.debug(f"Updated context: {intent}")
        except Exception as e:
            logger.error(f"Error updating context: {e}")
    
    def get_task_context(self) -> Optional[Dict]:
        """Get current task context"""
        return self.current_context.get('current_task')
    
    def clear_task_context(self):
        """Clear current task context"""
        if 'current_task' in self.current_context:
            del self.current_context['current_task']
            logger.debug("Cleared task context")
    
    def get_reference_context(self, reference: str) -> Optional[Dict]:
        """Resolve references like 'that file', 'previous command'"""
        references_map = {
            'that file': 'last_entities.get("filepath")',
            'that script': 'last_entities.get("filename")',
            'previous command': 'last_input',
            'last action': 'last_action',
            'current task': 'current_task'
        }
        
        reference_lower = reference.lower()
        for key in references_map:
            if key in reference_lower:
                return self.current_context
        
        return None
