# utils/rephrase.py
import re
from app import strings

def simple_rephrase(query: str) -> str:
    query = re.sub(r"\s+", " ", query.strip())
    if not query:
        return ""

    query = query[0].upper() + query[1:]

    if query.lower().startswith(("what", "why", "how", "when", "where", "who")):
        if not query.endswith("?"):
            query += "?"

    return query
