from services.llm_service import (
    LlmServiceError,
    generate_chat_response,
    is_llm_enabled,
    stream_chat_response,
)

def build_support_response(message: str, assessment: dict, resources: list[dict]) -> str:
    summary = _summarize_message(message)
    categories = assessment.get("resource_categories", [])
    primary_category = next((category for category in categories if category != "general"), "general")
    acknowledgement = _build_acknowledgement(summary=summary, sentiment=assessment.get("sentiment", "neutral"))

    resource_hint = ""
    if resources:
        resource = resources[0]
        description = resource.get("description", "").strip()
        resource_hint = f" One option you could explore is {resource['title']}."
        if description:
            resource_hint += f" {description}"

    if assessment["risk_level"] == "high":
        return (
            f"I'm really sorry you're carrying this right now. From what you shared about {summary}, "
            "I can hear that you're in a very difficult place, and your feelings matter. "
            "While I'm here to support you with coping strategies and resources, what you're experiencing requires immediate, real human support from someone who can truly help. "
            "I can't provide emergency intervention, but you deserve care from a trusted person, whether that's a campus counsellor, a close friend or family member, or a local emergency helpline. "
            "If you're in immediate danger, please reach out to emergency services right away. You are not alone in this, and there are real people ready to support you through this moment."
        )

    if assessment["risk_level"] == "medium":
        guidance = _category_guidance(primary_category)
        return (
            f"{acknowledgement} "
            "Those feelings are valid, and reaching out is a strong step. "
            f"Let's start with something practical: {guidance} "
            "If that feels manageable, try it for a minute or two and notice whether the intensity comes down even slightly."
            f"{resource_hint}"
        )

    return (
        f"{acknowledgement} "
        "Reaching out is a strong first step, whether you're looking for coping strategies, trying to understand your emotions, or simply needing a place to pause and reflect. "
        f"We can explore small next steps connected to {primary_category}, practice mood check-ins to track how you're feeling over time, "
        "and connect you with support resources tailored to what you need. "
        "Remember, you don't have to navigate this alone. Whenever you need to talk, check in on your mood, or learn about resources, I'm here for you."
    )


def generate_support_response(
    *,
    message: str,
    assessment: dict,
    resources: list[dict],
    user=None,
) -> dict:
    fallback_text = build_support_response(message=message, assessment=assessment, resources=resources)

    if assessment["risk_level"] == "high" or not is_llm_enabled():

        return {
            "content": fallback_text,
            "source": "fallback" if assessment["risk_level"] == "high" else "rule_engine",
            "fallback_used": assessment["risk_level"] == "high",
        }

    try:
        content = generate_chat_response(
            system_prompt=_build_system_prompt(assessment=assessment, resources=resources, user=user),
            user_message=message,
        )
    except LlmServiceError:
        return {
            "content": fallback_text,
            "source": "fallback",
            "fallback_used": True,
        }

    return {
        "content": content,
        "source": "ai_service",
        "fallback_used": False,
    }


def stream_support_response(
    *,
    message: str,
    assessment: dict,
    resources: list[dict],
    user=None,
):
    fallback_text = build_support_response(message=message, assessment=assessment, resources=resources)

    if assessment["risk_level"] == "high" or not is_llm_enabled():
        yield {
            "content": fallback_text,
            "source": "fallback" if assessment["risk_level"] == "high" else "rule_engine",
            "fallback_used": assessment["risk_level"] == "high",
        }
        return

    try:
        content_parts = []
        emitted_chunk = False
        for chunk in stream_chat_response(
            system_prompt=_build_system_prompt(assessment=assessment, resources=resources, user=user),
            user_message=message,
        ):
            if chunk:
                emitted_chunk = True
                content_parts.append(chunk)
                yield {
                    "content": chunk,
                    "source": "ai_service",
                    "fallback_used": False,
                }

        full_content = "".join(content_parts).strip()
        if not full_content:
            raise LlmServiceError("The provider returned an empty streamed message.")
    except LlmServiceError:
        if emitted_chunk:
            return
        yield {
            "content": fallback_text,
            "source": "fallback",
            "fallback_used": True,
        }


def _build_system_prompt(*, assessment: dict, resources: list[dict], user=None) -> str:
    display_name = ""
    if user and getattr(user, "display_name", ""):
        display_name = user.display_name
    elif user and getattr(user, "username", ""):
        display_name = user.username

    resource_lines = []
    for resource in resources[:3]:
        resource_lines.append(
            f"- {resource['title']}: {resource['description']}"
            + (f" ({resource['url']})" if resource.get("url") else "")
        )

    prompt = [
        "You are a compassionate and supportive mental health chatbot for students.",
        "Do not diagnose, do not claim to be a therapist, and do not invent crisis hotlines.",
        "Write thoughtful, warm, and detailed responses in full paragraphs. Aim for 2-3 substantial paragraphs.",
        "Answer the student's actual question directly before adding broader reassurance when they ask for advice or information.",
        "Do not repeatedly begin responses with 'thank you for sharing' or similar stock phrases.",
        "Provide practical, concrete next steps and coping strategies.",
        "Show genuine empathy and validate their feelings before offering advice.",
        "If the message appears risky, strongly encourage reaching out to trusted human support.",
        f"Detected risk level: {assessment['risk_level']}.",
        f"Detected sentiment: {assessment['sentiment']}.",
        f"Suggested support categories: {', '.join(assessment['resource_categories'])}.",
    ]
    if display_name:
        prompt.append(f"The student is signed in as {display_name}.")
    if resource_lines:
        prompt.append("Relevant support resources:")
        prompt.extend(resource_lines)
    else:
        prompt.append("No resource records were matched for this message.")
    return "\n".join(prompt)


def _summarize_message(message: str) -> str:
    cleaned = " ".join(message.strip().split())
    if not cleaned:
        return "what's been on your mind"
    words = cleaned.split()
    snippet = " ".join(words[:10]).rstrip(".,!?")
    return snippet if len(words) <= 10 else f"{snippet}..."


def _category_guidance(category: str) -> str:
    if category == "stress":
        return (
            "try picking just one small task for the next 10 minutes and give yourself permission to ignore the rest until that timer ends."
        )
    if category == "anxiety":
        return (
            "try a grounding exercise by naming five things you can see, four you can feel, three you can hear, two you can smell, and one you can taste."
        )
    if category == "crisis":
        return "please reach out to immediate human support right now."
    return (
        "try taking one slow breath, unclenching your shoulders, and writing down the main thing that feels hardest right now."
    )


def _build_acknowledgement(*, summary: str, sentiment: str) -> str:
    if sentiment == "negative":
        return f"It sounds like {summary} has been feeling heavy for you, and you deserve support with it."
    if sentiment == "positive":
        return f"It sounds like {summary} has been meaningful for you, and we can build on that."
    return f"It sounds like {summary} is what you're trying to work through right now, and I'm here with you."
