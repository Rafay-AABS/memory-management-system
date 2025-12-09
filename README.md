# Chatbot Memory Management System

🤖 An intelligent LLM-based chatbot with advanced conversation memory management. Supports multiple AI providers (OpenAI, Groq, Gemini) with automatic conversation summarization, context retrieval, and persistent memory across sessions.

## 🌟 Features

### Core Capabilities
- **Multi-Provider Support**: Seamlessly switch between OpenAI, Groq, and Gemini APIs
- **Intelligent Memory Management**: Automatic conversation summarization and context compression
- **Session-Based Conversations**: Maintain multiple independent chat sessions
- **Context-Aware Responses**: LLM automatically retrieves relevant past context
- **Memory Search**: Search through conversation history for specific topics
- **Fact Extraction**: Automatically extract and store key facts from conversations
- **Streaming Support**: Real-time streaming responses for better UX
- **Export/Import**: Save and restore conversation sessions

### Memory Features
- **Automatic Summarization**: Condenses old messages when memory threshold is reached
- **Smart Context Window**: Includes relevant summaries + recent messages for LLM
- **Key Facts Extraction**: LLM extracts important facts from conversations
- **Memory Search**: Find relevant past messages by semantic similarity
- **Usage Statistics**: Track memory usage and conversation metrics

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd memory-management-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file with your API keys:

```env
# Required: At least one API key
OPENAI_API_KEY=sk-your-openai-key
GROQ_API_KEY=gsk_your-groq-key
GEMINI_API_KEY=your-gemini-key

# Optional: Server configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true
```

### Running the Server

```bash
python main.py
```

The server will start at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## 📖 API Usage

### Basic Chat

```python
import requests

# Start a conversation
response = requests.post("http://localhost:8000/chat", json={
    "message": "Hello! I'm working on a Python project.",
    "provider": "openai",  # or "groq", "gemini"
    "temperature": 0.7
})

print(response.json())
# {
#   "response": "Hello! I'd be happy to help...",
#   "session_id": "abc123...",
#   "timestamp": "2025-12-09T10:30:00",
#   "metadata": {...}
# }
```

### Continue Conversation

```python
# Use the same session_id to continue
response = requests.post("http://localhost:8000/chat", json={
    "message": "Can you remind me what we discussed?",
    "session_id": "abc123..."  # Same session
})
```

### Streaming Responses

```python
response = requests.post("http://localhost:8000/chat", json={
    "message": "Tell me a story",
    "stream": True
}, stream=True)

for line in response.iter_lines():
    if line:
        print(line.decode('utf-8'))
```

### Memory Management

```python
# Get conversation summary
summary = requests.get("http://localhost:8000/memory/abc123/summary")
print(summary.json())

# Extract key facts
facts = requests.get("http://localhost:8000/memory/abc123/facts")
print(facts.json())

# Search conversation history
results = requests.post("http://localhost:8000/search/abc123", params={
    "query": "Python project",
    "top_k": 5
})
print(results.json())
```

### Session Management

```python
# Create new session with custom settings
session = requests.post("http://localhost:8000/sessions/new", json={
    "provider": "groq",
    "model": "llama-3.1-70b-versatile",
    "system_prompt": "You are a helpful coding assistant."
})

# List all sessions
sessions = requests.get("http://localhost:8000/sessions")

# Delete session
requests.delete("http://localhost:8000/sessions/abc123")
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      API Layer                          │
│  (FastAPI - REST endpoints for chat & management)      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Chatbot Engine                         │
│  (Session management, conversation orchestration)       │
└────────┬───────────────────────────────┬────────────────┘
         │                               │
┌────────▼──────────────┐   ┌────────────▼───────────────┐
│   Memory Manager      │   │     LLM Service            │
│ • Store messages      │   │ • OpenAI client            │
│ • Summarization       │   │ • Groq client              │
│ • Context retrieval   │   │ • Gemini client            │
│ • Search & facts      │   │ • Unified interface        │
└───────────────────────┘   └────────────────────────────┘
```

### Components

