from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


# --------------------------
# 1️⃣ Conversation ViewSet
# --------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        """Create a new conversation"""
        participants_ids = request.data.get('participants', [])
        if not participants_ids:
            return Response(
                {'error': 'Participants required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        participants = User.objects.filter(id__in=participants_ids)
        if not participants.exists():
            return Response(
                {'error': 'No valid participants found'},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# --------------------------
# 2️⃣ Message ViewSet
# --------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body']

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send message to an existing conversation"""
        conversation = Conversation.objects.get(pk=pk)
        sender = request.user
        message_body = request.data.get('message_body')

        if not message_body:
            return Response(
                {'error': 'Message body is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body,
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
