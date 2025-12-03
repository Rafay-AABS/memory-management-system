# app/composer.py
from .parser import load_and_validate
from .notes import generate_notes
from .rephrase import simple_rephrase
from .intent import classify_intent
from . import strings

def process_input(payload):
    data = load_and_validate(payload)

    history_queries = [h.get("query", "") for h in data["history"]]
    notes = generate_notes(data["history"])
    rephrased = simple_rephrase(data["current"]["query"])
    intent = classify_intent(data["current"]["query"], history_queries)

    return {
        "notes": notes,
        "rephrased_query": rephrased,
        "intent": intent["intent_label"],
        "confidence": intent["confidence_score"]
    }
