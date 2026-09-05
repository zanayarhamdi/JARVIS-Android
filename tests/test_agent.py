import unittest
from agent.agent_core import JARVISAgent
from agent.reasoning import ReasoningEngine
from agent.decision_maker import DecisionMaker

class TestAgent(unittest.TestCase):
    
    def setUp(self):
        self.agent = JARVISAgent()
        self.reasoning = ReasoningEngine()
        self.decision_maker = DecisionMaker()
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        self.assertIsNotNone(self.agent.nlu)
        self.assertIsNotNone(self.agent.planner)
        self.assertIsNotNone(self.agent.executor)
    
    def test_reasoning(self):
        """Test reasoning engine"""
        plan = {'task_id': '123', 'intent': 'file_operation', 'steps': []}
        reasoning = self.reasoning.reason(plan, {})
        self.assertIsNotNone(reasoning.get('feasible'))
    
    def test_decision_making(self):
        """Test decision making"""
        plan = {'task_id': '123', 'intent': 'file_operation', 'steps': []}
        reasoning = {'feasible': True, 'confidence': 0.9, 'risks': []}
        decision = self.decision_maker.decide(plan, reasoning)
        self.assertTrue(decision.get('execute'))

if __name__ == '__main__':
    unittest.main()
