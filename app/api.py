"""
API endpoints for the chatbot memory management system
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import json
from datetime import datetime

from .chatbot import Chatbot
from . import strings

app = FastAPI(
    title="Chatbot Memory Management System API",
    description="LLM-based chatbot with intelligent memory management",
    version="2.0.0"
)

# Global chatbot sessions storage
chatbot_sessions: Dict[str, Chatbot] = {}


# Pydantic models
class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Session ID (creates new if not provided)")
    provider: Optional[str] = Field("openai", description="LLM provider (openai, groq, gemini)")
    model: Optional[str] = Field(None, description="Model name")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=1.0, description="Response temperature")
    max_tokens: Optional[int] = Field(1000, gt=0, description="Maximum tokens")
    stream: Optional[bool] = Field(False, description="Stream response")


class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    metadata: Dict[str, Any]


class SessionRequest(BaseModel):
    provider: Optional[str] = Field("openai", description="LLM provider")
    model: Optional[str] = Field(None, description="Model name")
    system_prompt: Optional[str] = Field(None, description="Custom system prompt")


class SessionResponse(BaseModel):
    session_id: str
    created_at: str
    provider: str
    model: str


# Helper functions
def get_or_create_chatbot(session_id: Optional[str], provider: str, model: Optional[str]) -> Chatbot:
    """Get existing chatbot or create new one."""
    if session_id and session_id in chatbot_sessions:
        return chatbot_sessions[session_id]
    
    chatbot = Chatbot(provider=provider, model=model, session_id=session_id)
    chatbot_sessions[chatbot.session_id] = chatbot
    return chatbot


# API Endpoints

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "Chatbot Memory Management System",
        "version": "2.0.0",
        "description": "LLM-based chatbot with intelligent conversation memory",
        "endpoints": {
            "chat": "/chat",
            "sessions": "/sessions",
            "history": "/history/{session_id}",
            "memory": "/memory/{session_id}",
            "search": "/search/{session_id}",
            "stats": "/stats/{session_id}"
        }
    }


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Send a message to the chatbot.
    
    - **message**: User message
    - **session_id**: Optional session ID
    - **provider**: LLM provider (openai, groq, gemini)
    - **model**: Optional model name
    - **temperature**: Response randomness (0.0-1.0)
    - **max_tokens**: Maximum response length
    - **stream**: Stream response (returns as text/event-stream)
    """
    try:
        chatbot = get_or_create_chatbot(request.session_id, request.provider, request.model)
        
        if request.stream:
            # Return streaming response
            async def generate():
                for chunk in chatbot.stream_chat(
                    request.message,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens
                ):
                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                yield f"data: {json.dumps({'done': True, 'session_id': chatbot.session_id})}\n\n"
            
            return StreamingResponse(generate(), media_type="text/event-stream")
        
        # Regular response
        response = chatbot.chat(
            request.message,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return ChatResponse(**response)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sessions/new", response_model=SessionResponse)
def create_session(request: SessionRequest):
    """
    Create a new chat session.
    
    - **provider**: LLM provider
    - **model**: Optional model name
    - **system_prompt**: Optional custom system prompt
    """
    try:
        chatbot = Chatbot(
            provider=request.provider,
            model=request.model,
            system_prompt=request.system_prompt
        )
        chatbot_sessions[chatbot.session_id] = chatbot
        
        return SessionResponse(
            session_id=chatbot.session_id,
            created_at=chatbot.metadata["created_at"],
            provider=chatbot.llm.provider,
            model=chatbot.llm.model
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions")
def list_sessions():
    """List all active chat sessions."""
    sessions = []
    for session_id, chatbot in chatbot_sessions.items():
        sessions.append({
            "session_id": session_id,
            "created_at": chatbot.metadata["created_at"],
            "provider": chatbot.llm.provider,
            "model": chatbot.llm.model,
            "message_count": chatbot.metadata["message_count"]
        })
    return {"sessions": sessions, "count": len(sessions)}


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    """Delete a chat session."""
    if session_id not in chatbot_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    del chatbot_sessions[session_id]
    return {"message": "Session deleted", "session_id": session_id}


@app.get("/history/{session_id}")
def get_history(session_id: str, limit: Optional[int] = None):
    """
    Get conversation history for a session.
    
    - **session_id**: Session identifier
    - **limit**: Optional limit on number of messages
    """
    if session_id not in chatbot_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    chatbot = chatbot_sessions[session_id]
    history = chatbot.get_conversation_history(limit=limit)
    
    return {
        "session_id": session_id,
        "history": history,
        "count": len(history)
    }


@app.post("/history/{session_id}/clear")
def clear_history(session_id: str):
    """Clear conversation history for a session."""
    if session_id not in chatbot_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    chatbot = chatbot_sessions[session_id]
    chatbot.clear_conversation()
    
    return {"message": "Conversation cleared", "session_id": session_id}


@app.get("/memory/{session_id}/summary")
def get_memory_summary(session_id: str):
    """Get memory summary for a session."""
    if session_id not in chatbot_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    chatbot = chatbot_sessions[session_id]
    summary = chatbot.get_memory_summary()
    
    return {
        "session_id": session_id,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/memory/{session_id}/facts")
def get_key_facts(session_id: str):
    """Extract key facts from conversation."""
    if session_id not in chatbot_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    chatbot = chatbot_sessions[session_id]
    facts = chatbot.get_key_facts()
    
    return {
        "session_id": session_id,
        "facts": facts,
        "count": len(facts)
    }


@app.post("/search/{session_id}")
def search_memory(session_id: str, query: str, top_k: int = 5):
    """
    Search conversation memory.
    
    - **session_id**: Session identifier
    - **query**: Search query
    - **top_k**: Number of results to return
    """
    if session_id not in chatbot_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    chatbot = chatbot_sessions[session_id]
    results = chatbot.search_memory(query, top_k)
    
    return {
        "session_id": session_id,
        "query": query,
        "results": results,
        "count": len(results)
    }


@app.get("/stats/{session_id}")
def get_statistics(session_id: str):
    """Get statistics for a session."""
    if session_id not in chatbot_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    chatbot = chatbot_sessions[session_id]
    stats = chatbot.get_statistics()
    
    return stats


@app.get("/export/{session_id}")
def export_conversation(session_id: str):
    """Export full conversation data."""
    if session_id not in chatbot_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    chatbot = chatbot_sessions[session_id]
    data = chatbot.export_conversation()
    
    return data


@app.post("/import")
def import_conversation(data: Dict[str, Any]):
    """Import conversation data."""
    try:
        session_id = data.get("session_id")
        if not session_id:
            raise ValueError("session_id required in import data")
        
        # Create new chatbot and import
        chatbot = Chatbot()
        chatbot.import_conversation(data)
        chatbot_sessions[session_id] = chatbot
        
        return {
            "message": "Conversation imported",
            "session_id": session_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/provider/{session_id}/switch")
def switch_provider(session_id: str, provider: str, model: Optional[str] = None):
    """
    Switch LLM provider for a session.
    
    - **session_id**: Session identifier
    - **provider**: New provider (openai, groq, gemini)
    - **model**: Optional model name
    """
    if session_id not in chatbot_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    chatbot = chatbot_sessions[session_id]
    
    try:
        chatbot.switch_provider(provider, model)
        return {
            "message": "Provider switched",
            "session_id": session_id,
            "provider": provider,
            "model": model or chatbot.llm.model
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(chatbot_sessions)
    }
