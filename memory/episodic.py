import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from memory.persistence import get_database
from core.logger import create_logger
from core.config import get_config

logger = create_logger("EPISODIC_MEMORY")

class EpisodicMemory:
    """Event history - long-term storage of experiences"""
    
    def __init__(self):
        self.db = get_database()
        self.config = get_config()
    
    def store_event(self, event_type: str, content: Any, context: Optional[Dict] = None, importance: float = 1.0) -> int:
        """Store an event"""
        try:
            if isinstance(content, (dict, list)):
                content = json.dumps(content, ensure_ascii=False)
            else:
                content = str(content)
            
            context_str = json.dumps(context, ensure_ascii=False) if context else None
            
            record_id = self.db.insert(
                'episodic_memory',
                {
                    'event_type': event_type,
                    'content': content,
                    'context': context_str,
                    'importance': importance
                }
            )
            
            logger.debug(f"Stored episodic event: {event_type} (ID: {record_id})")
            return record_id
        except Exception as e:
            logger.error(f"Error storing episodic event: {e}")
            return -1
    
    def get_events(self, event_type: Optional[str] = None, limit: int = 100, days_back: int = 90) -> List[Dict]:
        """Retrieve events"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()
            
            if event_type:
                where = f'event_type = "{event_type}" AND timestamp > "{cutoff_date}"'
            else:
                where = f'timestamp > "{cutoff_date}"'
            
            records = self.db.select('episodic_memory', where=where, limit=limit)
            
            for record in records:
                try:
                    if record['content']:
                        record['content'] = json.loads(record['content'])
                except:
                    pass
                
                try:
                    if record['context']:
                        record['context'] = json.loads(record['context'])
                except:
                    pass
            
            return records
        except Exception as e:
            logger.error(f"Error retrieving episodic events: {e}")
            return []
    
    def get_recent_events(self, count: int = 10) -> List[Dict]:
        """Get most recent events"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=1)).isoformat()
            records = self.db.select(
                'episodic_memory',
                where=f'timestamp > "{cutoff_date}"',
                limit=count
            )
            
            for record in records:
                try:
                    if record['content']:
                        record['content'] = json.loads(record['content'])
                except:
                    pass
                
                try:
                    if record['context']:
                        record['context'] = json.loads(record['context'])
                except:
                    pass
            
            return records
        except Exception as e:
            logger.error(f"Error retrieving recent events: {e}")
            return []
    
    def search_events(self, keyword: str, limit: int = 50) -> List[Dict]:
        """Search events by keyword"""
        try:
            query = f'''
            SELECT * FROM episodic_memory 
            WHERE content LIKE '%{keyword}%' OR event_type LIKE '%{keyword}%'
            ORDER BY timestamp DESC
            LIMIT {limit}
            '''
            records = self.db.execute_custom(query)
            
            for record in records:
                try:
                    if record['content']:
                        record['content'] = json.loads(record['content'])
                except:
                    pass
                
                try:
                    if record['context']:
                        record['context'] = json.loads(record['context'])
                except:
                    pass
            
            return records
        except Exception as e:
            logger.error(f"Error searching events: {e}")
            return []
    
    def cleanup_old_events(self, days_to_keep: Optional[int] = None):
        """Remove events older than retention period"""
        try:
            if days_to_keep is None:
                days_to_keep = self.config.get('memory.episodic_retention_days', 90)
            
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).isoformat()
            
            self.db.delete(
                'episodic_memory',
                f'timestamp < "{cutoff_date}"'
            )
            
            logger.info(f"Cleaned up episodic events older than {days_to_keep} days")
        except Exception as e:
            logger.error(f"Error cleaning up old events: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get episodic memory statistics"""
        try:
            records = self.db.select('episodic_memory')
            event_types = {}
            
            for record in records:
                event_type = record['event_type']
                event_types[event_type] = event_types.get(event_type, 0) + 1
            
            return {
                'total_events': len(records),
                'event_types': event_types,
                'oldest_event': records[-1]['timestamp'] if records else None,
                'newest_event': records[0]['timestamp'] if records else None
            }
        except Exception as e:
            logger.error(f"Error getting episodic stats: {e}")
            return {}
