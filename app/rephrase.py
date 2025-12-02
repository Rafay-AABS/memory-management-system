# app/rephrase.py
import re

CONTRACTIONS = {
    "dont":"don't","cant":"can't","wont":"won't","im":"I'm","ive":"I've"
}

def simple_rephrase(q: str) -> str:
    q = q.strip()
    # fix repeated whitespace
    q = re.sub(r"\s+", " ", q)
    # simple lowercase fix for beginning
    q = q[0].upper() + q[1:] if q else q
    # expand simple contractions
    words = q.split()
    words = [CONTRACTIONS.get(w.lower(), w) for w in words]
    q = " ".join(words)
    # ensure it ends with ? if it looks like a question
    if q.lower().startswith(("how","what","why","when","where","who","should","can","do","does","did","is","are")) and not q.endswith("?"):
        q = q + "?"
    return q
