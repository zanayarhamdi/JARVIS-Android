import re
from typing import Dict, List, Optional, Tuple, Any
from brain.intent_classifier import IntentClassifier
from brain.entity_extractor import EntityExtractor
from brain.semantic_parser import SemanticParser
from brain.context_tracker import ContextTracker
from memory.memory_manager import get_memory_manager
from core.logger import create_logger

logger = create_logger("NLU")

class NLUEngine:
    """Natural Language Understanding Engine"""
    
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.entity_extractor = EntityExtractor()
        self.semantic_parser = SemanticParser()
        self.context_tracker = ContextTracker()
        self.memory = get_memory_manager()
    
    def process(self, user_input: str) -> Dict[str, Any]:
        """Process user input and extract understanding"""
        try:
            # Clean input
            cleaned_input = self._clean_input(user_input)
            
            # Get conversation context
            context = self.context_tracker.get_current_context()
            
            # Classify intent
            intent_result = self.intent_classifier.classify(cleaned_input, context)
            
            # Extract entities
            entities = self.entity_extractor.extract(cleaned_input, intent_result['intent'])
            
            # Parse semantics
            semantic = self.semantic_parser.parse(cleaned_input, intent_result['intent'], entities)
            
            # Update context
            self.context_tracker.update(user_input, intent_result['intent'], entities)
            
            # Log to memory
            self.memory.record_event(
                'user_input_processed',
                {
                    'input': user_input,
                    'cleaned_input': cleaned_input,
                    'intent': intent_result['intent'],
                    'confidence': intent_result['confidence'],
                    'entities': entities
                }
            )
            
            result = {
                'original_input': user_input,
                'cleaned_input': cleaned_input,
                'intent': intent_result['intent'],
                'intent_confidence': intent_result['confidence'],
                'entities': entities,
                'semantic': semantic,
                'context': context,
                'requires_clarification': intent_result['confidence'] < 0.5
            }
            
            logger.debug(f"Processed input: {result['intent']} (confidence: {result['intent_confidence']})")
            return result
        except Exception as e:
            logger.error(f"Error processing NLU: {e}")
            return {
                'original_input': user_input,
                'intent': 'unknown',
                'intent_confidence': 0.0,
                'entities': [],
                'semantic': {},
                'error': str(e),
                'requires_clarification': True
            }
    
    def _clean_input(self, text: str) -> str:
        """Clean and normalize input text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Convert to lowercase for processing
        text = text.lower()
        return text
    
    def get_similar_learned_commands(self, user_input: str, threshold: float = 0.7) -> List[Dict]:
        """Find similar learned commands"""
        try:
            from difflib import SequenceMatcher
            
            learned_skills = self.memory.get_all_learned_skills()
            similar = []
            
            for skill in learned_skills:
                ratio = SequenceMatcher(None, user_input.lower(), skill['skill_name'].lower()).ratio()
                if ratio >= threshold:
                    similar.append({
                        'skill_name': skill['skill_name'],
                        'similarity': ratio,
                        'confidence': skill['confidence']
                    })
            
            return sorted(similar, key=lambda x: x['similarity'], reverse=True)
        except Exception as e:
            logger.error(f"Error finding similar commands: {e}")
            return []
