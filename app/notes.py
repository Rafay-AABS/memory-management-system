# app/notes.py
import re
from collections import Counter
from typing import List, Dict, Any
import json

def generate_notes(history: List[Dict[str, Any]]) -> str:
    if not history:
        return "No history provided."

    queries = [q["query"] for q in history]

    # simple word frequency
    words = Counter()
    for q in queries:
        for w in re.findall(r"\w{3,}", q.lower()):
            words[w] += 1

    top_words = [w for w, _ in words.most_common(6)]
    unresolved = [q for q in queries if "?" in q or "how to" in q.lower()]

    notes = {
        "total_queries": len(queries),
        "top_topics": top_words,
        "unresolved_queries": unresolved[-5:]
    }

    return json.dumps(notes, ensure_ascii=False)
