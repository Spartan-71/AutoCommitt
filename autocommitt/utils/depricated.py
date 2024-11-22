import os
import json
from typing import Dict


class ConfigManager:
     
    # Constants
    CONFIG_DIR = os.path.expanduser("~/.autocommitt")
    CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
    MODELS_FILE = os.path.join(CONFIG_DIR, "models.json")
    
    
    DEFAULT_MODELS = {
        "llama3.2:1b": {
            "description": "Lightweight model good for simple commits",
            "size":"1.3GB",
            "status":"disabled",
            "downloaded":"no"
        },
        "gemma2:2b": {
            "description":"Improved lightweight model", 
            "size":"1.6GB",
            "status": "disabled",
            "downloaded":"no"
    
        },
        "llama3.2:3b": {
            "description":"Good quality for complex changes",
            "size":"2.0GB",
            "status":"disabled",
            "downloaded":"no"
    
        },
        "llama3.1:8b": {
            "description":"Best quality for complex changes" ,
            "size":"4.7GB",
            "status": "disabled",
            "downloaded":"no"
    
        }
    }
    
    @classmethod
    def ensure_config(cls) -> None:
        """Ensure config directory and files exist"""
        os.makedirs(cls.CONFIG_DIR, exist_ok=True)
        
        # Initialize config file if it doesn't exist
        if not os.path.exists(cls.CONFIG_FILE):
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump({"model_name": "llama3.2:3b"}, f)
        
        # Initialize models file if it doesn't exist
        if not os.path.exists(cls.MODELS_FILE):
            with open(cls.MODELS_FILE, 'w') as f:
                json.dump(cls.DEFAULT_MODELS, f)

    @classmethod
    def get_config(cls) -> Dict:
        """Get current configuration"""
        cls.ensure_config()
        with open(cls.CONFIG_FILE, 'r') as f:
            return json.load(f)
    
    @classmethod
    def get_models(cls) -> dict:
        """Get available models"""
        cls.ensure_config()
        with open(cls.MODELS_FILE, 'r') as f:
            return json.load(f)
    
    @classmethod
    def save_config(cls, config: Dict) -> None:
        """Save configuration"""
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    
    @classmethod
    def save_models(cls, models: Dict) -> None:
        """Save models configuration"""
        with open(cls.MODELS_FILE, 'w') as f:
            json.dump(models, f, indent=2)