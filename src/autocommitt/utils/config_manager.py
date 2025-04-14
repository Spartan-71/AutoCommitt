import json
from typing import Dict
from pathlib import Path
from platformdirs import user_config_dir, user_cache_dir


class ConfigManager:
    """
    Manages application configuration and model settings for AutoCommitt.
    Handles reading/writing config files and model definitions.
    """

    # Use platform-specific config directory
    CONFIG_DIR = Path(user_config_dir("autocommitt"))
    CACHE_DIR = Path(user_cache_dir("autocommitt"))

    # Config files
    CONFIG_FILE = CONFIG_DIR / "config.json"
    MODELS_FILE = CONFIG_DIR / "models.json"

    DEFAULT_MODELS = {
        "deepseek-r1:1.5b": {
            "description": "State of the art reasoning model for your commit messages.",
            "size": "1.1GB",
            "status": "disabled",
            "downloaded": "no",
        },
        "llama3.2:1b": {
            "description": "Lightweight model suitable for basic commit messages",
            "size": "1.3GB",
            "status": "disabled",
            "downloaded": "no",
        },
        "gemma2:2b": {
            "description": "Enhanced lightweight model for moderate commit complexity",
            "size": "1.6GB",
            "status": "disabled",
            "downloaded": "no",
        },
        "llama3.2:3b": {
            "description": "Balanced model for handling complex commits",
            "size": "2.0GB",
            "status": "disabled",
            "downloaded": "no",
        },
    }

    @classmethod
    def ensure_config(cls) -> None:
        """
        Ensures configuration directory and files exist with default values.
        Creates them if they don't exist.
        """
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        # Initialize config file if it doesn't exist
        if not cls.CONFIG_FILE.exists():
            cls.save_config({"model_name": "llama3.2:3b"})

        # Initialize models file if it doesn't exist
        if not cls.MODELS_FILE.exists():
            cls.save_models(cls.DEFAULT_MODELS)

    @classmethod
    def get_config(cls) -> Dict:
        """
        Retrieves current configuration.

        Returns:
            Dict: Current configuration settings
        """
        cls.ensure_config()
        return json.loads(cls.CONFIG_FILE.read_text())

    @classmethod
    def get_models(cls) -> Dict:
        """
        Retrieves available model configurations.

        Returns:
            Dict: Dictionary of available models and their settings
        """
        cls.ensure_config()
        return json.loads(cls.MODELS_FILE.read_text())

    @classmethod
    def save_config(cls, config: Dict) -> None:
        """
        Saves configuration settings to file.

        Args:
            config (Dict): Configuration settings to save
        """
        cls.CONFIG_FILE.write_text(json.dumps(config, indent=2))

    @classmethod
    def save_models(cls, models: Dict) -> None:
        """
        Saves model configurations to file.

        Args:
            models (Dict): Model configurations to save
        """
        cls.MODELS_FILE.write_text(json.dumps(models, indent=2))

    @classmethod
    def get_active_model(cls) -> str:
        """
        Returns the currently active model name.

        Returns:
            str: Name of the active model
        """
        config = cls.get_config()
        return config.get("model_name", "llama3.2:3b")  # Default if not set
