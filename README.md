# Memory Management System

A flexible AI-powered memory management system with support for multiple LLM providers (OpenAI, Groq, Gemini).

## Features

- **Multi-Provider Support**: Easily switch between OpenAI, Groq, and Gemini APIs
- **Intent Classification**: Automatically detect user intent from queries
- **Memory Notes**: Generate and store conversation summaries
- **Query Rephrasing**: Improve query formatting and structure
- **REST API**: FastAPI-based endpoints for easy integration

## Model Providers

### OpenAI
- **Models**: GPT-4, GPT-4 Turbo, GPT-4o, GPT-3.5 Turbo
- **Capabilities**: Chat, Completion, Embedding, Vision, Function Calling
- **Best For**: General purpose, high-quality responses

### Groq
- **Models**: Llama 3.1 70B, Llama 3.1 8B, Mixtral 8x7B, Gemma 7B
- **Capabilities**: Ultra-fast chat and completion
- **Best For**: Speed-optimized inference with open-source models

### Gemini
- **Models**: Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 1.0 Pro
- **Capabilities**: Chat, Completion, Vision, Multimodal, Code Execution
- **Best For**: Long context, multimodal tasks

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
```

### Basic Usage

```python
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