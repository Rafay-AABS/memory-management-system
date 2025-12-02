# app/parser.py
import json
from datetime import datetime
from typing import Dict, Any

REQUIRED_KEYS = {"input", "current", "history"}

def load_and_validate(data: Dict[str, Any]) -> Dict[str, Any]:
    missing = REQUIRED_KEYS - data.keys()
    if missing:
        raise ValueError(f"Missing keys: {missing}")

    def is_iso(ts):
        try:
            datetime.fromisoformat(ts)
            return True
        except:
            return False

    if "timestamp" in data["current"] and not is_iso(data["current"]["timestamp"]):
        raise ValueError("current.timestamp must be ISO format")

    for h in data["history"]:
        if "timestamp" in h and not is_iso(h["timestamp"]):
            raise ValueError("history[].timestamp must be ISO format")

    return data
