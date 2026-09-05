from typing import Dict, Optional, Any, List, Type
from core.logger import create_logger
from tools.tool_base import BaseTool

logger = create_logger("TOOL_REGISTRY")

class ToolRegistry:
    """Registry and manager for all tools"""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._load_built_in_tools()
    
    def _load_built_in_tools(self):
        """Load built-in tools"""
        # Placeholder for dynamic loading
        logger.info("Built-in tools initialized")
    
    def register_tool(self, tool: BaseTool) -> bool:
        """Register a new tool"""
        try:
            if tool.name in self.tools:
                logger.warning(f"Tool already registered: {tool.name}")
                return False
            
            self.tools[tool.name] = tool
            logger.info(f"Registered tool: {tool.name}")
            return True
        except Exception as e:
            logger.error(f"Error registering tool: {e}")
            return False
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get tool by name"""
        return self.tools.get(name)
    
    def get_all_tools(self) -> Dict[str, BaseTool]:
        """Get all registered tools"""
        return self.tools.copy()
    
    def find_tool_by_capability(self, capability: str) -> List[BaseTool]:
        """Find tools by capability"""
        matching_tools = []
        for tool in self.tools.values():
            if capability.lower() in tool.description.lower():
                matching_tools.append(tool)
        return matching_tools
    
    def execute_tool(self, name: str, **kwargs) -> Dict[str, Any]:
        """Execute tool by name"""
        try:
            tool = self.get_tool(name)
            if not tool:
                logger.error(f"Tool not found: {name}")
                return {'success': False, 'error': f'Tool not found: {name}'}
            
            logger.debug(f"Executing tool: {name}")
            result = tool.execute(**kwargs)
            
            # Verify result
            verified = tool.verify_result(result)
            result['verified'] = verified
            
            return result
        except Exception as e:
            logger.error(f"Error executing tool: {e}")
            return {'success': False, 'error': str(e)}


_registry_instance = None

def get_tool_registry() -> ToolRegistry:
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = ToolRegistry()
    return _registry_instance
