from services.sentiment_service import assess_message


def analyze_text(message: str) -> dict:
    return assess_message(message)
