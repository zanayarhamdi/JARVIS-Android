from typing import Dict, List, Optional, Any
from pathlib import Path
from core.logger import create_logger
from skills.skill_base import Skill

logger = create_logger("SKILL_MANAGER")

class SkillManager:
    """Manage and discover skills"""
    
    def __init__(self, skills_dir: str = "skills/built_in"):
        self.skills_dir = Path(skills_dir)
        self.skills: Dict[str, Skill] = {}
        self.load_built_in_skills()
    
    def load_built_in_skills(self):
        """Load built-in skills"""
        logger.info("Built-in skills loaded")
    
    def register_skill(self, skill: Skill) -> bool:
        """Register a skill"""
        try:
            if skill.name in self.skills:
                logger.warning(f"Skill already registered: {skill.name}")
                return False
            
            self.skills[skill.name] = skill
            logger.info(f"Registered skill: {skill.name}")
            return True
        except Exception as e:
            logger.error(f"Error registering skill: {e}")
            return False
    
    def get_skill(self, name: str) -> Optional[Skill]:
        """Get skill by name"""
        return self.skills.get(name)
    
    def execute_skill(self, name: str, **kwargs) -> Dict[str, Any]:
        """Execute skill"""
        try:
            skill = self.get_skill(name)
            if not skill:
                logger.error(f"Skill not found: {name}")
                return {'success': False, 'error': f'Skill not found: {name}'}
            
            result = skill.execute(**kwargs)
            return result
        except Exception as e:
            logger.error(f"Error executing skill: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_all_skills(self) -> Dict[str, Skill]:
        """Get all skills"""
        return self.skills.copy()
