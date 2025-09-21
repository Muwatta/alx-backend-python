#!/usr/bin/env python3
"""Serializers for messaging app API."""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Conversation, Message
import uuid


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - converts User to/from JSON."""
    
    class Meta:
        model = User
        fields = [
            'id',           # UUID
            'first_name',   # Required
            'last_name',    # Required
            'email',        # Username/login
            'phone_number', # Optional
            'role',         # guest/host/admin
            'created_at',   # Auto timestamp
        ]
        read_only_fields = ['id', 'created_at']  # Can't change these


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with nested sender info."""
    
    # Show sender's name/email instead of just ID
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id',           # UUID
            'sender',       # Nested UserSerializer
            'message_body', # The actual message text
            'sent_at',      # Timestamp
        ]
        read_only_fields = ['id', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation with nested participants & messages."""
    
    # Show all participants with their details
    participants = UserSerializer(many=True, read_only=True)
    
    # Show recent messages in the conversation
    messages = MessageSerializer(many=True, read_only=True)
    
    # Count of messages (calculated field)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id',           # UUID
            'participants', # List of UserSerializers
            'messages',     # List of MessageSerializers
            'created_at',   # Timestamp
            'message_count',# Calculated
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_message_count(self, obj):
        """Return number of messages in conversation."""
        return obj.messages.count()


class ConversationCreateSerializer(serializers.ModelSerializer):
    """Special serializer for CREATING new conversations."""
    
    # Accept list of participant UUIDs when creating
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,  # Only used for input, not output
        min_length=2,     # At least 2 people to chat!
        max_length=10,    # Max 10 people in group chat
    )
    
    class Meta:
        model = Conversation
        fields = ['participant_ids']  # Only need this for creation
    
    def create(self, validated_data):
        """Custom create method to handle participant_ids."""
        participant_ids = validated_data.pop('participant_ids')
        
        # Get users by their UUIDs
        participants = User.objects.filter(id__in=participant_ids)
        
        # Validate we found all participants
        if participants.count() != len(participant_ids):
            raise serializers.ValidationError(
                "Some participant IDs not found"
            )
        
        # Create conversation
        conversation = Conversation.objects.create()
        
        # Add all participants
        conversation.participants.set(participants)
        
        return conversation