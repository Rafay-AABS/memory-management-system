# app/parser.py
import json
from datetime import datetime
from typing import Dict, Any
from . import strings

REQUIRED_KEYS = {"input", "current", "history"}

def load_and_validate(data: Dict[str, Any]) -> Dict[str, Any]:
    missing = REQUIRED_KEYS - data.keys()
    if missing:
        raise ValueError(strings.VALIDATION_REQUIRED_FIELD.format(missing))

    def is_iso(ts):
        try:
            datetime.fromisoformat(ts)
            return True
        except:
            return False

    if "timestamp" in data["current"] and not is_iso(data["current"]["timestamp"]):
        raise ValueError(strings.PARSE_INVALID_FORMAT)

    for h in data["history"]:
        if "timestamp" in h and not is_iso(h["timestamp"]):
            raise ValueError(strings.PARSE_INVALID_FORMAT)

    return data
