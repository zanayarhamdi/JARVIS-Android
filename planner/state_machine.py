from typing import Dict, List, Optional, Any
from enum import Enum
from core.logger import create_logger
from datetime import datetime

logger = create_logger("STATE_MACHINE")

class TaskState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    CANCELED = "canceled"

class StateMachine:
    """Manage task state transitions"""
    
    def __init__(self):
        self.valid_transitions = {
            TaskState.PENDING: [TaskState.RUNNING, TaskState.CANCELED],
            TaskState.RUNNING: [TaskState.COMPLETED, TaskState.FAILED, TaskState.PAUSED],
            TaskState.PAUSED: [TaskState.RUNNING, TaskState.CANCELED],
            TaskState.COMPLETED: [],
            TaskState.FAILED: [TaskState.PENDING],
            TaskState.CANCELED: []
        }
    
    def can_transition(self, current_state: TaskState, next_state: TaskState) -> bool:
        """Check if transition is valid"""
        return next_state in self.valid_transitions.get(current_state, [])
    
    def transition(self, current_state: TaskState, next_state: TaskState) -> bool:
        """Transition to new state"""
        if self.can_transition(current_state, next_state):
            logger.info(f"State transition: {current_state.value} -> {next_state.value}")
            return True
        else:
            logger.warning(f"Invalid transition: {current_state.value} -> {next_state.value}")
            return False
