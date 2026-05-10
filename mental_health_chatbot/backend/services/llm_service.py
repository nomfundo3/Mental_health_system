import json
import os
from urllib import error, request

DEFAULT_LLM_PROVIDER = "openrouter"
DEFAULT_LLM_MODEL = "openrouter/free"


class LlmServiceError(RuntimeError):
    pass


def is_llm_enabled() -> bool:
    provider = os.environ.get("LLM_PROVIDER", DEFAULT_LLM_PROVIDER).strip().lower()
    if provider == "openrouter":
        api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
        return bool(api_key)
    return provider == "ollama"


def get_llm_provider_status() -> dict:
    provider = os.environ.get("LLM_PROVIDER", DEFAULT_LLM_PROVIDER).strip().lower()

    if provider == "openrouter":
        api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
        return {
            "provider": provider,
            "enabled": bool(api_key),
            "model": os.environ.get("LLM_MODEL", DEFAULT_LLM_MODEL),
        }

    if provider == "ollama":
        return {
            "provider": provider,
            "enabled": True,
            "model": os.environ.get("LLM_MODEL", "llama3.1:8b"),
            "base_url": os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
        }

    return {"provider": "disabled", "enabled": False, "model": None}


def generate_chat_response(*, system_prompt: str, user_message: str) -> str:
    provider = os.environ.get("LLM_PROVIDER", "").strip().lower()
    if provider == "openrouter":
        return _call_openrouter(system_prompt=system_prompt, user_message=user_message)
    if provider == "ollama":
        return _call_ollama(system_prompt=system_prompt, user_message=user_message)
    raise LlmServiceError("No supported LLM provider is configured.")


def _call_openrouter(*, system_prompt: str, user_message: str) -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise LlmServiceError("OPENROUTER_API_KEY is not configured.")

    payload = {
        "model": os.environ.get("LLM_MODEL", "openrouter/auto"),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.4,
    }
    req = request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    return _read_openai_style_response(req)


def _call_ollama(*, system_prompt: str, user_message: str) -> str:
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    payload = {
        "model": os.environ.get("LLM_MODEL", "llama3.1:8b"),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
    }
    req = request.Request(
        f"{base_url}/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except error.URLError as exc:
        raise LlmServiceError(f"Ollama request failed: {exc}") from exc

    content = payload.get("message", {}).get("content", "").strip()
    if not content:
        raise LlmServiceError("Ollama returned an empty response.")
    return content


def _read_openai_style_response(req: request.Request) -> str:
    try:
        with request.urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))

    except error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise LlmServiceError(f"LLM HTTP error {exc.code}: {error_body}") from exc

    except error.URLError as exc:
        raise LlmServiceError(f"LLM request failed: {exc}") from exc

    choices = payload.get("choices") or []

    if not choices:
        raise LlmServiceError("The provider returned no completion choices.")

    message = choices[0].get("message", {})
    content = message.get("content", "")

    if isinstance(content, list):
        content = "".join(
            part.get("text", "") for part in content if isinstance(part, dict)
        )

    content = str(content).strip()

    if not content:
        raise LlmServiceError("The provider returned an empty message.")

    return content
