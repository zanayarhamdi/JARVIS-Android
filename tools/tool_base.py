from typing import Any, Dict, Optional, Callable
from abc import ABC, abstractmethod
from enum import Enum

class PermissionLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class RiskLevel(Enum):
    SAFE = 1
    LOW_RISK = 2
    MEDIUM_RISK = 3
    HIGH_RISK = 4
    CRITICAL = 5

class BaseTool(ABC):
    """Base class for all tools"""
    
    def __init__(
        self,
        name: str,
        description: str,
        permission_level: PermissionLevel = PermissionLevel.LOW,
        risk_level: RiskLevel = RiskLevel.SAFE
    ):
        self.name = name
        self.description = description
        self.permission_level = permission_level
        self.risk_level = risk_level
        self.parameters = {}
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute tool with given parameters"""
        pass
    
    @abstractmethod
    def verify_result(self, result: Dict[str, Any]) -> bool:
        """Verify execution result"""
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get tool metadata"""
        return {
            'name': self.name,
            'description': self.description,
            'permission_level': self.permission_level.name,
            'risk_level': self.risk_level.name,
            'parameters': self.parameters
        }
