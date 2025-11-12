from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User, Conversation, Message


# --------------------------
# 1️⃣ User Serializer
# --------------------------
class UserSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source='username', read_only=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'display_name',
            'email',
            'first_name',
            'last_name',
            'phone_number',
        ]


# --------------------------
# 2️⃣ Message Serializer
# --------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'sender',
            'message_body',
            'sent_at',
            'created_at',
        ]


# --------------------------
# 3️⃣ Conversation Serializer
# --------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    total_messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'total_messages',
            'created_at',
        ]

    def get_total_messages(self, obj):
        return obj.messages.count()

    def validate(self, data):
        """Example validation logic using serializers.ValidationError"""
        if not data:
            raise serializers.ValidationError("Conversation data cannot be empty.")
        return data