- **`app/api.py`**: FastAPI endpoints for chatbot operations
- **`app/chatbot.py`**: Main chatbot engine with session management
- **`app/memory_manager.py`**: Conversation memory with LLM-based summarization
- **`app/llm_service.py`**: Unified interface for multiple LLM providers
- **`app/prompts.py`**: System prompts and templates
- **`app/models.py`**: Provider configurations and metadata
- **`app/settings.py`**: Application settings management

## 🔧 Configuration

### Model Providers

#### OpenAI
- **Models**: `gpt-4o`, `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
- **Best For**: High-quality responses, general purpose
- **Required**: `OPENAI_API_KEY`

#### Groq
- **Models**: `llama-3.1-70b-versatile`, `llama-3.1-8b-instant`, `mixtral-8x7b-32768`
- **Best For**: Ultra-fast inference, cost-effective
- **Required**: `GROQ_API_KEY`

#### Gemini
- **Models**: `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-1.0-pro`
- **Best For**: Long context, multimodal tasks
- **Required**: `GEMINI_API_KEY`

### Memory Configuration

Edit `data/model_config.json`:

```json
{
  "default_provider": "openai",
  "memory_settings": {
    "max_messages": 50,
    "summary_threshold": 20,
    "context_window": 10
  }
}
```

## 📚 API Reference

### Chat Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Send message and get response |
| `/sessions/new` | POST | Create new chat session |
| `/sessions` | GET | List all sessions |
| `/sessions/{id}` | DELETE | Delete session |

### Memory Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/history/{id}` | GET | Get conversation history |
| `/history/{id}/clear` | POST | Clear conversation |
| `/memory/{id}/summary` | GET | Get memory summary |
| `/memory/{id}/facts` | GET | Extract key facts |
| `/search/{id}` | POST | Search memory |
| `/stats/{id}` | GET | Get session statistics |

### Management Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/export/{id}` | GET | Export conversation |
| `/import` | POST | Import conversation |
| `/provider/{id}/switch` | POST | Switch LLM provider |
| `/health` | GET | Health check |

## 💡 Usage Examples

### Example 1: Coding Assistant with Memory

```python
import requests

url = "http://localhost:8000"

# Start coding session
r1 = requests.post(f"{url}/chat", json={
    "message": "I'm building a REST API with FastAPI",
    "provider": "openai"
})
session_id = r1.json()["session_id"]

# Continue - chatbot remembers context
r2 = requests.post(f"{url}/chat", json={
    "message": "How do I add authentication?",
    "session_id": session_id
})

# Later - retrieve what was discussed
summary = requests.get(f"{url}/memory/{session_id}/summary")
print(summary.json()["summary"])
```

### Example 2: Multi-Session Management

```python
# Session 1: Work project
work = requests.post(f"{url}/sessions/new", json={
    "provider": "groq",
    "system_prompt": "You are a Python expert helping with a work project."
})
work_id = work.json()["session_id"]

# Session 2: Personal learning
learn = requests.post(f"{url}/sessions/new", json={
    "provider": "openai",
    "system_prompt": "You are a patient tutor teaching machine learning."
})
learn_id = learn.json()["session_id"]

# Chat in different contexts
requests.post(f"{url}/chat", json={
    "message": "Review this production code",
    "session_id": work_id
})

requests.post(f"{url}/chat", json={
    "message": "Explain backpropagation simply",
    "session_id": learn_id
})
```

### Example 3: Python SDK Usage

```python
from app.chatbot import Chatbot

# Initialize chatbot
bot = Chatbot(provider="openai", model="gpt-4o")

# Chat
response = bot.chat("Hello! Help me with Python.")
print(response["response"])

# Continue conversation
response = bot.chat("What's a decorator?")
print(response["response"])

# Get conversation summary
summary = bot.get_memory_summary()
print(summary)

# Extract facts
facts = bot.get_key_facts()
for fact in facts:
    print(f"• {fact}")

# Export for later
data = bot.export_conversation()
# Save data to file or database

# Import later
bot2 = Chatbot()
bot2.import_conversation(data)
```

## 🔍 How Memory Works

### Memory Lifecycle

1. **Storage**: Messages stored in deque with configurable max size
2. **Threshold Check**: When messages exceed threshold (default: 20)
3. **Summarization**: LLM summarizes older messages
4. **Compression**: Summarized messages removed, summary stored
5. **Context Building**: Recent messages + summaries sent to LLM

