"""
Example usage of the Chatbot Memory Management System
Demonstrates both API and SDK usage
"""

import sys
import time
from app.chatbot import Chatbot
from app.llm_service import LLMService

def example_basic_chat():
    """Example 1: Basic chatbot usage"""
    print("\n" + "="*60)
    print("Example 1: Basic Chat")
    print("="*60)
    
    # Initialize chatbot (defaults to OpenAI)
    bot = Chatbot(provider="openai")
    
    # Have a conversation
    messages = [
        "Hi! I'm learning Python.",
        "Can you explain what a decorator is?",
        "Give me a simple example.",
    ]
    
    for msg in messages:
        print(f"\n👤 User: {msg}")
        response = bot.chat(msg)
        print(f"🤖 Bot: {response['response'][:200]}...")
        time.sleep(1)
    
    print(f"\n📊 Session ID: {bot.session_id}")

def example_memory_features():
    """Example 2: Memory management features"""
    print("\n" + "="*60)
    print("Example 2: Memory Features")
    print("="*60)
    
    bot = Chatbot(provider="openai")
    
    # Have several conversations
    topics = [
        "I'm building a REST API with FastAPI",
        "I need to add JWT authentication",
        "Should I use PostgreSQL or MongoDB?",
        "How do I deploy to AWS?",
    ]
    
    for topic in topics:
        bot.chat(topic)
        print(f"✓ Discussed: {topic}")
    
    # Get memory summary
    print("\n📝 Conversation Summary:")
    print("-" * 60)
    summary = bot.get_memory_summary()
    print(summary)
    
    # Extract key facts
    print("\n📌 Key Facts Extracted:")
    print("-" * 60)
    facts = bot.get_key_facts()
    for i, fact in enumerate(facts, 1):
        print(f"{i}. {fact}")
    
    # Search memory
    print("\n🔍 Search Results for 'authentication':")
    print("-" * 60)
    results = bot.search_memory("authentication", top_k=3)
    for result in results:
        msg = result['message']
        print(f"  • {msg['role']}: {msg['content'][:100]}...")
        print(f"    Score: {result['score']}")

def example_multi_provider():
    """Example 3: Using multiple providers"""
    print("\n" + "="*60)
    print("Example 3: Multi-Provider Support")
    print("="*60)
    
    providers = ["openai", "groq", "gemini"]
    question = "What is the capital of France?"
    
    for provider in providers:
        try:
            print(f"\n🔄 Testing {provider.upper()}...")
            bot = Chatbot(provider=provider)
            response = bot.chat(question)
            print(f"✓ Response: {response['response'][:150]}...")
            print(f"  Model: {response['metadata']['model']}")
        except Exception as e:
            print(f"✗ Error with {provider}: {str(e)[:100]}")

def example_session_management():
    """Example 4: Multiple sessions"""
    print("\n" + "="*60)
    print("Example 4: Session Management")
    print("="*60)
    
    # Create different sessions for different purposes
    work_bot = Chatbot(
        provider="openai",
        system_prompt="You are a senior software engineer helping with work projects."
    )
    
    learning_bot = Chatbot(
        provider="groq",
        system_prompt="You are a patient tutor teaching programming concepts."
    )
    
    # Chat in work context
    print("\n💼 Work Session:")
    work_response = work_bot.chat("Review this SQL query for security issues")
    print(f"Work Bot: {work_response['response'][:150]}...")
    
    # Chat in learning context
    print("\n📚 Learning Session:")
    learn_response = learning_bot.chat("Explain recursion with a simple analogy")
    print(f"Learning Bot: {learn_response['response'][:150]}...")
    
    print(f"\n✓ Work Session ID: {work_bot.session_id}")
    print(f"✓ Learning Session ID: {learning_bot.session_id}")

def example_export_import():
    """Example 5: Export and import conversations"""
    print("\n" + "="*60)
    print("Example 5: Export & Import")
    print("="*60)
    
    # Create a conversation
    bot1 = Chatbot(provider="openai")
    bot1.chat("My favorite color is blue")
    bot1.chat("I work as a software engineer")
    bot1.chat("I'm learning machine learning")
    
    print("✓ Created conversation with 3 messages")
    
    # Export
    export_data = bot1.export_conversation()
    print(f"✓ Exported conversation (session: {export_data['session_id']})")
    
    # Import to new bot
    bot2 = Chatbot()
    bot2.import_conversation(export_data)
    print("✓ Imported conversation to new bot")
    
    # Verify memory
    history = bot2.get_conversation_history()
    print(f"✓ Verified: {len(history)} messages in imported bot")
    
    # Continue conversation in new bot
    response = bot2.chat("What do you know about me?")
    print(f"\n🤖 Bot remembers: {response['response'][:200]}...")

def example_statistics():
    """Example 6: Get statistics"""
    print("\n" + "="*60)
    print("Example 6: Statistics & Monitoring")
    print("="*60)
    
    bot = Chatbot(provider="openai")
    
    # Have some conversations
    for i in range(5):
        bot.chat(f"This is message number {i+1}")
    
    # Get stats
    stats = bot.get_statistics()
    
    print("\n📊 Session Statistics:")
    print("-" * 60)
    print(f"  Session ID: {stats['session']['session_id']}")
    print(f"  Created: {stats['session']['created_at']}")
    print(f"  Provider: {stats['current_provider']}")
    print(f"  Model: {stats['current_model']}")
    print(f"  Total Messages: {stats['memory']['total_messages']}")
    print(f"  Current Messages: {stats['memory']['current_messages']}")
    print(f"  Summaries Created: {stats['memory']['summaries_created']}")
    print(f"  Memory Utilization: {stats['memory']['memory_usage']['utilization']}")

def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("🤖 Chatbot Memory Management System - Examples")
    print("="*60)
    print("\nNote: Make sure you have set your API keys in .env file")
    print("This demo will use OpenAI by default. Update if needed.")
    
    try:
        # Run examples
        example_basic_chat()
        time.sleep(2)
        
        example_memory_features()
        time.sleep(2)
        
        example_session_management()
        time.sleep(2)
        
        example_export_import()
        time.sleep(2)
        
        example_statistics()
        
        # Uncomment to test multiple providers
        # example_multi_provider()
        
        print("\n" + "="*60)
        print("✓ All examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure:")
        print("1. You have created a .env file with API keys")
        print("2. You have installed all dependencies: pip install -r requirements.txt")
        print("3. Your API keys are valid and have credit")
        sys.exit(1)

if __name__ == "__main__":
    main()
