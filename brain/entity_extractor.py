import re
from typing import Dict, List, Optional, Any
from core.logger import create_logger

logger = create_logger("ENTITY_EXTRACTOR")

class EntityExtractor:
    """Extract named entities and parameters from text"""
    
    def __init__(self):
        self.entity_patterns = {
            'filepath': r'(\/[\w\/.-]*|~[\/\w.-]*|\.[\/\w.-]*)',
            'filename': r'[\w.-]+\.(py|txt|json|sh|java|cpp|js|ts)',
            'directory': r'(desktop|downloads|documents|pictures|music|videos|home|data)',
            'number': r'\b\d+\b',
            'email': r'[\w.-]+@[\w.-]+',
            'url': r'https?:\/\/[\S]+',
            'command': r'(run|execute|create|delete|rename|copy|move)\s+([\w\s.-]+)',
            'target': r'(?:to|in|from|at)\s+([\w\/\.-]+)'
        }
    
    def extract(self, text: str, intent: Optional[str] = None) -> Dict[str, List[Any]]:
        """Extract entities from text"""
        try:
            entities = {}
            
            # Extract all entity types
            for entity_type, pattern in self.entity_patterns.items():
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    # Flatten if pattern returns tuples
                    if isinstance(matches[0], tuple):
                        matches = [m for match in matches for m in match if m]
                    entities[entity_type] = matches
            
            # Intent-specific extraction
            if intent == 'file_operation':
                entities = self._extract_file_operation_entities(text, entities)
            elif intent == 'code_generation':
                entities = self._extract_code_generation_entities(text, entities)
            
            logger.debug(f"Extracted entities: {entities}")
            return entities
        except Exception as e:
            logger.error(f"Error extracting entities: {e}")
            return {}
    
    def _extract_file_operation_entities(self, text: str, entities: Dict) -> Dict:
        """Extract file operation specific entities"""
        # Extract operation type
        operations = ['delete', 'rename', 'copy', 'move', 'create', 'modify']
        for op in operations:
            if op in text.lower():
                entities['operation'] = [op]
                break
        
        # Extract source and destination
        source_match = re.search(r'(?:from|in|at)\s+([\w\/\.-]+)', text)
        if source_match:
            entities['source'] = [source_match.group(1)]
        
        dest_match = re.search(r'(?:to|into)\s+([\w\/\.-]+)', text)
        if dest_match:
            entities['destination'] = [dest_match.group(1)]
        
        return entities
    
    def _extract_code_generation_entities(self, text: str, entities: Dict) -> Dict:
        """Extract code generation specific entities"""
        # Extract language
        languages = ['python', 'java', 'cpp', 'javascript', 'typescript']
        for lang in languages:
            if lang in text.lower():
                entities['language'] = [lang]
                break
        
        # Extract description
        desc_match = re.search(r'(?:that|which)\s+([^.!?]+)', text)
        if desc_match:
            entities['description'] = [desc_match.group(1)]
        
        return entities
