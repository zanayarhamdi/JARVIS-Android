import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from memory.persistence import get_database
from core.logger import create_logger

logger = create_logger("LEARNED_SKILLS")

class LearnedSkills:
    """Store and manage learned skills"""
    
    def __init__(self):
        self.db = get_database()
    
    def register_skill(self, skill_name: str, description: str, implementation: str) -> bool:
        """Register a new learned skill"""
        try:
            existing = self.db.select_one(
                'learned_skills',
                f'skill_name = "{skill_name}"'
            )
            
            if existing:
                logger.warning(f"Skill already exists: {skill_name}")
                return False
            
            self.db.insert(
                'learned_skills',
                {
                    'skill_name': skill_name,
                    'description': description,
                    'implementation': implementation,
                    'success_count': 0,
                    'failure_count': 0,
                    'confidence': 0.5
                }
            )
            
            logger.info(f"Registered skill: {skill_name}")
            return True
        except Exception as e:
            logger.error(f"Error registering skill: {e}")
            return False
    
    def get_skill(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve a skill"""
        try:
            record = self.db.select_one(
                'learned_skills',
                f'skill_name = "{skill_name}"'
            )
            
            if record:
                return record
            
            return None
        except Exception as e:
            logger.error(f"Error retrieving skill: {e}")
            return None
    
    def execute_skill(self, skill_name: str) -> Optional[str]:
        """Get skill implementation for execution"""
        try:
            skill = self.get_skill(skill_name)
            if skill:
                return skill['implementation']
            return None
        except Exception as e:
            logger.error(f"Error getting skill implementation: {e}")
            return None
    
    def log_skill_success(self, skill_name: str):
        """Log successful skill execution"""
        try:
            skill = self.get_skill(skill_name)
            if skill:
                total = skill['success_count'] + skill['failure_count'] + 1
                success_rate = skill['success_count'] + 1 / total
                
                self.db.update(
                    'learned_skills',
                    {
                        'success_count': skill['success_count'] + 1,
                        'confidence': success_rate,
                        'last_used': datetime.now().isoformat()
                    },
                    f'skill_name = "{skill_name}"'
                )
                logger.debug(f"Logged success for skill: {skill_name}")
        except Exception as e:
            logger.error(f"Error logging skill success: {e}")
    
    def log_skill_failure(self, skill_name: str):
        """Log failed skill execution"""
        try:
            skill = self.get_skill(skill_name)
            if skill:
                total = skill['success_count'] + skill['failure_count'] + 1
                success_rate = skill['success_count'] / total if total > 0 else 0
                
                self.db.update(
                    'learned_skills',
                    {
                        'failure_count': skill['failure_count'] + 1,
                        'confidence': success_rate,
                        'last_used': datetime.now().isoformat()
                    },
                    f'skill_name = "{skill_name}"'
                )
                logger.debug(f"Logged failure for skill: {skill_name}")
        except Exception as e:
            logger.error(f"Error logging skill failure: {e}")
    
    def get_all_skills(self) -> List[Dict[str, Any]]:
        """Get all learned skills"""
        try:
            records = self.db.select('learned_skills')
            return records
        except Exception as e:
            logger.error(f"Error retrieving all skills: {e}")
            return []
    
    def get_skills_by_confidence(self, min_confidence: float = 0.7) -> List[Dict[str, Any]]:
        """Get skills with confidence above threshold"""
        try:
            records = self.db.select('learned_skills')
            filtered = [r for r in records if r['confidence'] >= min_confidence]
            return sorted(filtered, key=lambda x: x['confidence'], reverse=True)
        except Exception as e:
            logger.error(f"Error getting skills by confidence: {e}")
            return []
    
    def delete_skill(self, skill_name: str) -> bool:
        """Delete a learned skill"""
        try:
            self.db.delete('learned_skills', f'skill_name = "{skill_name}"')
            logger.info(f"Deleted skill: {skill_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting skill: {e}")
            return False
    
    def update_skill(self, skill_name: str, implementation: str) -> bool:
        """Update skill implementation"""
        try:
            self.db.update(
                'learned_skills',
                {'implementation': implementation},
                f'skill_name = "{skill_name}"'
            )
            logger.debug(f"Updated skill: {skill_name}")
            return True
        except Exception as e:
            logger.error(f"Error updating skill: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get learned skills statistics"""
        try:
            records = self.db.select('learned_skills')
            
            if not records:
                return {'total_skills': 0}
            
            total_success = sum(r['success_count'] for r in records)
            total_failure = sum(r['failure_count'] for r in records)
            avg_confidence = sum(r['confidence'] for r in records) / len(records) if records else 0
            
            return {
                'total_skills': len(records),
                'total_successes': total_success,
                'total_failures': total_failure,
                'average_confidence': avg_confidence,
                'most_used': max(records, key=lambda x: x['success_count'])['skill_name'] if records else None
            }
        except Exception as e:
            logger.error(f"Error getting skills stats: {e}")
            return {}
