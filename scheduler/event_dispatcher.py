from typing import Dict, Callable, Optional, List
from core.logger import create_logger

logger = create_logger("EVENT_DISPATCHER")

class EventDispatcher:
    """Dispatch and handle events"""
    
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, callback: Callable) -> bool:
        """Subscribe to event"""
        try:
            if event_type not in self.listeners:
                self.listeners[event_type] = []
            
            self.listeners[event_type].append(callback)
            logger.debug(f"Subscribed to event: {event_type}")
            return True
        except Exception as e:
            logger.error(f"Error subscribing to event: {e}")
            return False
    
    def dispatch(self, event_type: str, data: Optional[Dict] = None) -> bool:
        """Dispatch event"""
        try:
            if event_type not in self.listeners:
                return False
            
            for callback in self.listeners[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Error in event callback: {e}")
            
            logger.debug(f"Dispatched event: {event_type}")
            return True
        except Exception as e:
            logger.error(f"Error dispatching event: {e}")
            return False
