from rest_framework.response import Response
from rest_framework.views import APIView

from apps.chat.models import ChatMessage


class FlaggedMessagesView(APIView):
    def get(self, request, *args, **kwargs):
        flagged = ChatMessage.objects.filter(flagged=True).order_by("-created_at")[:20]
        data = [
            {
                "session_id": message.session_id,
                "content": message.content,
                "risk_level": message.risk_level,
                "created_at": message.created_at,
            }
            for message in flagged
        ]
        return Response({"flagged_messages": data})
