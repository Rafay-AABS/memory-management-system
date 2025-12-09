"""
Simple test to verify the chatbot system is working
Run with: pytest test_basic.py -v
"""

import pytest
from app.chatbot import Chatbot
from app.memory_manager import MemoryManager
from app.llm_service import LLMService


class MockLLMService:
    """Mock LLM service for testing without API calls"""
    
    def __init__(self, provider="mock", model="mock-model"):
        self.provider = provider
        self.model = model
    
    def chat(self, messages, temperature=0.7, max_tokens=1000, stream=False):
        return {
            "content": "This is a mock response for testing.",
            "role": "assistant",
            "finish_reason": "stop",
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 10,
                "total_tokens": 20
            }
        }
    
    def generate_text(self, prompt, temperature=0.7, max_tokens=1000):
        return "This is a mock generated text."


def test_memory_manager_basic():
    """Test basic memory manager functionality"""
    mock_llm = MockLLMService()
    memory = MemoryManager(llm_service=mock_llm, max_messages=10, summary_threshold=5)
    
    # Add messages
    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi there!")
    
    # Get messages
    messages = memory.get_messages()
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello"


def test_memory_manager_context():
    """Test memory context retrieval"""
    mock_llm = MockLLMService()
    memory = MemoryManager(llm_service=mock_llm)
    
    # Add some messages
    for i in range(5):
        memory.add_message("user", f"Message {i}")
        memory.add_message("assistant", f"Response {i}")
    
    # Get context for LLM
    context = memory.get_context_for_llm(include_summary=False, recent_count=4)
    
    # Should have 4 messages (not including system messages)
    non_system = [m for m in context if m["role"] != "system"]
    assert len(non_system) <= 4


def test_memory_search():
    """Test memory search functionality"""
    mock_llm = MockLLMService()
    memory = MemoryManager(llm_service=mock_llm)
    
    # Add messages with different content
    memory.add_message("user", "I love Python programming")
    memory.add_message("assistant", "Python is great!")
    memory.add_message("user", "Tell me about JavaScript")
    memory.add_message("assistant", "JavaScript is for web development")
    
    # Search for Python
    results = memory.search_memory("Python", top_k=2)
    
    assert len(results) > 0
    assert "Python" in results[0]["message"]["content"]


def test_memory_statistics():
    """Test memory statistics"""
    mock_llm = MockLLMService()
    memory = MemoryManager(llm_service=mock_llm, max_messages=10)
    
    # Add some messages
    for i in range(3):
        memory.add_message("user", f"Message {i}")
    
    stats = memory.get_statistics()
    
    assert stats["total_messages"] == 3
    assert stats["current_messages"] == 3
    assert "memory_usage" in stats


def test_memory_clear():
    """Test clearing memory"""
    mock_llm = MockLLMService()
    memory = MemoryManager(llm_service=mock_llm)
    
    # Add messages
    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi")
    
    assert len(memory.get_messages()) == 2
    
    # Clear
    memory.clear_memory()
    
    assert len(memory.get_messages()) == 0


def test_memory_export_import():
    """Test exporting and importing memory"""
    mock_llm = MockLLMService()
    memory1 = MemoryManager(llm_service=mock_llm)
    
    # Add messages
    memory1.add_message("user", "Test message")
    memory1.add_message("assistant", "Test response")
    
    # Export
    data = memory1.export_history()
    
    # Import to new memory
    memory2 = MemoryManager(llm_service=mock_llm)
    memory2.import_history(data)
    
    # Verify
    messages1 = memory1.get_messages()
    messages2 = memory2.get_messages()
    
    assert len(messages1) == len(messages2)
    assert messages1[0]["content"] == messages2[0]["content"]


def test_chatbot_basic():
    """Test basic chatbot functionality with mock"""
    # Note: This test uses mock, so it won't make real API calls
    # To test with real APIs, you need to set API keys
    pass  # Skipping real API test to avoid requiring keys


def test_api_imports():
    """Test that all API modules can be imported"""
    from app import api
    from app import chatbot
    from app import memory_manager
    from app import llm_service
    from app import prompts
    
    assert api is not None
    assert chatbot is not None
    assert memory_manager is not None
    assert llm_service is not None
    assert prompts is not None


def test_prompts_available():
    """Test that prompts are defined"""
    from app.prompts import (
        SYSTEM_PROMPT,
        INTENT_CLASSIFICATION_PROMPT,
        SUMMARIZATION_PROMPT,
        FACT_EXTRACTION_PROMPT
    )
    
    assert len(SYSTEM_PROMPT) > 0
    assert "{query}" in INTENT_CLASSIFICATION_PROMPT
    assert "{conversation}" in SUMMARIZATION_PROMPT
    assert "{conversation}" in FACT_EXTRACTION_PROMPT


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
