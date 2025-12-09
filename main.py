"""
Chatbot Memory Management System - Main Entry Point
A LLM-based chatbot with intelligent conversation memory management
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.api import app

if __name__ == "__main__":
    import uvicorn
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print("=" * 60)
    print("🤖 Chatbot Memory Management System")
    print("=" * 60)
    print(f"📡 Server: http://{host}:{port}")
    print(f"📚 API Docs: http://{host}:{port}/docs")
    print(f"🔧 OpenAPI: http://{host}:{port}/openapi.json")
    print("=" * 60)
    print("\nSupported Providers:")
    print("  • OpenAI (gpt-4o, gpt-4, gpt-3.5-turbo)")
    print("  • Groq (llama-3.1-70b, llama-3.1-8b)")
    print("  • Gemini (gemini-1.5-pro, gemini-1.5-flash)")
    print("\n" + "=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
