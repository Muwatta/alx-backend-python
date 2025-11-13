from django.shortcuts import render
from .models import Message

def inbox_view(request):
    user = request.user
    unread_messages = Message.unread.unread_for_user(user)
    return render(request, 'messaging/inbox.html', {'messages': unread_messages})
