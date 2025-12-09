"""
System prompts for the chatbot memory management system
"""

SYSTEM_PROMPT = """You are a helpful AI assistant with advanced memory management capabilities.

You have access to:
1. Recent conversation history
2. Summaries of previous conversations
3. Key facts extracted from past discussions

Guidelines:
- Be helpful, concise, and accurate
- Reference previous conversations when relevant
- If you're unsure about something from past context, ask for clarification
- Maintain continuity across the conversation
- Learn from user preferences and adapt your responses

Your goal is to provide consistent, context-aware assistance while maintaining conversation coherence."""

MEMORY_EXTRACTION_PROMPT = """Analyze this conversation and extract:

1. **User Preferences**: Any stated preferences, likes, or dislikes
2. **Important Facts**: Names, dates, numbers, or key information
3. **Action Items**: Tasks or things to remember for future
4. **Context**: Background information relevant for future conversations

Conversation:
{conversation}

Extract and format the information clearly:"""

INTENT_CLASSIFICATION_PROMPT = """Classify the user's intent from this message:

Message: {query}

Choose ONE primary intent from:
1. question - User is asking for information
2. command - User wants you to perform an action
3. statement - User is sharing information
4. clarification - User is clarifying previous message
5. feedback - User is providing feedback
6. casual - Casual conversation/greeting

Respond with ONLY the intent category and confidence (0-1):
Format: intent|confidence"""

CONTEXT_RELEVANCE_PROMPT = """Given this user query, determine which past conversation topics are most relevant.

Current query: {query}

Past topics:
{topics}

Rate relevance (0-10) for each topic and explain why.
Focus on topics that would help answer the current query."""

SUMMARIZATION_PROMPT = """Summarize this conversation section concisely:

{conversation}

Include:
- Main topics discussed
- Key information exchanged  
- Important conclusions or decisions
- Any unresolved questions

Summary:"""

FACT_EXTRACTION_PROMPT = """Extract concrete facts and information from this conversation:

{conversation}

List ONLY verifiable facts, such as:
- Names, places, dates
- Technical details
- Specific numbers or measurements
- Stated preferences or requirements
- Decisions made

Format as a bullet list:"""
