# 🚀 Setup Instructions

## Prerequisites

- Python 3.8+ installed
- At least one LLM API key (OpenAI, Groq, or Gemini)
- Git (for cloning)

## Installation Steps

### 1. Navigate to Project Directory

```powershell
cd "D:\.Work\AABS\Memory Management System\memory-management-system"
```

### 2. Activate Virtual Environment

The virtual environment is already created:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

All dependencies are already installed, but if you need to reinstall:

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file (copy from `.env.example`):

```powershell
Copy-Item .env.example .env
```

Then edit `.env` and add your API keys:

```env
# Add at least one API key
OPENAI_API_KEY=sk-your-openai-key-here
GROQ_API_KEY=gsk-your-groq-key-here
GEMINI_API_KEY=your-gemini-key-here

# Optional: Server configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true
```

### 5. Test Installation

Run the tests to verify everything works:

```powershell
python -m pytest tests/test_basic.py -v
```

You should see:
```
========== 9 passed in X.XXs ==========
```

### 6. Start the Server

```powershell
python main.py
```

You should see:
```
🤖 Chatbot Memory Management System
📡 Server: http://0.0.0.0:8000
📚 API Docs: http://0.0.0.0:8000/docs
```

### 7. Test the API

Open a new terminal and test:

```powershell
# Simple test
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{\"message\": \"Hello!\"}'

# Or use the examples
python examples.py
```

## Getting API Keys

### OpenAI
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create new secret key
5. Copy and add to `.env` as `OPENAI_API_KEY`

### Groq
1. Go to https://console.groq.com/
2. Sign up or log in
3. Go to API Keys section
4. Create new API key
5. Copy and add to `.env` as `GROQ_API_KEY`

### Gemini
1. Go to https://aistudio.google.com/
2. Sign in with Google account
3. Click "Get API key"
4. Create new API key
5. Copy and add to `.env` as `GEMINI_API_KEY`

## Verification Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list` shows openai, groq, google-generativeai)
- [ ] `.env` file created with at least one API key
- [ ] Tests pass (`pytest tests/test_basic.py -v`)
- [ ] Server starts (`python main.py`)
- [ ] API accessible (http://localhost:8000/docs)

## Troubleshooting

### Issue: Module not found

```powershell
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: API key error

```
Error: OpenAI API key not found
```

**Solution**: 
1. Check `.env` file exists in project root
2. Verify API key is correct (no extra spaces)
3. Make sure the key starts with the correct prefix (sk- for OpenAI, gsk_ for Groq)
4. Restart the server after editing `.env`

### Issue: Tests fail

```powershell
# Check Python version
python --version  # Should be 3.8+

# Reinstall test dependencies
pip install pytest

# Run tests with more detail
python -m pytest tests/test_basic.py -vv
```

### Issue: Server won't start

```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Use a different port
$env:PORT="8001"
python main.py
```

### Issue: Import errors

Make sure you're in the project directory and virtual environment is activated:

```powershell
# Check current directory
pwd
# Should be: D:\.Work\AABS\Memory Management System\memory-management-system

# Check virtual environment
python -c "import sys; print(sys.prefix)"
# Should point to .venv directory
```

## Quick Reference

### Start Server
```powershell
python main.py
```

### Run Tests
```powershell
python -m pytest tests/test_basic.py -v
```

### Run Examples
```powershell
python examples.py
```

### Access API Docs
```
http://localhost:8000/docs
```

### Check Logs
Server logs appear in the terminal where you ran `python main.py`

## Next Steps

1. ✅ **Installation Complete** - You're done with setup!
2. 📖 **Read Documentation** - Check `README.md` for full API reference
3. 🎮 **Try Examples** - Run `python examples.py` to see it in action
4. 🔧 **Customize** - Modify `app/prompts.py` to customize behavior
5. 🚀 **Build** - Start integrating the API into your application

## Support

- **Documentation**: README.md, QUICKSTART.md, CHANGES.md
- **API Reference**: http://localhost:8000/docs
- **Tests**: Run `pytest tests/ -v` to verify functionality
- **Examples**: Check `examples.py` for usage patterns

---

**Status**: ✅ System is ready to use!

For more information, see:
- `README.md` - Complete documentation
- `QUICKSTART.md` - Quick start guide
- `CHANGES.md` - What changed from old system
- `examples.py` - Usage examples
