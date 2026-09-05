from typing import Dict, List, Optional
from datetime import datetime
from memory.persistence import get_database
from core.logger import create_logger

logger = create_logger("AUDIT_LOG")

class AuditLog:
    """Audit log for security tracking"""
    
    def __init__(self):
        self.db = get_database()
    
    def log_action(
        self,
        action: str,
        actor: str,
        resource: str,
        status: str,
        details: Optional[Dict] = None
    ) -> bool:
        """Log an action"""
        try:
            details_str = str(details) if details else ""
            
            self.db.insert(
                'audit_log',
                {
                    'action': action,
                    'actor': actor,
                    'resource': resource,
                    'status': status,
                    'details': details_str,
                    'timestamp': datetime.now().isoformat()
                }
            )
            
            logger.info(f"Audit log: {actor} {action} {resource} [{status}]")
            return True
        except Exception as e:
            logger.error(f"Error logging action: {e}")
            return False
    
    def get_logs(
        self,
        action: Optional[str] = None,
        actor: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Get audit logs"""
        try:
            where_clause = ""
            if action:
                where_clause += f'action = "{action}"'
            if actor:
                if where_clause:
                    where_clause += " AND "
                where_clause += f'actor = "{actor}"'
            
            logs = self.db.select('audit_log', where=where_clause if where_clause else None, limit=limit)
            return logs
        except Exception as e:
            logger.error(f"Error getting audit logs: {e}")
            return []
