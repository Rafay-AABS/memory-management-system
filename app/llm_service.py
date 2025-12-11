"""
LLM Service - Unified interface for multiple LLM providers
Supports OpenAI, Groq, and Gemini APIs
"""

import os
from typing import Optional, Dict, Any, List, Generator
from enum import Enum
import json

class LLMProvider(Enum):
    OPENAI = "openai"
    GROQ = "groq"
    GEMINI = "gemini"

class LLMService:
    """Unified interface for interacting with different LLM providers."""
    
    def __init__(self, provider: str = "gemini", model: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize LLM service.
        
        Args:
            provider: Provider name (openai, groq, gemini)
            model: Model name (uses default if not specified)
            api_key: API key (uses environment variable if not specified)
        """
        self.provider = provider.lower()
        self.model = model
        self.api_key = api_key
        self._client = None
        
        # Default models
        self.default_models = {
            "openai": "gpt-4o",
            "groq": "llama-3.3-70b-versatile",
            "gemini": "gemini-2.5-flash"  # Using Flash for better free tier limits
        }
        
        if not self.model:
            self.model = self.default_models.get(self.provider, "gpt-4o")
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate client based on provider."""
        if self.provider == "openai":
            self._initialize_openai()
        elif self.provider == "groq":
            self._initialize_groq()
        elif self.provider == "gemini":
            self._initialize_gemini()
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _initialize_openai(self):
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
            self._client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
    
    def _initialize_groq(self):
        """Initialize Groq client."""
        try:
            from groq import Groq
            api_key = self.api_key or os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("Groq API key not found. Set GROQ_API_KEY environment variable.")
            self._client = Groq(api_key=api_key)
        except ImportError:
            raise ImportError("Groq package not installed. Run: pip install groq")
    
    def _initialize_gemini(self):
        """Initialize Gemini client."""
        try:
            import google.generativeai as genai
            api_key = self.api_key or os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("Gemini API key not found. Set GEMINI_API_KEY environment variable.")
            genai.configure(api_key=api_key)
            # Use correct model format - add 'models/' prefix if not present
            model_name = self.model if self.model.startswith('models/') else f'models/{self.model}'
            self._client = genai.GenerativeModel(model_name)
        except ImportError:
            raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")
    
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 1000, stream: bool = False) -> Dict[str, Any]:
        """
        Send chat messages to the LLM.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            
        Returns:
            Dict with 'content', 'role', and usage info
        """
        if self.provider in ["openai", "groq"]:
            return self._chat_openai_compatible(messages, temperature, max_tokens, stream)
        elif self.provider == "gemini":
            return self._chat_gemini(messages, temperature, max_tokens, stream)
    
    def _chat_openai_compatible(self, messages: List[Dict[str, str]], temperature: float, max_tokens: int, stream: bool) -> Dict[str, Any]:
        """Chat for OpenAI and Groq (OpenAI-compatible APIs)."""
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )
            
            if stream:
                return {"stream": response, "streaming": True}
            
            return {
                "content": response.choices[0].message.content,
                "role": response.choices[0].message.role,
                "finish_reason": response.choices[0].finish_reason,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            raise Exception(f"Error calling {self.provider} API: {str(e)}")
    
    def _chat_gemini(self, messages: List[Dict[str, str]], temperature: float, max_tokens: int, stream: bool) -> Dict[str, Any]:
        """Chat for Gemini."""
        try:
            # Convert messages to Gemini format
            # Gemini uses a different structure: system message separate, then alternating user/model
            system_message = None
            chat_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                elif msg["role"] == "user":
                    chat_messages.append({"role": "user", "parts": [msg["content"]]})
                elif msg["role"] == "assistant":
                    chat_messages.append({"role": "model", "parts": [msg["content"]]})
            
            # Create generation config
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
            
            # If system message exists, prepend to first user message
            if system_message and chat_messages:
                if chat_messages[0]["role"] == "user":
                    chat_messages[0]["parts"][0] = f"{system_message}\n\n{chat_messages[0]['parts'][0]}"
            
            # For Gemini, we need to use chat or generate_content
            if len(chat_messages) > 1:
                # Multi-turn conversation
                chat = self._client.start_chat(history=chat_messages[:-1])
                response = chat.send_message(
                    chat_messages[-1]["parts"][0],
                    generation_config=generation_config,
                    stream=stream
                )
            else:
                # Single message
                response = self._client.generate_content(
                    chat_messages[0]["parts"][0] if chat_messages else "",
                    generation_config=generation_config,
                    stream=stream
                )
            
            if stream:
                return {"stream": response, "streaming": True}
            
            return {
                "content": response.text,
                "role": "assistant",
                "finish_reason": "stop",
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else 0,
                    "total_tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0
                }
            }
        except Exception as e:
            raise Exception(f"Error calling Gemini API: {str(e)}")
    
    def generate_text(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """
        Generate text from a simple prompt.
        
        Args:
            prompt: Text prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        messages = [{"role": "user", "content": prompt}]
        response = self.chat(messages, temperature, max_tokens)
        return response["content"]
    
    def switch_provider(self, provider: str, model: Optional[str] = None):
        """
        Switch to a different provider.
        
        Args:
            provider: New provider name
            model: Optional model name
        """
        self.provider = provider.lower()
        self.model = model or self.default_models.get(self.provider)
        self._initialize_client()
    
    def switch_model(self, model: str):
        """
        Switch to a different model within the same provider.
        
        Args:
            model: Model name
        """
        self.model = model
        if self.provider == "gemini":
            # Need to reinitialize Gemini client with new model
            self._initialize_gemini()
