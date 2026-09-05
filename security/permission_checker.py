from typing import Dict, List, Optional
from enum import Enum
from core.logger import create_logger

logger = create_logger("PERMISSION_CHECKER")

class Permission(Enum):
    READ_FILES = "read_files"
    WRITE_FILES = "write_files"
    DELETE_FILES = "delete_files"
    EXECUTE_COMMANDS = "execute_commands"
    NETWORK_ACCESS = "network_access"
    SYSTEM_INFO = "system_info"
    INSTALL_PACKAGES = "install_packages"
    MODIFY_SYSTEM = "modify_system"

class PermissionChecker:
    """Check permissions for operations"""
    
    def __init__(self):
        self.permissions = {
            "user": [
                Permission.READ_FILES,
                Permission.WRITE_FILES,
                Permission.EXECUTE_COMMANDS,
                Permission.SYSTEM_INFO
            ],
            "admin": [
                Permission.READ_FILES,
                Permission.WRITE_FILES,
                Permission.DELETE_FILES,
                Permission.EXECUTE_COMMANDS,
                Permission.NETWORK_ACCESS,
                Permission.SYSTEM_INFO,
                Permission.INSTALL_PACKAGES,
                Permission.MODIFY_SYSTEM
            ]
        }
    
    def has_permission(self, role: str, permission: Permission) -> bool:
        """Check if role has permission"""
        try:
            role_perms = self.permissions.get(role, [])
            result = permission in role_perms
            logger.debug(f"Permission check: {role} -> {permission.value} = {result}")
            return result
        except Exception as e:
            logger.error(f"Error checking permission: {e}")
            return False
    
    def can_perform_action(self, action: str, role: str = "user") -> bool:
        """Check if action is permitted"""
        action_permissions = {
            "delete": Permission.DELETE_FILES,
            "modify_system": Permission.MODIFY_SYSTEM,
            "install_package": Permission.INSTALL_PACKAGES,
            "execute_command": Permission.EXECUTE_COMMANDS,
            "write_file": Permission.WRITE_FILES,
            "read_file": Permission.READ_FILES,
            "network_access": Permission.NETWORK_ACCESS
        }
        
        required_perm = action_permissions.get(action)
        if not required_perm:
            return True
        
        return self.has_permission(role, required_perm)
