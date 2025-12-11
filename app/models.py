"""
AI Model API configurations and metadata.
"""

from typing import Dict, List, Any

# Model API Providers
MODEL_PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "models": [
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4o",
            "gpt-3.5-turbo"
        ],
        "capabilities": ["chat", "completion", "embedding", "vision"],
        "requires_api_key": True,
        "env_var": "OPENAI_API_KEY"
    },
    "groq": {
        "name": "Groq",
        "base_url": "https://api.groq.com/openai/v1",
        "models": [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "openai/gpt-oss-120b",
            "qwen/qwen3-32b"
        ],
        "capabilities": ["chat", "completion"],
        "requires_api_key": True,
        "env_var": "GROQ_API_KEY"
    },
    "gemini": {
        "name": "Google Gemini",
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "models": [
            "gemini-2.5-pro",
            "gemini-2.5-flash",
            "gemini-2.0-flash"
        ],
        "capabilities": ["chat", "completion", "vision", "multimodal"],
        "requires_api_key": True,
        "env_var": "GEMINI_API_KEY"
    }
}

# Default model for each provider
DEFAULT_MODELS = {
    "openai": "gpt-4o",
    "groq": "llama-3.3-70b-versatile",
    "gemini": "gemini-2.5-flash"
}

# Functionality descriptions
PROVIDER_FUNCTIONALITY = {
    "openai": {
        "chat_completion": "Generate conversational responses with context awareness",
        "text_completion": "Complete text based on prompts",
        "embeddings": "Convert text to vector embeddings for semantic search",
        "vision": "Analyze and describe images",
        "function_calling": "Execute functions based on natural language instructions"
    },
    "groq": {
        "chat_completion": "Ultra-fast inference for conversational AI with open-source models",
        "text_completion": "High-speed text generation and completion",
        "streaming": "Real-time token streaming for responsive interactions"
    },
    "gemini": {
        "chat_completion": "Advanced multi-turn conversations with long context windows",
        "text_completion": "Generate and complete text with state-of-the-art quality",
        "vision": "Analyze images and videos with detailed understanding",
        "multimodal": "Process and generate content across text, image, and video",
        "code_execution": "Execute Python code within the model environment"
    }
}

def get_provider_info(provider: str) -> Dict[str, Any]:
    """Get information about a specific provider."""
    return MODEL_PROVIDERS.get(provider.lower())

def get_all_providers() -> List[str]:
    """Get list of all available providers."""
    return list(MODEL_PROVIDERS.keys())

def get_provider_models(provider: str) -> List[str]:
    """Get available models for a specific provider."""
    provider_info = MODEL_PROVIDERS.get(provider.lower())
    return provider_info["models"] if provider_info else []

def get_default_model(provider: str) -> str:
    """Get the default model for a provider."""
    return DEFAULT_MODELS.get(provider.lower())
