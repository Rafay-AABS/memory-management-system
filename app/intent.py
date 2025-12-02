# app/intent.py
from typing import List, Dict

INTENT_KEYWORDS = {
    "Search / Information Retrieval": ["search", "find", "lookup"],
    "Memory Update Request": ["remember", "forget", "store", "save"],
    "Task Execution": ["create", "build", "generate", "make"],
    "Tool Invocation": ["api", "run", "execute"],
    "Chat": ["hi", "hello", "hey"],
}

def classify_intent(query: str, history: List[str]) -> Dict[str, any]:
    q = query.lower()
    scores = {k: 0 for k in INTENT_KEYWORDS}

    for label, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in q:
                scores[label] += 1

    # question shape default → search
    if query.endswith("?"):
        scores["Search / Information Retrieval"] += 0.7

    best = max(scores, key=scores.get)
    confidence = round(scores[best] / (sum(scores.values()) + 1e-6), 2)

    return {
        "intent_label": best,
        "confidence_score": float(confidence)
    }
