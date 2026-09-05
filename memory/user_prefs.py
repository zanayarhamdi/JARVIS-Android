import json
from typing import Any, Dict, List, Optional
from memory.persistence import get_database
from core.logger import create_logger

logger = create_logger("USER_PREFS")

class UserPreferences:
    """Store user preferences and settings"""
    
    def __init__(self):
        self.db = get_database()
    
    def set_preference(self, key: str, value: Any, data_type: Optional[str] = None) -> bool:
        """Set a user preference"""
        try:
            if data_type is None:
                if isinstance(value, bool):
                    data_type = 'boolean'
                elif isinstance(value, int):
                    data_type = 'integer'
                elif isinstance(value, float):
                    data_type = 'float'
                elif isinstance(value, (dict, list)):
                    data_type = 'json'
                else:
                    data_type = 'string'
            
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            else:
                value = str(value)
            
            existing = self.db.select_one(
                'user_preferences',
                f'key = "{key}"'
            )
            
            if existing:
                self.db.update(
                    'user_preferences',
                    {'value': value, 'data_type': data_type},
                    f'key = "{key}"'
                )
            else:
                self.db.insert(
                    'user_preferences',
                    {
                        'key': key,
                        'value': value,
                        'data_type': data_type
                    }
                )
            
            logger.debug(f"Set preference: {key} = {value}")
            return True
        except Exception as e:
            logger.error(f"Error setting preference: {e}")
            return False
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference"""
        try:
            record = self.db.select_one(
                'user_preferences',
                f'key = "{key}"'
            )
            
            if not record:
                return default
            
            value = record['value']
            data_type = record.get('data_type', 'string')
            
            if data_type == 'boolean':
                return value.lower() in ('true', '1', 'yes')
            elif data_type == 'integer':
                return int(value)
            elif data_type == 'float':
                return float(value)
            elif data_type == 'json':
                try:
                    return json.loads(value)
                except:
                    return value
            else:
                return value
        except Exception as e:
            logger.error(f"Error getting preference: {e}")
            return default
    
    def get_all_preferences(self) -> Dict[str, Any]:
        """Get all user preferences"""
        try:
            records = self.db.select('user_preferences')
            result = {}
            
            for record in records:
                key = record['key']
                value = record['value']
                data_type = record.get('data_type', 'string')
                
                if data_type == 'boolean':
                    result[key] = value.lower() in ('true', '1', 'yes')
                elif data_type == 'integer':
                    result[key] = int(value)
                elif data_type == 'float':
                    result[key] = float(value)
                elif data_type == 'json':
                    try:
                        result[key] = json.loads(value)
                    except:
                        result[key] = value
                else:
                    result[key] = value
            
            return result
        except Exception as e:
            logger.error(f"Error getting all preferences: {e}")
            return {}
    
    def delete_preference(self, key: str) -> bool:
        """Delete a user preference"""
        try:
            self.db.delete('user_preferences', f'key = "{key}"')
            logger.debug(f"Deleted preference: {key}")
            return True
        except Exception as e:
            logger.error(f"Error deleting preference: {e}")
            return False
    
    def has_preference(self, key: str) -> bool:
        """Check if preference exists"""
        try:
            record = self.db.select_one(
                'user_preferences',
                f'key = "{key}"'
            )
            return record is not None
        except Exception as e:
            logger.error(f"Error checking preference: {e}")
            return False
