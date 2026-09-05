import unittest
from memory.memory_manager import get_memory_manager
from memory.short_term import ShortTermMemory
from memory.episodic import EpisodicMemory
from memory.semantic import SemanticMemory

class TestMemory(unittest.TestCase):
    
    def setUp(self):
        self.memory = get_memory_manager()
        self.short_term = ShortTermMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
    
    def test_short_term_memory(self):
        """Test short-term memory storage"""
        self.short_term.store('test_key', 'test_value', ttl_seconds=3600)
        value = self.short_term.retrieve('test_key')
        self.assertEqual(value, 'test_value')
    
    def test_episodic_memory(self):
        """Test episodic memory"""
        event_id = self.episodic.store_event('test_event', {'data': 'test'})
        self.assertGreater(event_id, 0)
    
    def test_semantic_memory(self):
        """Test semantic memory"""
        self.semantic.store_concept('test_concept', {'definition': 'test'}, 'test_category')
        concept = self.semantic.get_concept('test_concept')
        self.assertIsNotNone(concept)
    
    def test_memory_manager(self):
        """Test memory manager orchestration"""
        self.memory.remember_temporary('key1', 'value1')
        self.assertEqual(self.memory.recall_temporary('key1'), 'value1')

if __name__ == '__main__':
    unittest.main()
