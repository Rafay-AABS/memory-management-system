"""
Example usage of Settings system for model provider management.
"""

from app.settings import get_settings, Settings
from app.models import get_all_providers, PROVIDER_FUNCTIONALITY

def example_basic_settings():
    """Basic settings usage."""
    print("=== Basic Settings Usage ===\n")
    
    settings = get_settings()
    print(f"Current settings: {settings}")
    print(f"Provider: {settings.current_provider}")
    print(f"Model: {settings.current_model}")
    print()

def example_switch_provider_settings():
    """Switch providers using settings."""
    print("=== Switching Providers via Settings ===\n")
    
    settings = get_settings()
    print(f"Started with: {settings.current_provider}")
    
    # Switch to Groq
    settings.switch_provider("groq")
    print(f"Switched to: {settings.current_provider} - {settings.current_model}")
    
    # Switch to Gemini with specific model
    settings.switch_provider("gemini", model="gemini-1.5-flash")
    print(f"Switched to: {settings.current_provider} - {settings.current_model}")
    
    # Switch back to OpenAI
    settings.switch_provider("openai")
    print(f"Back to: {settings.current_provider} - {settings.current_model}")
    print()

def example_switch_model_settings():
    """Switch models within provider."""
    print("=== Switching Models via Settings ===\n")
    
    settings = get_settings()
    settings.switch_provider("openai")
    print(f"Current model: {settings.current_model}")
    
    # Switch to different OpenAI model
    settings.switch_model("gpt-3.5-turbo")
    print(f"Switched to: {settings.current_model}")
    
    settings.switch_model("gpt-4o")
    print(f"Switched to: {settings.current_model}")
    print()

def example_provider_config():
    """Get provider configuration."""
    print("=== Provider Configuration ===\n")
    
    settings = get_settings()
    config = settings.get_provider_config()
    
    print("Current Provider Config:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    print()

def example_check_availability():
    """Check provider availability."""
    print("=== Provider Availability ===\n")
    
    settings = get_settings()
    
    print("Available providers:")
    for provider in get_all_providers():
        is_available = settings.is_provider_enabled(provider)
        status = "✓ Available" if is_available else "✗ Not available"
        print(f"  {provider}: {status}")
    
    print(f"\nAll available: {settings.get_available_providers()}")
    print()

def example_model_preferences():
    """Set and get model preferences."""
    print("=== Model Preferences ===\n")
    
    settings = get_settings()
    
    # Set preferences for different use cases
    settings.set_preferred_model("chat", "openai", "gpt-4o")
    settings.set_preferred_model("fast_inference", "groq", "llama-3.1-8b-instant")
    
    # Get preferred models
    chat_model = settings.get_preferred_model("chat")
    fast_model = settings.get_preferred_model("fast_inference")
    
    print(f"Preferred model for chat: {chat_model}")
    print(f"Preferred model for fast inference: {fast_model}")
    print()

def example_fallback():
    """Get fallback provider."""
    print("=== Fallback Providers ===\n")
    
    settings = get_settings()
    settings.switch_provider("openai")
    
    print(f"Current provider: {settings.current_provider}")
    print(f"Fallback order: {settings.fallback_order}")
    
    next_fallback = settings.get_next_fallback_provider()
    print(f"Next fallback provider: {next_fallback}")
    print()

def example_runtime_settings():
    """Modify runtime settings."""
    print("=== Runtime Settings ===\n")
    
    settings = get_settings()
    
    print(f"Current timeout: {settings.timeout}s")
    print(f"Current max retries: {settings.max_retries}")
    
    # Modify settings
    settings.set_timeout(60)
    settings.set_max_retries(5)
    
    print(f"Updated timeout: {settings.timeout}s")
    print(f"Updated max retries: {settings.max_retries}")
    print()

def example_validate_settings():
    """Validate settings."""
    print("=== Validate Settings ===\n")
    
    settings = get_settings()
    validation = settings.validate_settings()
    
    print(f"Valid: {validation['valid']}")
    if validation['issues']:
        print("Issues:")
        for issue in validation['issues']:
            print(f"  - {issue}")
    if validation['warnings']:
        print("Warnings:")
        for warning in validation['warnings']:
            print(f"  - {warning}")
    print()

def example_all_settings():
    """Display all settings."""
    print("=== All Settings ===\n")
    
    settings = get_settings()
    all_settings = settings.get_all_settings()
    
    for key, value in all_settings.items():
        print(f"{key}: {value}")
    print()

def example_save_and_load():
    """Save and load configuration."""
    print("=== Save and Load Config ===\n")
    
    settings = get_settings()
    
    # Modify settings
    settings.switch_provider("groq")
    settings.set_timeout(45)
    settings.set_max_retries(4)
    
    # Save configuration
    if settings.save_config():
        print("Configuration saved successfully!")
    
    print(f"Current provider saved: {settings.current_provider}")
    print()

if __name__ == "__main__":
    print("SETTINGS SYSTEM EXAMPLES")
    print("=" * 60)
    print()
    
    example_basic_settings()
    example_switch_provider_settings()
    example_switch_model_settings()
    example_provider_config()
    example_check_availability()
    example_model_preferences()
    example_fallback()
    example_runtime_settings()
    example_validate_settings()
    example_all_settings()
    example_save_and_load()
    
    print("=" * 60)
    print("\nSettings features:")
    print("  ✓ Easy provider switching")
    print("  ✓ Model management")
    print("  ✓ API key handling")
    print("  ✓ Fallback configuration")
    print("  ✓ Model preferences per use case")
    print("  ✓ Runtime settings (timeout, retries)")
    print("  ✓ Configuration persistence")
    print("  ✓ Settings validation")
