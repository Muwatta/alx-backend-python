import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# --------------------------
# 1️⃣ Custom User Model
# --------------------------
class User(AbstractUser):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Explicitly declared
    first_name = models.CharField(max_length=150, blank=True)  # Explicitly declared
    last_name = models.CharField(max_length=150, blank=True)   # Explicitly declared
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


# --------------------------
# 2️⃣ Conversation Model
# --------------------------
class Conversation(models.Model):
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# --------------------------
# 3️⃣ Message Model
# --------------------------
class Message(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.conversation.conversation_id}"
