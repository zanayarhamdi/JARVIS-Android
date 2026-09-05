import unittest
from brain.nlu import NLUEngine
from brain.intent_classifier import IntentClassifier

class TestNLU(unittest.TestCase):
    
    def setUp(self):
        self.nlu = NLUEngine()
        self.classifier = IntentClassifier()
    
    def test_intent_classification(self):
        """Test intent classification"""
        result = self.classifier.classify("یک فایل Python بساز")
        self.assertIn(result['intent'], ['code_generation', 'file_operation'])
    
    def test_nlu_processing(self):
        """Test NLU processing"""
        result = self.nlu.process("فایل‌ها رو حذف کن")
        self.assertIsNotNone(result.get('intent'))
        self.assertIn('entities', result)
    
    def test_context_tracking(self):
        """Test context tracking"""
        self.nlu.process("یک فایل بساز")
        context = self.nlu.context_tracker.get_current_context()
        self.assertIsNotNone(context)

if __name__ == '__main__':
    unittest.main()
