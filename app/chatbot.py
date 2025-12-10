"""
Chatbot - Main conversation engine with memory management
"""

import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime

from .llm_service import LLMService
from .memory_manager import MemoryManager
from .prompts import SYSTEM_PROMPT, INTENT_CLASSIFICATION_PROMPT


class Chatbot:
    """Main chatbot engine with LLM-based memory management."""
    
    def __init__(self, provider: str = "gemini", model: Optional[str] = None, 
                 system_prompt: Optional[str] = None, session_id: Optional[str] = None):
        """
        Initialize chatbot.
        
        Args:
            provider: LLM provider (openai, groq, gemini)
            model: Model name (uses default if not specified)
            system_prompt: Custom system prompt (uses default if not specified)
            session_id: Session identifier (generates new if not specified)
        """
        self.session_id = session_id or str(uuid.uuid4())
        self.llm = LLMService(provider=provider, model=model)
        self.memory = MemoryManager(llm_service=self.llm)
        self.system_prompt = system_prompt or SYSTEM_PROMPT
        
        # Add system prompt to memory
        self.memory.add_message("system", self.system_prompt)
        
        # Session metadata
        self.metadata = {
            "session_id": self.session_id,
            "created_at": datetime.now().isoformat(),
            "provider": provider,
            "model": model or self.llm.model,
            "message_count": 0
        }
    
    def chat(self, user_message: str, temperature: float = 0.7, max_tokens: int = 1000) -> Dict[str, Any]:
        """
        Process user message and generate response.
        
        Args:
            user_message: User's message
            temperature: Response randomness (0.0-1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Dictionary with response and metadata
        """
        # Add user message to memory
        self.memory.add_message("user", user_message)
        self.metadata["message_count"] += 1
        
        # Get conversation context
        context_messages = self.memory.get_context_for_llm(include_summary=True, recent_count=10)
        
        # Add system prompt at the beginning if not already there
        if not context_messages or context_messages[0]["role"] != "system":
            context_messages.insert(0, {"role": "system", "content": self.system_prompt})
        
        # Generate response
        try:
            response = self.llm.chat(
                messages=context_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            assistant_message = response["content"]
            
            # Add assistant response to memory
            self.memory.add_message("assistant", assistant_message)
            
            return {
                "response": assistant_message,
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "provider": self.llm.provider,
                    "model": self.llm.model,
                    "usage": response.get("usage", {}),
                    "finish_reason": response.get("finish_reason", "stop")
                }
            }
        
        except Exception as e:
            error_message = f"Error generating response: {str(e)}"
            return {
                "response": "I apologize, but I encountered an error processing your message. Please try again.",
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "error": error_message,
                "metadata": {}
            }
    
    def stream_chat(self, user_message: str, temperature: float = 0.7, max_tokens: int = 1000):
        """
        Process user message and stream response.
        
        Args:
            user_message: User's message
            temperature: Response randomness
            max_tokens: Maximum tokens in response
            
        Yields:
            Chunks of the response
        """
        # Add user message to memory
        self.memory.add_message("user", user_message)
        self.metadata["message_count"] += 1
        
        # Get conversation context
        context_messages = self.memory.get_context_for_llm(include_summary=True, recent_count=10)
        
        if not context_messages or context_messages[0]["role"] != "system":
            context_messages.insert(0, {"role": "system", "content": self.system_prompt})
        
        try:
            response = self.llm.chat(
                messages=context_messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            full_response = ""
            
            if response.get("streaming"):
                stream = response["stream"]
                
                if self.llm.provider in ["openai", "groq"]:
                    for chunk in stream:
                        if chunk.choices[0].delta.content:
                            content = chunk.choices[0].delta.content
                            full_response += content
                            yield content
                
                elif self.llm.provider == "gemini":
                    for chunk in stream:
                        if chunk.text:
                            full_response += chunk.text
                            yield chunk.text
            
            # Add complete response to memory
            if full_response:
                self.memory.add_message("assistant", full_response)
        
        except Exception as e:
            error_message = f"Error: {str(e)}"
            yield error_message
    
    def classify_intent(self, message: str) -> Dict[str, Any]:
        """
        Classify user intent using LLM.
        
        Args:
            message: User message
            
        Returns:
            Intent classification result
        """
        prompt = INTENT_CLASSIFICATION_PROMPT.format(query=message)
        
        try:
            result = self.llm.generate_text(prompt, temperature=0.1, max_tokens=50)
            
            # Parse result
            if "|" in result:
                intent, confidence = result.strip().split("|")
                return {
                    "intent": intent.strip(),
                    "confidence": float(confidence.strip())
                }
            else:
                return {
                    "intent": result.strip(),
                    "confidence": 0.5
                }
        except Exception as e:
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "error": str(e)
            }
    
    def get_memory_summary(self) -> str:
        """
        Get a summary of the conversation memory.
        
        Returns:
            Memory summary text
        """
        return self.memory.generate_memory_summary()
    
    def get_key_facts(self) -> List[str]:
        """
        Extract key facts from conversation.
        
        Returns:
            List of key facts
        """
        return self.memory.extract_key_facts()
    
    def search_memory(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search conversation memory.
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            List of relevant messages
        """
        return self.memory.search_memory(query, top_k)
    
    def get_conversation_history(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """
        Get conversation history.
        
        Args:
            limit: Limit number of messages
            
        Returns:
            List of messages
        """
        return self.memory.get_messages(limit=limit, include_system=False)
    
    def clear_conversation(self):
        """Clear conversation history."""
        self.memory.clear_memory()
        # Re-add system prompt
        self.memory.add_message("system", self.system_prompt)
        self.metadata["message_count"] = 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get chatbot statistics.
        
        Returns:
            Statistics dictionary
        """
        memory_stats = self.memory.get_statistics()
        
        return {
            "session": self.metadata,
            "memory": memory_stats,
            "current_provider": self.llm.provider,
            "current_model": self.llm.model
        }
    
    def export_conversation(self) -> Dict[str, Any]:
        """
        Export full conversation.
        
        Returns:
            Conversation data
        """
        return {
            "session_id": self.session_id,
            "metadata": self.metadata,
            "memory": self.memory.export_history()
        }
    
    def import_conversation(self, data: Dict[str, Any]):
        """
        Import conversation from export.
        
        Args:
            data: Exported conversation data
        """
        self.session_id = data.get("session_id", self.session_id)
        self.metadata = data.get("metadata", self.metadata)
        if "memory" in data:
            self.memory.import_history(data["memory"])
    
    def switch_provider(self, provider: str, model: Optional[str] = None):
        """
        Switch LLM provider.
        
        Args:
            provider: New provider name
            model: Optional model name
        """
        self.llm.switch_provider(provider, model)
        self.metadata["provider"] = provider
        self.metadata["model"] = model or self.llm.model
    
    def switch_model(self, model: str):
        """
        Switch model within same provider.
        
        Args:
            model: Model name
        """
        self.llm.switch_model(model)
        self.metadata["model"] = model
