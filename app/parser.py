# app/parser.py
import json
from datetime import datetime
from typing import Dict, Any

REQUIRED_KEYS = {"input", "current", "history"}

def load_and_validate(json_str_or_obj) -> Dict[str, Any]:
    if isinstance(json_str_or_obj, str):
        data = json.loads(json_str_or_obj)
    else:
        data = json_str_or_obj

    # basic shape checks
    missing = REQUIRED_KEYS - set(data.keys())
    if missing:
        raise ValueError(f"missing keys: {missing}")

    # validate timestamps (best effort)
    def _is_iso(ts):
        try:
            datetime.fromisoformat(ts)
            return True
        except Exception:
            return False

    if "timestamp" in data["current"] and not _is_iso(data["current"]["timestamp"]):
        raise ValueError("current.timestamp must be ISO format")

    for h in data.get("history", []):
        if "timestamp" in h and not _is_iso(h["timestamp"]):
            raise ValueError("history[].timestamp must be ISO format")

    return data
