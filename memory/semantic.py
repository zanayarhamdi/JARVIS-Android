import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from memory.persistence import get_database
from core.logger import create_logger

logger = create_logger("SEMANTIC_MEMORY")

class SemanticMemory:
    """Knowledge base - concepts and their relationships"""
    
    def __init__(self):
        self.db = get_database()
    
    def store_concept(self, concept: str, data: Dict[str, Any], category: Optional[str] = None) -> bool:
        """Store a concept in semantic memory"""
        try:
            data_str = json.dumps(data, ensure_ascii=False)
            
            existing = self.db.select_one(
                'semantic_memory',
                f'concept = "{concept}"'
            )
            
            if existing:
                self.db.update(
                    'semantic_memory',
                    {
                        'data': data_str,
                        'category': category or existing['category'],
                        'updated_at': datetime.now().isoformat()
                    },
                    f'concept = "{concept}"'
                )
            else:
                self.db.insert(
                    'semantic_memory',
                    {
                        'concept': concept,
                        'data': data_str,
                        'category': category
                    }
                )
            
            logger.debug(f"Stored concept: {concept}")
            return True
        except Exception as e:
            logger.error(f"Error storing concept: {e}")
            return False
    
    def get_concept(self, concept: str) -> Optional[Dict[str, Any]]:
        """Retrieve a concept"""
        try:
            record = self.db.select_one(
                'semantic_memory',
                f'concept = "{concept}"'
            )
            
            if record:
                try:
                    return json.loads(record['data'])
                except:
                    return record['data']
            
            return None
        except Exception as e:
            logger.error(f"Error retrieving concept: {e}")
            return None
    
    def get_concepts_by_category(self, category: str) -> Dict[str, Any]:
        """Get all concepts in a category"""
        try:
            records = self.db.select(
                'semantic_memory',
                where=f'category = "{category}"'
            )
            
            result = {}
            for record in records:
                try:
                    result[record['concept']] = json.loads(record['data'])
                except:
                    result[record['concept']] = record['data']
            
            return result
        except Exception as e:
            logger.error(f"Error retrieving concepts by category: {e}")
            return {}
    
    def search_concepts(self, keyword: str) -> Dict[str, Any]:
        """Search concepts by keyword"""
        try:
            query = f'''
            SELECT * FROM semantic_memory 
            WHERE concept LIKE '%{keyword}%' OR data LIKE '%{keyword}%'
            '''
            records = self.db.execute_custom(query)
            
            result = {}
            for record in records:
                try:
                    result[record['concept']] = json.loads(record['data'])
                except:
                    result[record['concept']] = record['data']
            
            return result
        except Exception as e:
            logger.error(f"Error searching concepts: {e}")
            return {}
    
    def delete_concept(self, concept: str) -> bool:
        """Delete a concept"""
        try:
            self.db.delete('semantic_memory', f'concept = "{concept}"')
            logger.debug(f"Deleted concept: {concept}")
            return True
        except Exception as e:
            logger.error(f"Error deleting concept: {e}")
            return False
    
    def get_all_categories(self) -> List[str]:
        """Get all concept categories"""
        try:
            records = self.db.select('semantic_memory')
            categories = set()
            
            for record in records:
                if record['category']:
                    categories.add(record['category'])
            
            return sorted(list(categories))
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get semantic memory statistics"""
        try:
            records = self.db.select('semantic_memory')
            categories = {}
            
            for record in records:
                cat = record['category'] or 'uncategorized'
                categories[cat] = categories.get(cat, 0) + 1
            
            return {
                'total_concepts': len(records),
                'categories': categories
            }
        except Exception as e:
            logger.error(f"Error getting semantic stats: {e}")
            return {}
