from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .models import Message
import django.db.models as models

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('logout')  # Update if you have a logout view

@cache_page(60)
@login_required
def message_list(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = Message.objects.filter(
        models.Q(sender=request.user, receiver=receiver) | models.Q(sender=receiver, receiver=request.user)
    ).select_related('sender', 'receiver').prefetch_related('replies', 'history').order_by('timestamp')
    return render(request, 'messaging/message_list.html', {'messages': messages, 'receiver': receiver})