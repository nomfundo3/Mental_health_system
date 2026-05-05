from rest_framework.response import Response
from rest_framework.views import APIView


class AiHealthView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "service": "ai-engine",
                "status": "ready",
                "message": "Starter AI service is configured for rules-based support flow.",
            }
        )