### Context Window

```
┌──────────────────────────────────────┐
│  System Prompt                       │
├──────────────────────────────────────┤
│  Summary 1 (messages 1-20)           │
│  Summary 2 (messages 21-40)          │
├──────────────────────────────────────┤
│  Recent Message 1 (user)             │
│  Recent Message 2 (assistant)        │
│  Recent Message 3 (user)             │
│  ...                                 │
│  Current Message (user)              │
└──────────────────────────────────────┘
```

## 🧪 Testing

### Run Tests

```bash
pytest tests/
```

### Manual Testing with cURL

```bash
# Start conversation
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "provider": "openai"}'

# Continue conversation (use session_id from above)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What did we discuss?", "session_id": "abc123..."}'

# Get history
curl http://localhost:8000/history/abc123...

# Get summary
curl http://localhost:8000/memory/abc123.../summary
```

## 🐛 Troubleshooting

### API Key Issues

```
Error: OpenAI API key not found
```

**Solution**: Ensure `.env` file exists with valid API key:
```bash
echo "OPENAI_API_KEY=sk-your-key" > .env
```

### Import Errors

```
ImportError: No module named 'openai'
```

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Memory Issues

```
Response doesn't include past context
```

**Solution**: Verify session_id is being passed correctly. Each session maintains separate memory.

## 📊 Performance

### Provider Comparison

| Provider | Speed | Cost | Context | Best For |
|----------|-------|------|---------|----------|
| Groq | ⚡️⚡️⚡️ | 💰 | 32K | Fast responses |
| GPT-3.5 | ⚡️⚡️ | 💰 | 16K | Balanced |
| GPT-4o | ⚡️ | 💰💰 | 128K | Complex tasks |
| Gemini Pro | ⚡️⚡️ | 💰💰 | 1M+ | Long context |

### Memory Efficiency

- **Max Messages**: 50 (configurable)
- **Summary Threshold**: 20 messages
- **Compression Ratio**: ~5:1 (20 messages → 1 summary)
- **Context Window**: Last 10 messages + summaries

## 🛣️ Roadmap

- [ ] Vector embeddings for semantic search
- [ ] PostgreSQL/Redis backend for persistence
- [ ] Multi-user support with authentication
- [ ] Conversation branching and forking
- [ ] Advanced analytics and insights
- [ ] WebSocket support for real-time chat
- [ ] Integration with LangChain/LlamaIndex
- [ ] Voice input/output support

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- OpenAI for GPT models
- Groq for ultra-fast inference
- Google for Gemini models
- FastAPI for the excellent web framework

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check documentation at `/docs`
- Review API reference at `/openapi.json`

---

Built with ❤️ using Python, FastAPI, and LLMs
from app.client import ModelClient

# Initialize with a provider
client = ModelClient(provider="openai")

# Switch providers easily
client.switch_provider("groq")
client.switch_provider("gemini")

# Switch models within a provider
client.switch_model("gpt-3.5-turbo")

# Check capabilities
if client.has_capability("vision"):
    print("Provider supports vision!")

# Get configuration
config = client.get_client_config()
print(config)
```

### Running the API

```bash
uvicorn app.api:app --reload
```

### Example API Request

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d @data/sample_input.json
```

## Project Structure

```
memory-management-system/
├── app/
│   ├── __init__.py
│   ├── api.py           # FastAPI endpoints
│   ├── client.py        # Model client manager
│   ├── composer.py      # Main processing logic
│   ├── intent.py        # Intent classification
│   ├── models.py        # Model provider configs
│   ├── parser.py        # Input validation
│   └── strings.py       # String constants
├── utils/
│   ├── notes.py         # Note generation
│   └── rephrase.py      # Query rephrasing
├── data/
│   ├── model_config.json
│   ├── sample_input.json
│   ├── task_execution_example.json
│   └── memory_update_example.json
├── scripts/
│   └── model_client_examples.py
├── docs/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

## Model Switching Examples

See `scripts/model_client_examples.py` for comprehensive examples:

```bash
python scripts/model_client_examples.py
```

## Configuration

Edit `data/model_config.json` to customize:
- Default provider and models
- Fallback order
- Timeout and retry settings
- Provider-specific preferences

## License

MIT