from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class SignalsTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')

    def test_notification_on_message_create(self):
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Hello')
        self.assertTrue(Notification.objects.filter(user=self.user2, message=message).exists())

    def test_history_on_message_edit(self):
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Hello')
        message.content = 'Hi edited'
        message.save()
        self.assertTrue(MessageHistory.objects.filter(message=message, old_content='Hello').exists())
        self.assertTrue(message.edited)

    def test_cleanup_on_user_delete(self):
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content='Hello')
        Notification.objects.create(user=self.user2, message=message)
        self.user1.delete()
        self.assertFalse(Message.objects.filter(sender=self.user1).exists())
        self.assertFalse(Notification.objects.filter(user=self.user1).exists())