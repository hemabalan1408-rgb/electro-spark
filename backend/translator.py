from deep_translator import GoogleTranslator

SUPPORTED_LANGUAGES = {
    "en": "English",
    "ta": "Tamil (தமிழ்)",
    "hi": "Hindi (हिंदी)",
    "te": "Telugu (తెలుగు)",
    "kn": "Kannada (ಕನ್ನಡ)",
    "ml": "Malayalam (മലയാളം)",
    "mr": "Marathi (मराठी)",
    "bn": "Bengali (বাংলা)",
    "gu": "Gujarati (ગુજρаτী)",
    "pa": "Punjabi (ਪੰਜਾਬੀ)",
    "ur": "Urdu (اردو)"
}

LANG_CODE_MAP = {
    "ta": "tamil", "hi": "hindi", "te": "telugu",
    "kn": "kannada", "ml": "malayalam", "mr": "marathi",
    "bn": "bengali", "gu": "gujarati", "pa": "punjabi",
    "ur": "urdu", "en": "english"
}

UNICODE_RANGES = {
    "ta": ('\u0B80', '\u0BFF'),
    "hi": ('\u0900', '\u097F'),
    "te": ('\u0C00', '\u0C7F'),
    "kn": ('\u0C80', '\u0CFF'),
    "ml": ('\u0D00', '\u0D7F'),
    "gu": ('\u0A80', '\u0AFF'),
    "pa": ('\u0A00', '\u0A7F'),
    "bn": ('\u0980', '\u09FF'),
}


def detect_language(text: str) -> str:
    counts = {
        lang: sum(1 for c in text if lo <= c <= hi)
        for lang, (lo, hi) in UNICODE_RANGES.items()
    }
    best = max(counts, key=counts.get)
    return best if counts[best] > 0 else "en"


def translate_to_english(text: str) -> tuple[str, str]:
    detected = detect_language(text)
    if detected == "en":
        return text, "en"
    try:
        src = LANG_CODE_MAP.get(detected, "tamil")
        result = GoogleTranslator(source=src, target="english").translate(text)
        return result, detected
    except Exception:
        return text, detected


def translate_from_english(text: str, target: str) -> str:
    if target == "en":
        return text
    try:
        tgt = LANG_CODE_MAP.get(target, "english")
        # Split into chunks if text is long (API limit ~5000 chars)
        if len(text) > 4000:
            parts = [text[i:i+3500] for i in range(0, len(text), 3500)]
            translated_parts = [
                GoogleTranslator(source="english", target=tgt).translate(p)
                for p in parts
            ]
            return " ".join(translated_parts)
        return GoogleTranslator(source="english", target=tgt).translate(text)
    except Exception:
        return text  # Fallback to English


def get_supported_languages() -> dict:
    return SUPPORTED_LANGUAGES
