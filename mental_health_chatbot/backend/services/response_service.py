def build_support_response(message: str, assessment: dict, resources: list[dict]) -> str:
    if assessment["risk_level"] == "high":
        return (
            "I'm really sorry you're carrying this right now. I can't provide emergency help, "
            "but you deserve immediate support from a trusted person, campus counsellor, or local "
            "emergency helpline right away. If you're in immediate danger, please call emergency services now."
        )

    if assessment["risk_level"] == "medium":
        resource_hint = ""
        if resources:
            resource_hint = f" A good first step could be: {resources[0]['title']}."
        return (
            "It sounds like things have been heavy lately. Try one small grounding step right now: "
            "take a slow breath in for 4 seconds, hold for 4, and exhale for 6." + resource_hint
        )

    return (
        "Thank you for sharing that. I'm here to support you with coping ideas, mood check-ins, "
        "and helpful resources whenever you need them."
    )
