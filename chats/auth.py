from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer

class UserMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(conversation__participants=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
