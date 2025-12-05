"""
Example usage of the Model Client system.
"""

from app.client import ModelClient
from app.models import get_all_providers, get_provider_models, PROVIDER_FUNCTIONALITY

def example_basic_usage():
    """Basic usage: Initialize and use a model client."""
    print("=== Basic Usage ===\n")
    
    # Initialize with OpenAI (default)
    client = ModelClient(provider="openai")
    print(f"Initialized: {client}")
    print(f"Config: {client.get_client_config()}\n")

def example_switch_provider():
    """Example: Switch between different providers."""
    print("=== Switching Between Providers ===\n")
    
    client = ModelClient(provider="openai")
    print(f"Started with: {client.provider} - {client.model}")
    
    # Switch to Groq
    client.switch_provider("groq")
    print(f"Switched to: {client.provider} - {client.model}")
    
    # Switch to Gemini
    client.switch_provider("gemini")
    print(f"Switched to: {client.provider} - {client.model}\n")

def example_switch_model():
    """Example: Switch models within the same provider."""
    print("=== Switching Models ===\n")
    
    client = ModelClient(provider="openai", model="gpt-4o")
    print(f"Current model: {client.model}")
    
    # Switch to a different OpenAI model
    client.switch_model("gpt-3.5-turbo")
    print(f"Switched to: {client.model}\n")

def example_list_providers():
    """Example: List all available providers and their models."""
    print("=== Available Providers ===\n")
    
    providers = get_all_providers()
    for provider in providers:
        models = get_provider_models(provider)
        print(f"{provider.upper()}:")
        print(f"  Models: {', '.join(models)}")
        print(f"  Functionality:")
        for func_name, func_desc in PROVIDER_FUNCTIONALITY[provider].items():
            print(f"    - {func_name}: {func_desc}")
        print()

def example_check_capabilities():
    """Example: Check provider capabilities."""
    print("=== Checking Capabilities ===\n")
    
    client = ModelClient(provider="groq")
    print(f"Provider: {client.provider}")
    print(f"Has chat capability: {client.has_capability('chat')}")
    print(f"Has vision capability: {client.has_capability('vision')}")
    print(f"Has embedding capability: {client.has_capability('embedding')}\n")

def example_api_call():
    """Example: Make an API call (placeholder)."""
    print("=== Making API Call ===\n")
    
    client = ModelClient(provider="openai")
    messages = [
        {"role": "user", "content": "What are the key features of this system?"}
    ]
    
    response = client.call_api(messages, temperature=0.7)
    print(f"Response: {response}\n")

if __name__ == "__main__":
    print("MODEL CLIENT EXAMPLES\n")
    print("=" * 50)
    print()
    
    example_basic_usage()
    example_switch_provider()
    example_switch_model()
    example_list_providers()
    example_check_capabilities()
    example_api_call()
    
    print("=" * 50)
    print("\nNote: Set environment variables for API keys:")
    print("  - OPENAI_API_KEY")
    print("  - GROQ_API_KEY")
    print("  - GEMINI_API_KEY")
