import unittest
from planner.task_planner import TaskPlanner
from planner.state_machine import StateMachine, TaskState

class TestPlanner(unittest.TestCase):
    
    def setUp(self):
        self.planner = TaskPlanner()
        self.state_machine = StateMachine()
    
    def test_file_operation_planning(self):
        """Test file operation planning"""
        entities = {'operation': ['delete'], 'source': ['/test/file.txt']}
        plan = self.planner.plan('file_operation', entities)
        self.assertIsNotNone(plan.get('task_id'))
        self.assertGreater(len(plan.get('steps', [])), 0)
    
    def test_code_generation_planning(self):
        """Test code generation planning"""
        entities = {'language': ['python'], 'description': ['sort files']}
        plan = self.planner.plan('code_generation', entities)
        self.assertGreater(len(plan.get('steps', [])), 0)
    
    def test_state_transitions(self):
        """Test valid state transitions"""
        self.assertTrue(
            self.state_machine.can_transition(TaskState.PENDING, TaskState.RUNNING)
        )
        self.assertFalse(
            self.state_machine.can_transition(TaskState.COMPLETED, TaskState.RUNNING)
        )

if __name__ == '__main__':
    unittest.main()
