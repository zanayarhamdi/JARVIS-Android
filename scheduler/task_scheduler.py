from typing import Dict, List, Optional, Any
from datetime import datetime
from core.logger import create_logger
from memory.memory_manager import get_memory_manager

logger = create_logger("SCHEDULER")

class TaskScheduler:
    """Schedule and manage tasks"""
    
    def __init__(self):
        self.scheduled_tasks: Dict[str, Dict] = {}
        self.memory = get_memory_manager()
    
    def schedule_task(
        self,
        task_name: str,
        task_func,
        schedule_time: Optional[str] = None,
        recurring: bool = False,
        interval_minutes: int = 60
    ) -> bool:
        """Schedule a task"""
        try:
            task = {
                'task_name': task_name,
                'task_func': task_func,
                'schedule_time': schedule_time,
                'recurring': recurring,
                'interval_minutes': interval_minutes,
                'created_at': datetime.now().isoformat(),
                'last_run': None,
                'next_run': schedule_time
            }
            
            self.scheduled_tasks[task_name] = task
            logger.info(f"Scheduled task: {task_name}")
            return True
        except Exception as e:
            logger.error(f"Error scheduling task: {e}")
            return False
    
    def get_scheduled_tasks(self) -> Dict[str, Dict]:
        """Get all scheduled tasks"""
        return self.scheduled_tasks.copy()
    
    def cancel_task(self, task_name: str) -> bool:
        """Cancel scheduled task"""
        try:
            if task_name in self.scheduled_tasks:
                del self.scheduled_tasks[task_name]
                logger.info(f"Canceled task: {task_name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error canceling task: {e}")
            return False
