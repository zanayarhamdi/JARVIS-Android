from typing import Dict, List, Optional, Any
from core.logger import create_logger
from memory.memory_manager import get_memory_manager
from core.config import get_config

logger = create_logger("SKILL_BASE")

class Skill:
    """Base class for JARVIS skills"""
    
    def __init__(
        self,
        name: str,
        description: str,
        version: str = "1.0.0",
        author: str = "JARVIS"
    ):
        self.name = name
        self.description = description
        self.version = version
        self.author = author
        self.memory = get_memory_manager()
        self.config = get_config()
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute skill"""
        raise NotImplementedError("Skill must implement execute method")
    
    def learn_from_execution(self, inputs: Dict, output: Any) -> bool:
        """Learn from execution result"""
        return False
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get skill metadata"""
        return {
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'author': self.author
        }
