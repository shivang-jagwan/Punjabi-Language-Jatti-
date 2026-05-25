"""
Jatti LLM Configuration Management
Load, validate, and override configurations with environment variables
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JattiLLMConfig:
    """Configuration manager for Jatti LLM."""
    
    DEFAULT_CONFIG = {
        "model_type": "openai",
        "openai": {
            "model": "gpt-3.5-turbo",
            "api_key": "${OPENAI_API_KEY}",
            "base_url": "https://api.openai.com/v1",
            "timeout": 60,
            "max_retries": 3,
            "fine_tuning": {
                "epochs": 3,
                "batch_size": 32,
                "learning_rate": 2e-5
            }
        },
        "huggingface": {
            "model": "meta-llama/CodeLlama-7b-hf",
            "device": "auto",
            "dtype": "float16",
            "max_memory": None,
            "fine_tuning": {
                "epochs": 3,
                "batch_size": 8,
                "learning_rate": 1e-4,
                "use_lora": True,
                "lora_rank": 8,
                "lora_alpha": 16,
                "lora_dropout": 0.1
            },
            "output_dir": "./jatti_codellama_ft"
        },
        "data": {
            "train_file": "training_data.jsonl",
            "test_size": 0.1,
            "val_size": 0.1,
            "seed": 42,
            "max_seq_length": 512,
            "truncate": True
        },
        "inference": {
            "host": "localhost",
            "port": 5000,
            "model_path": None,
            "use_auth_token": False,
            "cache_dir": "./.cache",
            "debug": False
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": None
        },
        "monitoring": {
            "track_metrics": True,
            "save_dir": "./metrics",
            "log_wandb": False,
            "wandb_project": "jatti-llm"
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to YAML or JSON config file
        """
        self.config_path = config_path
        self.config = self._load_config()
        self._apply_env_overrides()
        self._validate_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        if self.config_path and Path(self.config_path).exists():
            logger.info(f"Loading config from: {self.config_path}")
            
            if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f)
            else:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
        
        logger.info("Using default configuration")
        return self.DEFAULT_CONFIG.copy()
    
    def _apply_env_overrides(self):
        """Apply environment variable overrides."""
        overrides = {
            "JATTI_MODEL_TYPE": ("model_type", str),
            "JATTI_OPENAI_KEY": ("openai.api_key", str),
            "JATTI_OPENAI_MODEL": ("openai.model", str),
            "JATTI_HF_MODEL": ("huggingface.model", str),
            "JATTI_DATA_FILE": ("data.train_file", str),
            "JATTI_INFERENCE_PORT": ("inference.port", int),
            "JATTI_INFERENCE_HOST": ("inference.host", str),
            "JATTI_EPOCHS": ("openai.fine_tuning.epochs", int),
            "JATTI_BATCH_SIZE": ("openai.fine_tuning.batch_size", int),
            "JATTI_DEBUG": ("inference.debug", lambda x: x.lower() == "true"),
            "JATTI_LOG_LEVEL": ("logging.level", str),
        }
        
        for env_var, (config_path, value_type) in overrides.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                try:
                    converted_value = value_type(value)
                    self._set_nested(config_path, converted_value)
                    logger.info(f"Overriding {config_path} from {env_var}")
                except Exception as e:
                    logger.warning(f"Failed to override {config_path}: {e}")
    
    def _set_nested(self, path: str, value: Any):
        """Set nested dictionary value using dot notation."""
        keys = path.split('.')
        current = self.config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def _get_nested(self, path: str) -> Any:
        """Get nested dictionary value using dot notation."""
        keys = path.split('.')
        current = self.config
        
        for key in keys:
            if isinstance(current, dict):
                current = current.get(key)
            else:
                return None
        
        return current
    
    def _validate_config(self):
        """Validate configuration."""
        model_type = self.config.get("model_type")
        if model_type not in ["openai", "huggingface"]:
            raise ValueError(f"Invalid model_type: {model_type}. Use 'openai' or 'huggingface'")
        
        if model_type == "openai":
            api_key = self.config["openai"].get("api_key", "")
            if not api_key or api_key == "${OPENAI_API_KEY}":
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    logger.warning("⚠️  OPENAI_API_KEY not configured. Set OPENAI_API_KEY environment variable")
        
        logger.info(f"✅ Config validated. Model type: {model_type}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        value = self._get_nested(key)
        
        if value is None:
            return default
        
        # Replace environment variable references
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            return os.getenv(env_var, default)
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        self._set_nested(key, value)
    
    def save(self, path: Optional[str] = None, format: str = "json"):
        """
        Save configuration to file.
        
        Args:
            path: Output file path
            format: "json" or "yaml"
        """
        path = path or self.config_path or "jatti_llm_config.json"
        
        if format == "yaml":
            with open(path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
        else:  # json
            with open(path, 'w') as f:
                json.dump(self.config, f, indent=2)
        
        logger.info(f"Config saved to {path}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Get entire config as dictionary."""
        return self.config.copy()
    
    def to_json(self) -> str:
        """Get entire config as JSON string."""
        return json.dumps(self.config, indent=2)
    
    def get_training_config(self) -> Dict[str, Any]:
        """Get only training-related configuration."""
        model_type = self.config.get("model_type")
        
        return {
            "model_type": model_type,
            "model": self.config[model_type].get("model"),
            "fine_tuning": self.config[model_type].get("fine_tuning", {}),
            "data": self.config["data"]
        }
    
    def get_inference_config(self) -> Dict[str, Any]:
        """Get only inference-related configuration."""
        model_type = self.config.get("model_type")
        
        return {
            "model_type": model_type,
            "model": self.config[model_type].get("model"),
            "model_path": self.config["inference"].get("model_path"),
            "inference": self.config["inference"]
        }
    
    def get_profile(self, profile_name: str) -> "JattiLLMConfig":
        """
        Create config for different profiles.
        
        Profiles:
        - "development": Smaller models, faster inference
        - "staging": Medium models, balanced
        - "production": Large models, high quality
        """
        profiles = {
            "development": {
                "model_type": "huggingface",
                "huggingface": {
                    "model": "gpt2",
                    "fine_tuning": {
                        "epochs": 1,
                        "batch_size": 4,
                        "learning_rate": 5e-5
                    }
                },
                "inference": {
                    "port": 5000,
                    "debug": True
                }
            },
            "staging": {
                "model_type": "huggingface",
                "huggingface": {
                    "model": "meta-llama/CodeLlama-7b-hf",
                    "fine_tuning": {
                        "epochs": 2,
                        "batch_size": 8
                    }
                }
            },
            "production": {
                "model_type": "openai",
                "openai": {
                    "model": "gpt-4",
                    "fine_tuning": {
                        "epochs": 5,
                        "batch_size": 64
                    }
                }
            }
        }
        
        if profile_name not in profiles:
            raise ValueError(f"Unknown profile: {profile_name}. Use: {list(profiles.keys())}")
        
        # Deep merge profile into config
        profile_config = profiles[profile_name]
        merged = self._deep_merge(self.config, profile_config)
        
        new_config = JattiLLMConfig.__new__(JattiLLMConfig)
        new_config.config = merged
        new_config.config_path = self.config_path
        
        logger.info(f"Loaded profile: {profile_name}")
        return new_config
    
    @staticmethod
    def _deep_merge(base: dict, update: dict) -> dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = JattiLLMConfig._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def __repr__(self) -> str:
        return f"JattiLLMConfig({self.config.get('model_type')})"


def create_config_file(path: str = "jatti_llm_config.json", format: str = "json"):
    """Create a default configuration file."""
    config = JattiLLMConfig()
    config.save(path, format)
    print(f"✅ Configuration file created: {path}")


def load_config(path: Optional[str] = None) -> JattiLLMConfig:
    """Load configuration from file or environment."""
    return JattiLLMConfig(path)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Jatti LLM Configuration Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Create command
    create_cmd = subparsers.add_parser("create", help="Create default config file")
    create_cmd.add_argument("--output", default="jatti_llm_config.json", help="Output file")
    create_cmd.add_argument("--format", choices=["json", "yaml"], default="json", help="File format")
    
    # Show command
    show_cmd = subparsers.add_parser("show", help="Show current config")
    show_cmd.add_argument("--file", help="Config file to load")
    show_cmd.add_argument("--key", help="Show specific key")
    show_cmd.add_argument("--profile", choices=["development", "staging", "production"], help="Show profile config")
    
    # Validate command
    validate_cmd = subparsers.add_parser("validate", help="Validate config file")
    validate_cmd.add_argument("--file", help="Config file to validate")
    
    args = parser.parse_args()
    
    if args.command == "create":
        create_config_file(args.output, args.format)
    
    elif args.command == "show":
        config = load_config(args.file)
        
        if args.profile:
            config = config.get_profile(args.profile)
        
        if args.key:
            value = config.get(args.key)
            print(f"{args.key}: {value}")
        else:
            print(config.to_json())
    
    elif args.command == "validate":
        config = load_config(args.file)
        print("✅ Configuration is valid")
    
    else:
        parser.print_help()
