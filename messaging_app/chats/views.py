#!/usr/bin/env python3
"""API views for messaging conversations and messages."""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, 
    ConversationCreateSerializer, 
    MessageSerializer
)


User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    """API endpoints for conversations."""
    
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Only show conversations for the logged-in user."""
        user = self.request.user
        return self.queryset.filter(
            participants=user
        ).prefetch_related(
            'participants',           # Many-to-many users
            'messages__sender'        # Reverse FK to messages, then sender
        ).order_by('-created_at')     # Sort by newest first
    
    def get_serializer_class(self):
        """Use different serializers for different actions."""
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer
    
    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        """Create a new conversation with participants."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save()
            # Return the full conversation data
            return Response(
                ConversationSerializer(conversation).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message to a conversation."""
        conversation = self.get_object()
        
        # Check if user is in this conversation
        if not conversation.participants.filter(id=request.user.id).exists():
            return Response(
                {'error': 'You are not a participant in this conversation'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Create message data
        message_data = {
            'conversation': conversation.id,
            'sender': request.user.id,
            'message_body': request.data.get('message_body', '').strip()
        }
        
        if not message_data['message_body']:
            return Response(
                {'error': 'Message body cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create and save message
        serializer = MessageSerializer(data=message_data)
        if serializer.is_valid():
            message = serializer.save()
            return Response(
                MessageSerializer(message).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get all messages in a conversation."""
        conversation = self.get_object()
        
        # Check permission
        if not conversation.participants.filter(id=request.user.id).exists():
            return Response(
                {'error': 'Access denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Return messages with prefetching
        messages = conversation.messages.select_related('sender').order_by('sent_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only API for messages (filtered by conversation)."""
    
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter messages by conversation and user permission."""
        conversation_id = self.kwargs.get('conversation_pk')
        if not conversation_id:
            return self.queryset.none()
        
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # Only show if user is participant
        if not conversation.participants.filter(id=self.request.user.id).exists():
            return self.queryset.none()
        
        return self.queryset.filter(
            conversation=conversation
        ).select_related('sender').order_by('sent_at')