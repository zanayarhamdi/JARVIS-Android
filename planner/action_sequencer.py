from typing import Dict, List, Any, Optional
from core.logger import create_logger

logger = create_logger("ACTION_SEQUENCER")

class ActionSequencer:
    """Sequence and order actions"""
    
    def __init__(self):
        self.action_dependencies = {
            'backup_system': [],
            'analyze_requirements': [],
            'generate_code': ['analyze_requirements'],
            'syntax_check': ['generate_code'],
            'create_file': ['syntax_check'],
            'test_changes': ['apply_changes'],
            'apply_changes': ['generate_changes'],
            'generate_changes': ['analyze_improvement']
        }
    
    def sequence(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Order steps respecting dependencies"""
        try:
            # Sort by dependencies
            sequenced = self._topological_sort(steps)
            
            logger.debug(f"Sequenced {len(sequenced)} actions")
            return sequenced
        except Exception as e:
            logger.error(f"Error sequencing actions: {e}")
            return steps
    
    def _topological_sort(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Topological sort of steps"""
        from collections import deque
        
        # Build dependency graph
        graph = {}
        in_degree = {}
        
        for step in steps:
            action = step['action']
            graph[action] = self.action_dependencies.get(action, [])
            in_degree[action] = 0
        
        for action in graph:
            for dep in graph[action]:
                if dep not in in_degree:
                    in_degree[dep] = 0
                in_degree[dep] += 1
        
        # Kahn's algorithm
        queue = deque([action for action in in_degree if in_degree[action] == 0])
        sorted_actions = []
        
        while queue:
            action = queue.popleft()
            sorted_actions.append(action)
            
            for dep in graph.get(action, []):
                in_degree[dep] -= 1
                if in_degree[dep] == 0:
                    queue.append(dep)
        
        # Map back to steps
        action_to_step = {step['action']: step for step in steps}
        return [action_to_step[action] for action in sorted_actions if action in action_to_step]
