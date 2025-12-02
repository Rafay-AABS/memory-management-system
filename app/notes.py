# app/notes.py
import re
from collections import Counter
from typing import List, Dict, Any

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

def extract_key_phrases(text: str) -> List[str]:
    # simple heuristics: code-like tokens, capitalized phrases, hashtags
    tokens = re.findall(r"[A-Za-z0-9_/.-]{2,}", text)
    return tokens[:10]

def generate_notes(history: List[Dict[str, Any]]) -> str:
    if not history:
        return "No history provided."

    queries = [h.get("query", "") for h in history]
    joined = " ||| ".join(queries)

    emails = EMAIL_RE.findall(joined)
    common_words = Counter()
    for q in queries:
        for w in re.findall(r"\w{3,}", q.lower()):
            common_words[w] += 1

    top_words = [w for w,c in common_words.most_common(10)]
    unresolved = [q for q in queries if "?" in q or "help" in q.lower() or "how to" in q.lower()]

    notes = {
        "summary": f"{len(queries)} past queries; common topics: {', '.join(top_words[:6])}.",
        "emails_found": list(set(emails)),
        "recent_queries": queries[-5:],
        "unresolved": unresolved,
    }
    # return as short JSON-like string for readability
    import json
    return json.dumps(notes, ensure_ascii=False)
