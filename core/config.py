import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from core.logger import create_logger

logger = create_logger("CONFIG")

class ConfigManager:
    def __init__(self, config_dir="config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config = {}
        self.load_configs()
    
    def load_configs(self):
        """Load all configuration files"""
        try:
            # Load default config
            default_config_path = self.config_dir / "default_config.json"
            if default_config_path.exists():
                with open(default_config_path, 'r', encoding='utf-8') as f:
                    self.config.update(json.load(f))
                logger.info(f"Loaded default config from {default_config_path}")
            
            # Load Android-specific config
            android_config_path = self.config_dir / "android_config.json"
            if android_config_path.exists():
                with open(android_config_path, 'r', encoding='utf-8') as f:
                    self.config.update(json.load(f))
                logger.info(f"Loaded Android config from {android_config_path}")
            
            # Load Termux-specific config
            termux_config_path = self.config_dir / "termux_config.json"
            if termux_config_path.exists():
                with open(termux_config_path, 'r', encoding='utf-8') as f:
                    self.config.update(json.load(f))
                logger.info(f"Loaded Termux config from {termux_config_path}")
        except Exception as e:
            logger.error(f"Error loading configs: {e}")
            self.config = self.get_default_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            "jarvis": {
                "name": "JARVIS",
                "version": "1.0.0",
                "personality": "calm, precise, polite",
                "max_response_length": 2000,
                "context_window": 10
            },
            "memory": {
                "db_path": "data/memory.db",
                "short_term_size": 100,
                "episodic_retention_days": 90,
                "backup_interval_hours": 24
            },
            "tools": {
                "timeout": 30,
                "max_concurrent": 3
            },
            "voice": {
                "enabled": False,
                "wake_word": "jarvis",
                "stt_engine": "google",
                "tts_engine": "android"
            },
            "android": {
                "use_termux_api": True,
                "permission_level": "standard"
            },
            "security": {
                "require_confirmation": ["delete", "modify_system", "install_package"],
                "audit_log": True,
                "backup_before_changes": True
            },
            "learning": {
                "enabled": True,
                "pattern_min_occurrences": 3,
                "skill_autosave": True
            },
            "network": {
                "offline_first": True,
                "timeout": 10
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with dot notation"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """Set configuration value with dot notation"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        logger.debug(f"Set config {key} = {value}")
    
    def save(self, config_name="default_config.json"):
        """Save configuration to file"""
        try:
            config_path = self.config_dir / config_name
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved config to {config_path}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def reload(self):
        """Reload configuration from files"""
        self.config = {}
        self.load_configs()


# Global config instance
_config_instance = None

def get_config() -> ConfigManager:
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance
