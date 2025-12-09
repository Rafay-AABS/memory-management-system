"""
Memory Manager - LLM-based conversation memory management
Handles conversation history, summarization, and intelligent retrieval
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import deque


class MemoryManager:
    """Manages conversation memory with LLM-based summarization and retrieval."""
    
    def __init__(self, llm_service, max_messages: int = 50, summary_threshold: int = 20):
        """
        Initialize memory manager.
        
        Args:
            llm_service: Instance of LLMService for summarization
            max_messages: Maximum messages to keep in full history
            summary_threshold: Number of messages before triggering summarization
        """
        self.llm = llm_service
        self.max_messages = max_messages
        self.summary_threshold = summary_threshold
        
        # Conversation storage
        self.messages: deque = deque(maxlen=max_messages)
        self.summaries: List[str] = []
        self.metadata: Dict[str, Any] = {
            "created_at": datetime.now().isoformat(),
            "message_count": 0,
            "summary_count": 0
        }
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """
        Add a message to conversation history.
        
        Args:
            role: Message role (user/assistant/system)
            content: Message content
            metadata: Optional metadata (timestamp, etc.)
        """
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.messages.append(message)
        self.metadata["message_count"] += 1
        
        # Check if we need to summarize
        if len(self.messages) >= self.summary_threshold:
            self._trigger_summarization()
    
    def get_messages(self, limit: Optional[int] = None, include_system: bool = False) -> List[Dict[str, str]]:
        """
        Get conversation messages.
        
        Args:
            limit: Limit number of recent messages
            include_system: Whether to include system messages
            
        Returns:
            List of messages
        """
        messages = list(self.messages)
        
        if not include_system:
            messages = [m for m in messages if m["role"] != "system"]
        
        if limit:
            messages = messages[-limit:]
        
        return messages
    
    def get_context_for_llm(self, include_summary: bool = True, recent_count: int = 10) -> List[Dict[str, str]]:
        """
        Get formatted conversation context for LLM.
        
        Args:
            include_summary: Whether to include conversation summaries
            recent_count: Number of recent messages to include
            
        Returns:
            List of messages formatted for LLM
        """
        context = []
        
        # Add summaries as context
        if include_summary and self.summaries:
            summary_text = "\n\n".join(self.summaries)
            context.append({
                "role": "system",
                "content": f"Previous conversation summary:\n{summary_text}"
            })
        
        # Add recent messages (without internal metadata)
        recent_messages = list(self.messages)[-recent_count:]
        for msg in recent_messages:
            if msg["role"] != "system":  # Don't duplicate system messages
                context.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        return context
    
    def _trigger_summarization(self):
        """Trigger summarization of older messages."""
        # Get messages to summarize (older half)
        messages_to_summarize = list(self.messages)[:len(self.messages) // 2]
        
        if not messages_to_summarize:
            return
        
        # Create summarization prompt
        conversation_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in messages_to_summarize
        ])
        
        summary_prompt = f"""Summarize the following conversation concisely, capturing:
1. Main topics discussed
2. Key information shared
3. Important decisions or conclusions
4. Any action items or unresolved questions

Conversation:
{conversation_text}

Provide a clear, structured summary:"""
        
        try:
            summary = self.llm.generate_text(summary_prompt, temperature=0.3, max_tokens=500)
            self.summaries.append(summary)
            self.metadata["summary_count"] += 1
            
            # Remove summarized messages (keep recent half)
            for _ in range(len(messages_to_summarize)):
                if len(self.messages) > self.summary_threshold // 2:
                    self.messages.popleft()
        
        except Exception as e:
            print(f"Summarization failed: {e}")
    
    def search_memory(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search through conversation memory for relevant context.
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of relevant messages with scores
        """
        results = []
        query_lower = query.lower()
        
        # Simple keyword-based search (can be enhanced with embeddings)
        for msg in self.messages:
            if msg["role"] == "system":
                continue
            
            content_lower = msg["content"].lower()
            
            # Calculate simple relevance score
            score = 0
            query_words = query_lower.split()
            
            for word in query_words:
                if len(word) > 2:  # Skip short words
                    if word in content_lower:
                        score += content_lower.count(word)
            
            if score > 0:
                results.append({
                    "message": msg,
                    "score": score
                })
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    def generate_memory_summary(self) -> str:
        """
        Generate a comprehensive summary of the entire conversation.
        
        Returns:
            Summary text
        """
        if not self.messages and not self.summaries:
            return "No conversation history available."
        
        # Combine all summaries and recent messages
        context_parts = []
        
        if self.summaries:
            context_parts.append("Previous summaries:")
            context_parts.extend(self.summaries)
        
        if self.messages:
            context_parts.append("\nRecent conversation:")
            for msg in list(self.messages)[-10:]:
                context_parts.append(f"{msg['role'].upper()}: {msg['content']}")
        
        conversation_text = "\n".join(context_parts)
        
        summary_prompt = f"""Create a comprehensive summary of this conversation, including:
1. Overall context and purpose
2. Main topics covered
3. Key insights and information
4. Current state and any pending items

Conversation history:
{conversation_text}

Provide a well-organized summary:"""
        
        try:
            summary = self.llm.generate_text(summary_prompt, temperature=0.3, max_tokens=800)
            return summary
        except Exception as e:
            return f"Error generating summary: {e}"
    
    def extract_key_facts(self) -> List[str]:
        """
        Extract key facts and information from the conversation.
        
        Returns:
            List of key facts
        """
        if not self.messages:
            return []
        
        # Get all messages
        conversation_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in self.messages
            if msg["role"] != "system"
        ])
        
        facts_prompt = f"""Extract key facts, information, and important details from this conversation.
List only concrete information, decisions, or important points.
Format as a numbered list.

Conversation:
{conversation_text}

Key facts:"""
        
        try:
            facts_text = self.llm.generate_text(facts_prompt, temperature=0.2, max_tokens=500)
            # Parse the numbered list
            facts = [line.strip() for line in facts_text.split('\n') if line.strip() and any(c.isdigit() for c in line[:3])]
            return facts
        except Exception as e:
            print(f"Fact extraction failed: {e}")
            return []
    
    def clear_memory(self):
        """Clear all conversation history and summaries."""
        self.messages.clear()
        self.summaries.clear()
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "message_count": 0,
            "summary_count": 0
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get memory statistics.
        
        Returns:
            Dictionary with memory stats
        """
        return {
            "total_messages": self.metadata["message_count"],
            "current_messages": len(self.messages),
            "summaries_created": self.metadata["summary_count"],
            "created_at": self.metadata["created_at"],
            "memory_usage": {
                "messages": len(self.messages),
                "max_messages": self.max_messages,
                "utilization": f"{(len(self.messages) / self.max_messages * 100):.1f}%"
            }
        }
    
    def export_history(self) -> Dict[str, Any]:
        """
        Export full conversation history.
        
        Returns:
            Dictionary with all conversation data
        """
        return {
            "messages": list(self.messages),
            "summaries": self.summaries,
            "metadata": self.metadata,
            "statistics": self.get_statistics()
        }
    
    def import_history(self, data: Dict[str, Any]):
        """
        Import conversation history.
        
        Args:
            data: Exported conversation data
        """
        self.messages = deque(data.get("messages", []), maxlen=self.max_messages)
        self.summaries = data.get("summaries", [])
        self.metadata = data.get("metadata", self.metadata)
