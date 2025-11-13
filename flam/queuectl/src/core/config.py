"""
Configuration management
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """Configuration manager for queuectl"""

    def __init__(self):
        self.config_dir = Path.home() / '.queuectl'
        self.config_file = self.config_dir / 'config.json'
        self.data_dir = self.config_dir / 'data'
        self.jobs_file = self.data_dir / 'jobs.json'
        self.dlq_file = self.data_dir / 'dlq.json'
        self.pid_file = self.config_dir / 'workers.pid'

        # Create directories if they don't exist
        self.config_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)

        # Default configuration
        self.defaults = {
            'max_retries': 3,
            'backoff_base': 2,
            'max_workers': 10,
            'worker_timeout': 3600,
        }

        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return self.defaults.copy()
        return self.defaults.copy()

    def _save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self._config, f, indent=2)

    def get(self, key: str, default=None):
        """Get configuration value"""
        return self._config.get(key, default if default is not None else self.defaults.get(key))

    def set(self, key: str, value: Any):
        """Set configuration value"""
        self._config[key] = value
        self._save_config()

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self._config.copy()

    def reset(self):
        """Reset to defaults"""
        self._config = self.defaults.copy()
        self._save_config()


# Global config instance
config = Config()
