from rest_framework.response import Response
from rest_framework.views import APIView

from services.llm_service import get_llm_provider_status


class AiHealthView(APIView):
    def get(self, request, *args, **kwargs):
        provider_status = get_llm_provider_status()
        return Response(
            {
                "service": "ai-engine",
                "status": "ready",
                "message": "The assistant supports a rules-based fallback and optional LLM-backed responses.",
                "llm": provider_status,
            }
        )
