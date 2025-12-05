"""
AI Model Client Manager for switching between different API providers.
"""

import os
from typing import Optional, Dict, Any
from enum import Enum
from .models import MODEL_PROVIDERS, DEFAULT_MODELS, get_provider_info
from .settings import get_settings
from . import strings

class ModelProvider(Enum):
    OPENAI = "openai"
    GROQ = "groq"
    GEMINI = "gemini"
class ModelClient:
    """Manages AI model API clients and handles switching between providers."""
    
    def __init__(self, provider: str = None, model: Optional[str] = None, api_key: Optional[str] = None, use_settings: bool = True):
        """
        Initialize the model client.
        
        Args:
            provider: The API provider (openai, groq, gemini). Uses settings default if None.
            model: Specific model to use (uses default if not specified)
            api_key: API key for the provider (uses environment variable if not specified)
            use_settings: Whether to use global settings instance
        """
        self.settings = get_settings() if use_settings else None
        
        # Use settings if available and no explicit provider given
        if provider is None and self.settings:
            provider = self.settings.current_provider
        elif provider is None:
            provider = "openai"
        
        self.provider = provider.lower()
        self.provider_info = get_provider_info(self.provider)
        
        if not self.provider_info:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(MODEL_PROVIDERS.keys())}")
        
        # Get model from settings if available
    def switch_provider(self, provider: str, model: Optional[str] = None, api_key: Optional[str] = None):
        """
        Switch to a different API provider.
        
        Args:
            provider: New provider to switch to
            model: Model to use with new provider
            api_key: API key for new provider
        """
        # Update settings if available
        if self.settings:
    def switch_model(self, model: str):
        """
        Switch to a different model within the same provider.
        
        Args:
            model: Model name to switch to
        """
        available_models = self.provider_info["models"]
        if model not in available_models:
            raise ValueError(f"Model {model} not available for {self.provider}. Available: {available_models}")
        
        self.model = model
        
        # Update settings if available
        if self.settings:
            self.settings.current_model = model
    def switch_provider(self, provider: str, model: Optional[str] = None, api_key: Optional[str] = None):
        """
        Switch to a different API provider.
        
        Args:
            provider: New provider to switch to
            model: Model to use with new provider
            api_key: API key for new provider
        """
        self.__init__(provider, model, api_key)
    
    def switch_model(self, model: str):
        """
        Switch to a different model within the same provider.
        
        Args:
            model: Model name to switch to
        """
        available_models = self.provider_info["models"]
        if model not in available_models:
            raise ValueError(f"Model {model} not available for {self.provider}. Available: {available_models}")
        self.model = model
    
    def get_client_config(self) -> Dict[str, Any]:
        """Get current client configuration."""
        return {
            "provider": self.provider,
            "provider_name": self.provider_info["name"],
            "model": self.model,
            "base_url": self.base_url,
            "capabilities": self.capabilities,
            "available_models": self.provider_info["models"]
        }
    
    def has_capability(self, capability: str) -> bool:
        """Check if current provider supports a specific capability."""
        return capability in self.capabilities
    
    def call_api(self, messages: list, temperature: float = 0.7, max_tokens: Optional[int] = None) -> Dict[str, Any]:
        """
        Make an API call to the current provider.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            API response dictionary
        """
        # This is a placeholder for actual API implementation
        # In production, this would use the appropriate SDK for each provider
        
        if not self.has_capability("chat"):
            raise ValueError(f"{self.provider} does not support chat completion")
        
        # Placeholder response structure
        return {
            "provider": self.provider,
            "model": self.model,
            "status": "success",
            "message": "This is a placeholder. Implement actual API calls using provider SDKs."
        }
    
    @staticmethod
    def list_all_providers() -> Dict[str, Any]:
        """List all available providers and their details."""
        return MODEL_PROVIDERS
    
    def __repr__(self) -> str:
        return f"ModelClient(provider='{self.provider}', model='{self.model}')"
