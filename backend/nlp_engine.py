import json
import os
import re
from difflib import SequenceMatcher

DB_PATH = os.path.join(os.path.dirname(__file__), "legal_db.json")
with open(DB_PATH, "r", encoding="utf-8") as f:
    LEGAL_DB = json.load(f)


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def tokenize(text: str) -> list:
    return re.findall(r'\w+', text.lower())


def find_category(text: str) -> str | None:
    tokens = tokenize(text)
    scores = {}
    for cat, data in LEGAL_DB["categories"].items():
        score = 0
        for kw in data["keywords"]:
            kw_lower = kw.lower()
            if kw_lower in text.lower():
                score += 3
            elif any(similarity(tok, kw_lower) > 0.75 for tok in tokens):
                score += 1
        if score > 0:
            scores[cat] = score
    return max(scores, key=scores.get) if scores else None


def find_best_qa(text: str, category: str) -> str | None:
    if not category:
        return None
    qa_list = LEGAL_DB["categories"][category]["qa"]
    best, best_score = None, 0
    tokens = set(tokenize(text))
    for qa in qa_list:
        q_tokens = set(tokenize(qa["q"]))
        overlap = len(tokens & q_tokens) / max(len(q_tokens), 1)
        sim = similarity(text, qa["q"])
        score = (overlap * 0.6) + (sim * 0.4)
        if score > best_score:
            best_score = score
            best = qa["a"]
    return best


def is_greeting(text: str) -> bool:
    greetings = ["hello", "hi", "help", "start", "vanakkam", "வணக்கம்",
                 "நமஸ்தே", "namaste", "hey", "good morning", "good evening"]
    t = text.lower().strip()
    return any(g in t for g in greetings) or len(t) < 5


def is_emergency(text: str) -> bool:
    words = ["emergency", "urgent", "danger", "help me now", "immediately",
             "suicide", "attack", "dying", "bleeding", "fire"]
    return any(w in text.lower() for w in words)


def get_emergency_contacts() -> str:
    contacts = LEGAL_DB["emergency_contacts"]
    lines = ["🚨 <b>Emergency Contacts:</b><br>"]
    for name, number in contacts.items():
        lines.append(f"• {name}: <b>{number}</b>")
    return "<br>".join(lines)


def get_legal_response(text: str, lang: str = "en") -> str:
    if is_greeting(text):
        key = "greeting_ta" if lang == "ta" else "greeting_en"
        return LEGAL_DB["general"][key]

    if is_emergency(text):
        return get_emergency_contacts()

    category = find_category(text)
    answer = find_best_qa(text, category)

    if answer:
        return answer
    if category:
        return LEGAL_DB["categories"][category]["qa"][0]["a"]

    key = "not_found_ta" if lang == "ta" else "not_found_en"
    return LEGAL_DB["general"][key]


def get_categories() -> dict:
    return {
        k: {"icon": v["icon"], "name": k.replace("_", " ").title()}
        for k, v in LEGAL_DB["categories"].items()
    }


def get_emergency_dict() -> dict:
    return LEGAL_DB["emergency_contacts"]
