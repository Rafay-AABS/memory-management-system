# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Environment

Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` and add your API key (at least one required):
```env
OPENAI_API_KEY=sk-your-key-here
# or
GROQ_API_KEY=gsk-your-key-here
# or  
GEMINI_API_KEY=your-key-here
```

### Step 3: Start the Server

```bash
python main.py
```

You should see:
```
🤖 Chatbot Memory Management System
📡 Server: http://0.0.0.0:8000
📚 API Docs: http://0.0.0.0:8000/docs
```

### Step 4: Test It!

Open another terminal and try:

**Option A: Using cURL**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Hello! Tell me about Python decorators.\"}"
```

**Option B: Using Python**
```bash
python examples.py
```

**Option C: Using the Interactive API Docs**

Open http://localhost:8000/docs in your browser and try the `/chat` endpoint.

## 💬 First Conversation

```python
import requests

# 1. Start conversation
response = requests.post("http://localhost:8000/chat", json={
    "message": "Hi! I'm learning to code."
})

session_id = response.json()["session_id"]
print(response.json()["response"])

# 2. Continue conversation (bot remembers context!)
response = requests.post("http://localhost:8000/chat", json={
    "message": "Can you suggest a project?",
    "session_id": session_id
})

print(response.json()["response"])

# 3. Check what the bot remembers
summary = requests.get(f"http://localhost:8000/memory/{session_id}/summary")
print(summary.json()["summary"])
```

## 🔧 Configuration

### Change Provider

```python
# Use Groq (fast & free tier available)
requests.post("http://localhost:8000/chat", json={
    "message": "Hello!",
    "provider": "groq"
})

# Use Gemini (good for long context)
requests.post("http://localhost:8000/chat", json={
    "message": "Hello!",
    "provider": "gemini",
    "model": "gemini-1.5-flash"
})
```

### Adjust Response Style

```python
# Creative (high temperature)
requests.post("http://localhost:8000/chat", json={
    "message": "Write a poem about coding",
    "temperature": 0.9
})

# Precise (low temperature)  
requests.post("http://localhost:8000/chat", json={
    "message": "What is 2+2?",
    "temperature": 0.1
})
```

## 📖 Key Endpoints

- **Chat**: `POST /chat` - Send messages
- **History**: `GET /history/{session_id}` - View past messages
- **Summary**: `GET /memory/{session_id}/summary` - Get conversation summary
- **Search**: `POST /search/{session_id}` - Search memory
- **Sessions**: `GET /sessions` - List all active sessions

## 🆘 Troubleshooting

### "API key not found"
- Make sure `.env` file exists in project root
- Verify API key is correct (no extra spaces)
- Restart the server after editing `.env`

### "ImportError: No module named 'openai'"
```bash
pip install -r requirements.txt
```

### "Session not found"
- Each session has a unique ID
- Session IDs are returned in the chat response
- Sessions are stored in memory (cleared on server restart)

## 🎯 Next Steps

1. **Try the Examples**: `python examples.py`
2. **Explore API Docs**: http://localhost:8000/docs
3. **Read Full Documentation**: See README.md
4. **Build Your App**: Use the REST API or import the SDK

## 📚 SDK Usage (No Server Required)

```python
from app.chatbot import Chatbot

# Create chatbot
bot = Chatbot(provider="openai")

# Chat
response = bot.chat("Hello!")
print(response["response"])

# Get history
history = bot.get_conversation_history()
for msg in history:
    print(f"{msg['role']}: {msg['content']}")
```

## 🔥 Cool Features to Try

### 1. Memory Search
Ask about something discussed earlier:
```python
bot.chat("Let's discuss Python")
# ... many messages later ...
bot.chat("What did we talk about Python?")
# Bot retrieves relevant context!
```

### 2. Multi-Session
Keep work and personal chats separate:
```python
work_session = create_session("openai")
personal_session = create_session("groq")
```

### 3. Export/Import
Save and restore conversations:
```python
data = bot.export_conversation()
# Save to file/database
# Later...
bot2 = Chatbot()
bot2.import_conversation(data)
```

---

**Ready to build?** Check the full API reference in README.md or at `/docs`! 🚀
