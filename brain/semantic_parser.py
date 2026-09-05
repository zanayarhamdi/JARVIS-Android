from typing import Dict, List, Optional, Any
from core.logger import create_logger

logger = create_logger("SEMANTIC_PARSER")

class SemanticParser:
    """Parse semantic meaning and relationships"""
    
    def __init__(self):
        pass
    
    def parse(self, text: str, intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Parse semantic meaning"""
        try:
            semantic = {
                'intent': intent,
                'entities': entities,
                'relationships': self._extract_relationships(text, entities),
                'modifiers': self._extract_modifiers(text),
                'tense': self._detect_tense(text),
                'subject': self._extract_subject(text),
                'object': self._extract_object(text)
            }
            
            logger.debug(f"Parsed semantic: {semantic}")
            return semantic
        except Exception as e:
            logger.error(f"Error parsing semantic: {e}")
            return {}
    
    def _extract_relationships(self, text: str, entities: Dict) -> List[Dict[str, str]]:
        """Extract relationships between entities"""
        relationships = []
        
        # Simple relationship extraction
        if 'operation' in entities and 'source' in entities:
            relationships.append({
                'type': 'action_on_object',
                'action': entities['operation'][0] if entities['operation'] else None,
                'object': entities['source'][0] if entities['source'] else None
            })
        
        return relationships
    
    def _extract_modifiers(self, text: str) -> List[str]:
        """Extract modifiers and adverbs"""
        modifiers = []
        modifier_words = ['carefully', 'احتیاط', 'quickly', 'سریع', 'silently', 'بدون', 'forcefully', 'مجبور']
        
        for modifier in modifier_words:
            if modifier in text.lower():
                modifiers.append(modifier)
        
        return modifiers
    
    def _detect_tense(self, text: str) -> str:
        """Detect tense (past, present, future)"""
        if any(word in text.lower() for word in ['will', 'خواهم', 'gonna', 'باید']):
            return 'future'
        elif any(word in text.lower() for word in ['did', 'was', 'کردم', 'بود']):
            return 'past'
        else:
            return 'present'
    
    def _extract_subject(self, text: str) -> Optional[str]:
        """Extract subject"""
        # Simple subject extraction
        pronouns = ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'من', 'تو', 'او', 'ما', 'شما']
        for pronoun in pronouns:
            if text.lower().startswith(pronoun):
                return pronoun
        return 'user'
    
    def _extract_object(self, text: str) -> Optional[str]:
        """Extract object"""
        # Simple object extraction - usually comes after verb
        words = text.lower().split()
        action_words = ['delete', 'create', 'modify', 'run', 'حذف', 'بساز', 'تغییر', 'اجرا']
        
        for i, word in enumerate(words):
            if word in action_words and i + 1 < len(words):
                return ' '.join(words[i+1:i+3])
        
        return None
