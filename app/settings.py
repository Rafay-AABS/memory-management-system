"""
Settings management for the Memory Management System.
Handles model provider configuration, API keys, and runtime settings.
"""

import os
import json
from typing import Optional, Dict, Any, List
from pathlib import Path
from enum import Enum
from . import strings

class ModelProvider(Enum):
    """Available model providers."""
    OPENAI = "openai"
    GROQ = "groq"
    GEMINI = "gemini"

class Settings:
    """Centralized settings manager for the application."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize settings.
        
        Args:
            config_path: Path to configuration JSON file
        """
        self.config_path = config_path or os.path.join("data", "model_config.json")
        self.config = self._load_config()
        
        # Model provider settings
        self._current_provider = self.config.get("default_provider", "openai")
        self._current_model = None
        
        # API keys
        self.api_keys = {
            "openai": os.getenv("OPENAI_API_KEY"),
            "groq": os.getenv("GROQ_API_KEY"),
            "gemini": os.getenv("GEMINI_API_KEY")
        }
        
        # Runtime settings
        self.timeout = self.config.get("timeout_seconds", 30)
        self.max_retries = self.config.get("max_retries", 3)
        self.fallback_order = self.config.get("fallback_order", ["openai", "groq", "gemini"])
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
        
        # Return default config if file doesn't exist
        return {
            "default_provider": "openai",
            "timeout_seconds": 30,
            "max_retries": 3,
            "fallback_order": ["openai", "groq", "gemini"]
        }
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            self.config["default_provider"] = self._current_provider
            self.config["timeout_seconds"] = self.timeout
            self.config["max_retries"] = self.max_retries
            self.config["fallback_order"] = self.fallback_order
            
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, indent=2, fp=f)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    # Model Provider Management
    
    @property
    def current_provider(self) -> str:
        """Get current model provider."""
        return self._current_provider
    
    @current_provider.setter
    def current_provider(self, provider: str):
        """Set current model provider."""
        if provider.lower() not in ["openai", "groq", "gemini"]:
            raise ValueError(f"Invalid provider: {provider}. Must be one of: openai, groq, gemini")
        self._current_provider = provider.lower()
        self._current_model = None  # Reset model when provider changes
    
    @property
    def current_model(self) -> Optional[str]:
        """Get current model."""
        if not self._current_model:
            # Get default model for current provider
            from .models import DEFAULT_MODELS
            return DEFAULT_MODELS.get(self._current_provider)
        return self._current_model
    
    @current_model.setter
    def current_model(self, model: str):
        """Set current model."""
        from .models import get_provider_models
        available_models = get_provider_models(self._current_provider)
        if model not in available_models:
            raise ValueError(f"Model {model} not available for {self._current_provider}")
        self._current_model = model
    
    def switch_provider(self, provider: str, model: Optional[str] = None):
        """
        Switch to a different provider.
        
        Args:
            provider: Provider name (openai, groq, gemini)
            model: Optional specific model to use
        """
        self.current_provider = provider
        if model:
            self.current_model = model
        return self
    
    def switch_model(self, model: str):
        """
        Switch to a different model within current provider.
        
        Args:
            model: Model name
        """
        self.current_model = model
        return self
    
    def get_provider_config(self) -> Dict[str, Any]:
        """Get configuration for current provider."""
        from .models import get_provider_info
        provider_info = get_provider_info(self._current_provider)
        
        return {
            "provider": self._current_provider,
            "provider_name": provider_info["name"],
            "model": self.current_model,
            "base_url": provider_info["base_url"],
            "api_key_set": bool(self.api_keys.get(self._current_provider)),
            "capabilities": provider_info["capabilities"]
        }
    
    def get_api_key(self, provider: Optional[str] = None) -> Optional[str]:
        """
        Get API key for a provider.
        
        Args:
            provider: Provider name (uses current provider if None)
        """
        provider = provider or self._current_provider
        return self.api_keys.get(provider)
    
    def set_api_key(self, provider: str, api_key: str):
        """
        Set API key for a provider.
        
        Args:
            provider: Provider name
            api_key: API key value
        """
        if provider not in self.api_keys:
            raise ValueError(f"Unknown provider: {provider}")
        self.api_keys[provider] = api_key
        os.environ[f"{provider.upper()}_API_KEY"] = api_key
    
    # Provider Availability
    
    def is_provider_enabled(self, provider: str) -> bool:
        """Check if a provider is enabled and has API key."""
        providers_config = self.config.get("providers", {})
        provider_config = providers_config.get(provider, {})
        
        is_enabled = provider_config.get("enabled", True)
        has_api_key = bool(self.api_keys.get(provider))
        
        return is_enabled and has_api_key
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers (enabled with API keys)."""
        return [p for p in ["openai", "groq", "gemini"] if self.is_provider_enabled(p)]
    
    def get_next_fallback_provider(self) -> Optional[str]:
        """Get next available provider from fallback order."""
        available = self.get_available_providers()
        for provider in self.fallback_order:
            if provider != self._current_provider and provider in available:
                return provider
        return None
    
    # Model Preferences
    
    def get_preferred_model(self, use_case: str = "chat") -> str:
        """
        Get preferred model for a specific use case.
        
        Args:
            use_case: Use case name (chat, fast_inference, etc.)
        """
        preferences = self.config.get("model_preferences", {})
        use_case_prefs = preferences.get(use_case, {})
        return use_case_prefs.get(self._current_provider, self.current_model)
    
    def set_preferred_model(self, use_case: str, provider: str, model: str):
        """
        Set preferred model for a use case and provider.
        
        Args:
            use_case: Use case name
            provider: Provider name
            model: Model name
        """
        if "model_preferences" not in self.config:
            self.config["model_preferences"] = {}
        if use_case not in self.config["model_preferences"]:
            self.config["model_preferences"][use_case] = {}
        
        self.config["model_preferences"][use_case][provider] = model
    
    # Runtime Settings
    
    def set_timeout(self, seconds: int):
        """Set API timeout in seconds."""
        self.timeout = seconds
    
    def set_max_retries(self, retries: int):
        """Set maximum retry attempts."""
        self.max_retries = retries
    
    def set_fallback_order(self, providers: List[str]):
        """Set fallback provider order."""
        self.fallback_order = providers
    
    # Summary Methods
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all current settings."""
        return {
            "current_provider": self._current_provider,
            "current_model": self.current_model,
            "available_providers": self.get_available_providers(),
            "timeout_seconds": self.timeout,
            "max_retries": self.max_retries,
            "fallback_order": self.fallback_order,
            "api_keys_configured": {
                provider: bool(key) for provider, key in self.api_keys.items()
            }
        }
    
    def validate_settings(self) -> Dict[str, Any]:
        """Validate current settings and return status."""
        issues = []
        warnings = []
        
        # Check if current provider has API key
        if not self.get_api_key():
            issues.append(f"No API key configured for {self._current_provider}")
        
        # Check if at least one provider is available
        available = self.get_available_providers()
        if not available:
            issues.append("No providers available (check API keys)")
        elif len(available) == 1:
            warnings.append("Only one provider available (no fallback)")
        
        # Check model validity
        from .models import get_provider_models
        if self._current_model:
            available_models = get_provider_models(self._current_provider)
            if self._current_model not in available_models:
                issues.append(f"Model {self._current_model} not valid for {self._current_provider}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings
        }
    
    def __repr__(self) -> str:
        return f"Settings(provider='{self._current_provider}', model='{self.current_model}')"


# Global settings instance
_settings_instance = None

def get_settings() -> Settings:
    """Get global settings instance."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance

def reset_settings():
    """Reset global settings instance."""
    global _settings_instance
    _settings_instance = None
