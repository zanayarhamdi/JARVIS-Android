import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from memory.persistence import get_database
from core.logger import create_logger

logger = create_logger("SHORT_TERM_MEMORY")

class ShortTermMemory:
    """Working memory - fast access, limited duration"""
    
    def __init__(self, max_size=100):
        self.db = get_database()
        self.max_size = max_size
        self.memory_dict = {}  # In-memory cache
    
    def store(self, key: str, value: Any, ttl_seconds: Optional[int] = 3600):
        """Store value in short-term memory"""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            else:
                value = str(value)
            
            # Store in database
            existing = self.db.select_one(
                'short_term_memory',
                f'key = "{key}"'
            )
            
            if existing:
                self.db.update(
                    'short_term_memory',
                    {'value': value, 'timestamp': datetime.now().isoformat(), 'ttl_seconds': ttl_seconds},
                    f'key = "{key}"'
                )
            else:
                self.db.insert(
                    'short_term_memory',
                    {
                        'key': key,
                        'value': value,
                        'ttl_seconds': ttl_seconds
                    }
                )
            
            # Store in memory cache
            self.memory_dict[key] = {
                'value': value,
                'timestamp': datetime.now(),
                'ttl_seconds': ttl_seconds
            }
            
            logger.debug(f"Stored in short-term memory: {key}")
        except Exception as e:
            logger.error(f"Error storing in short-term memory: {e}")
    
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve value from short-term memory"""
        try:
            # Check memory cache first
            if key in self.memory_dict:
                cached = self.memory_dict[key]
                if cached['ttl_seconds']:
                    elapsed = (datetime.now() - cached['timestamp']).total_seconds()
                    if elapsed > cached['ttl_seconds']:
                        self.delete(key)
                        return None
                
                value = cached['value']
                try:
                    return json.loads(value)
                except:
                    return value
            
            # Check database
            record = self.db.select_one(
                'short_term_memory',
                f'key = "{key}"'
            )
            
            if record:
                if record['ttl_seconds']:
                    created = datetime.fromisoformat(record['timestamp'])
                    elapsed = (datetime.now() - created).total_seconds()
                    if elapsed > record['ttl_seconds']:
                        self.delete(key)
                        return None
                
                value = record['value']
                try:
                    return json.loads(value)
                except:
                    return value
            
            return None
        except Exception as e:
            logger.error(f"Error retrieving from short-term memory: {e}")
            return None
    
    def delete(self, key: str):
        """Delete value from short-term memory"""
        try:
            self.db.delete('short_term_memory', f'key = "{key}"')
            if key in self.memory_dict:
                del self.memory_dict[key]
            logger.debug(f"Deleted from short-term memory: {key}")
        except Exception as e:
            logger.error(f"Error deleting from short-term memory: {e}")
    
    def clear_expired(self):
        """Clear expired entries"""
        try:
            records = self.db.select('short_term_memory')
            deleted_count = 0
            
            for record in records:
                if record['ttl_seconds']:
                    created = datetime.fromisoformat(record['timestamp'])
                    elapsed = (datetime.now() - created).total_seconds()
                    if elapsed > record['ttl_seconds']:
                        self.delete(record['key'])
                        deleted_count += 1
            
            logger.debug(f"Cleared {deleted_count} expired short-term memory entries")
        except Exception as e:
            logger.error(f"Error clearing expired entries: {e}")
    
    def get_all(self) -> Dict[str, Any]:
        """Get all non-expired entries"""
        try:
            self.clear_expired()
            records = self.db.select('short_term_memory')
            result = {}
            
            for record in records:
                value = record['value']
                try:
                    result[record['key']] = json.loads(value)
                except:
                    result[record['key']] = value
            
            return result
        except Exception as e:
            logger.error(f"Error getting all short-term memory: {e}")
            return {}
    
    def size(self) -> int:
        """Get current size of short-term memory"""
        try:
            self.clear_expired()
            records = self.db.select('short_term_memory')
            return len(records)
        except Exception as e:
            logger.error(f"Error getting short-term memory size: {e}")
            return 0
