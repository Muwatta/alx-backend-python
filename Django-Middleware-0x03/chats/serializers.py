from rest_framework import serializers
from .models import Message, Conversation
from users.models import User

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['id', 'sender', 'sent_at']

    def validate_conversation(self, value):
        if not value.participants.filter(id=self.context['request'].user.id).exists():
            raise serializers.ValidationError("User is not a participant in this conversation")
        return value
