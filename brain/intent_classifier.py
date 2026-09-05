from typing import Dict, List, Tuple, Optional, Any
from core.logger import create_logger

logger = create_logger("INTENT_CLASSIFIER")

class IntentClassifier:
    """Classify user intent"""
    
    def __init__(self):
        self.intent_patterns = {
            'file_operation': {
                'keywords': ['file', 'فایل', 'delete', 'حذف', 'rename', 'اسم', 'copy', 'کپی', 'move', 'جابه‌جا'],
                'patterns': [r'.*\b(file|فایل)\b.*', r'.*\b(delete|حذف)\b.*', r'.*\b(rename|اسم)\b.*'],
                'priority': 1
            },
            'system_info': {
                'keywords': ['status', 'وضعیت', 'info', 'اطلاعات', 'battery', 'باتری', 'storage', 'ذخیره'],
                'patterns': [r'.*\b(status|وضعیت)\b.*', r'.*\b(battery|باتری)\b.*'],
                'priority': 1
            },
            'code_generation': {
                'keywords': ['code', 'کد', 'script', 'اسکریپت', 'python', 'create', 'بساز'],
                'patterns': [r'.*\b(code|کد)\b.*', r'.*\b(script|اسکریپت)\b.*'],
                'priority': 1
            },
            'self_improvement': {
                'keywords': ['improve', 'بهبود', 'add', 'اضافه', 'feature', 'قابلیت', 'modify', 'تغییر'],
                'patterns': [r'.*\b(add|اضافه).*\b(feature|قابلیت)\b.*', r'.*\b(improve|بهبود)\b.*'],
                'priority': 2
            },
            'learning': {
                'keywords': ['learn', 'بیاموز', 'remember', 'یادبگیر', 'save', 'ذخیره'],
                'patterns': [r'.*\b(learn|بیاموز)\b.*', r'.*\b(remember|یادبگیر)\b.*'],
                'priority': 1
            },
            'conversation': {
                'keywords': ['hello', 'سلام', 'hi', 'bye', 'خدا', 'thanks', 'متشکرم'],
                'patterns': [r'.*\b(hello|سلام)\b.*', r'.*\b(bye|خدا)\b.*'],
                'priority': 0
            },
            'execution': {
                'keywords': ['run', 'اجرا', 'execute', 'command', 'دستور'],
                'patterns': [r'.*\b(run|اجرا)\b.*', r'.*\b(execute|command|دستور)\b.*'],
                'priority': 1
            }
        }
    
    def classify(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Classify user intent"""
        try:
            text_lower = text.lower()
            scores = {}
            
            for intent, config in self.intent_patterns.items():
                score = self._calculate_intent_score(text_lower, config)
                scores[intent] = score
            
            # Get top intent
            top_intent = max(scores, key=scores.get)
            confidence = min(scores[top_intent], 1.0)
            
            logger.debug(f"Classified intent: {top_intent} (confidence: {confidence})")
            
            return {
                'intent': top_intent,
                'confidence': confidence,
                'scores': scores
            }
        except Exception as e:
            logger.error(f"Error classifying intent: {e}")
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'scores': {}
            }
    
    def _calculate_intent_score(self, text: str, config: Dict) -> float:
        """Calculate score for intent"""
        import re
        
        score = 0.0
        max_score = 0.0
        
        # Check patterns
        for pattern in config.get('patterns', []):
            max_score += 0.4
            if re.search(pattern, text):
                score += 0.4
        
        # Check keywords
        keywords = config.get('keywords', [])
        keyword_weight = 0.6 / max(len(keywords), 1)
        for keyword in keywords:
            max_score += keyword_weight
            if keyword in text:
                score += keyword_weight
        
        return score / max(max_score, 1)
