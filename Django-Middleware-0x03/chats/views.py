from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message
from .serializers import MessageSerializer

class ChatView(APIView):
    def post(self, request):
        message_body = request.data.get('message_body')
        serializer = MessageSerializer(data={'message_body': message_body})
        if serializer.is_valid():
            serializer.save(sender=request.user, conversation_id=request.data.get('conversation_id'))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminActionView(APIView):
    def get(self, request):
        if request.user.role == 'admin':
            return Response({"message": "Admin action successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Admin access required"}, status=status.HTTP_403_FORBIDDEN)
