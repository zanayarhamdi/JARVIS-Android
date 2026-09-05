from typing import Any, Dict, List, Optional
from memory.short_term import ShortTermMemory
from memory.episodic import EpisodicMemory
from memory.semantic import SemanticMemory
from memory.user_prefs import UserPreferences
from memory.learned_skills import LearnedSkills
from core.logger import create_logger

logger = create_logger("MEMORY_MANAGER")

class MemoryManager:
    """Orchestrate all memory systems"""
    
    def __init__(self):
        self.short_term = ShortTermMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.user_prefs = UserPreferences()
        self.learned_skills = LearnedSkills()
        logger.info("Memory manager initialized")
    
    # Short-term memory operations
    def remember_temporary(self, key: str, value: Any, ttl_seconds: int = 3600):
        """Store temporary value"""
        self.short_term.store(key, value, ttl_seconds)
    
    def recall_temporary(self, key: str) -> Optional[Any]:
        """Retrieve temporary value"""
        return self.short_term.retrieve(key)
    
    def forget_temporary(self, key: str):
        """Forget temporary value"""
        self.short_term.delete(key)
    
    # Episodic memory operations
    def record_event(self, event_type: str, content: Any, context: Optional[Dict] = None, importance: float = 1.0) -> int:
        """Record an event"""
        return self.episodic.store_event(event_type, content, context, importance)
    
    def recall_events(self, event_type: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Recall events"""
        return self.episodic.get_events(event_type, limit)
    
    def recall_recent_events(self, count: int = 10) -> List[Dict]:
        """Recall recent events"""
        return self.episodic.get_recent_events(count)
    
    def search_events(self, keyword: str, limit: int = 50) -> List[Dict]:
        """Search events"""
        return self.episodic.search_events(keyword, limit)
    
    # Semantic memory operations
    def learn_concept(self, concept: str, data: Dict[str, Any], category: Optional[str] = None) -> bool:
        """Learn a concept"""
        return self.semantic.store_concept(concept, data, category)
    
    def recall_concept(self, concept: str) -> Optional[Dict[str, Any]]:
        """Recall a concept"""
        return self.semantic.get_concept(concept)
    
    def search_knowledge(self, keyword: str) -> Dict[str, Any]:
        """Search knowledge base"""
        return self.semantic.search_concepts(keyword)
    
    def get_knowledge_by_category(self, category: str) -> Dict[str, Any]:
        """Get knowledge by category"""
        return self.semantic.get_concepts_by_category(category)
    
    # User preferences operations
    def set_user_preference(self, key: str, value: Any) -> bool:
        """Set user preference"""
        return self.user_prefs.set_preference(key, value)
    
    def get_user_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference"""
        return self.user_prefs.get_preference(key, default)
    
    def get_all_user_preferences(self) -> Dict[str, Any]:
        """Get all user preferences"""
        return self.user_prefs.get_all_preferences()
    
    # Learned skills operations
    def register_learned_skill(self, skill_name: str, description: str, implementation: str) -> bool:
        """Register learned skill"""
        return self.learned_skills.register_skill(skill_name, description, implementation)
    
    def recall_skill(self, skill_name: str) -> Optional[str]:
        """Recall skill implementation"""
        return self.learned_skills.execute_skill(skill_name)
    
    def get_all_learned_skills(self) -> List[Dict[str, Any]]:
        """Get all learned skills"""
        return self.learned_skills.get_all_skills()
    
    def mark_skill_success(self, skill_name: str):
        """Mark skill execution as successful"""
        self.learned_skills.log_skill_success(skill_name)
    
    def mark_skill_failure(self, skill_name: str):
        """Mark skill execution as failed"""
        self.learned_skills.log_skill_failure(skill_name)
    
    def get_high_confidence_skills(self, min_confidence: float = 0.7) -> List[Dict[str, Any]]:
        """Get reliable learned skills"""
        return self.learned_skills.get_skills_by_confidence(min_confidence)
    
    # Memory statistics
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics"""
        return {
            'short_term': {
                'size': self.short_term.size(),
                'entries': self.short_term.get_all()
            },
            'episodic': self.episodic.get_stats(),
            'semantic': self.semantic.get_stats(),
            'learned_skills': self.learned_skills.get_stats(),
            'user_preferences': len(self.user_prefs.get_all_preferences())
        }


# Global memory manager instance
_memory_manager_instance = None

def get_memory_manager() -> MemoryManager:
    global _memory_manager_instance
    if _memory_manager_instance is None:
        _memory_manager_instance = MemoryManager()
    return _memory_manager_instance
