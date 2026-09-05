from typing import Dict, Optional
from enum import Enum
from core.logger import create_logger

logger = create_logger("RISK_ASSESSOR")

class RiskLevel(Enum):
    SAFE = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5

class RiskAssessor:
    """Assess risk of operations"""
    
    def __init__(self):
        self.risk_rules = {
            "delete": RiskLevel.HIGH,
            "modify_system": RiskLevel.CRITICAL,
            "install_package": RiskLevel.HIGH,
            "execute_command": RiskLevel.MEDIUM,
            "write_file": RiskLevel.LOW,
            "read_file": RiskLevel.SAFE
        }
    
    def assess_risk(self, action: str, params: Optional[Dict] = None) -> Dict:
        """Assess risk of action"""
        try:
            risk_level = self.risk_rules.get(action, RiskLevel.MEDIUM)
            
            assessment = {
                'action': action,
                'risk_level': risk_level.name,
                'requires_confirmation': risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL],
                'requires_backup': risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
            }
            
            logger.debug(f"Risk assessment: {action} = {risk_level.name}")
            return assessment
        except Exception as e:
            logger.error(f"Error assessing risk: {e}")
            return {'action': action, 'risk_level': 'UNKNOWN', 'error': str(e)}
