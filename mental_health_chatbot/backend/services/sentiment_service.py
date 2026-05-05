NEGATIVE_WORDS = {
    "sad",
    "stressed",
    "anxious",
    "tired",
    "burnout",
    "depressed",
    "hopeless",
    "lonely",
    "panic",
    "overwhelmed",
}

CRISIS_WORDS = {
    "suicide",
    "kill myself",
    "self harm",
    "hurt myself",
    "end my life",
}


def assess_message(message: str) -> dict:
    lowered = message.lower()
    is_crisis = any(term in lowered for term in CRISIS_WORDS)
    negative_hits = sum(1 for word in NEGATIVE_WORDS if word in lowered)

    sentiment = "positive"
    risk_level = "low"
    flagged = False
    categories = ["general"]

    if negative_hits:
        sentiment = "negative"
        risk_level = "medium"
        categories = ["stress", "anxiety"]

    if "stress" in lowered or "exam" in lowered:
        categories.append("stress")

    if "anx" in lowered or "panic" in lowered:
        categories.append("anxiety")

    if is_crisis:
        sentiment = "negative"
        risk_level = "high"
        flagged = True
        categories = ["crisis"]

    return {
        "sentiment": sentiment,
        "risk_level": risk_level,
        "flagged": flagged,
        "resource_categories": sorted(set(categories)),
    }
