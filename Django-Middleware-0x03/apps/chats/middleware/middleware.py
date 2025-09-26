import logging
from datetime import datetime
import pytz
from django.http import HttpResponseForbidden
from django.core.cache import cache
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('requests.log', maxBytes=1000000, backupCount=5)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

class RequestLoggingMiddleware:
    """Logs request timestamp, user (email), path, and method to requests.log"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.email if request.user.is_authenticated else "Anonymous"
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path} - Method: {request.method}")
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    """Restricts chat access outside 6 PM - 9 PM (Africa/Lagos)"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now(pytz.UTC).astimezone(pytz.timezone('Africa/Lagos'))
        hour = now.hour
        if 18 <= hour < 21:
            return self.get_response(request)
        return HttpResponseForbidden("Chat access restricted outside 6 PM - 9 PM")

class OffensiveLanguageMiddleware:
    """Limits chat messages to 5 per minute per IP address"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and '/chat/' in request.path:
            ip = request.META.get('REMOTE_ADDR')
            key = f"rate_{ip}"
            count = cache.get_or_set(key, 0, 60)
            if count >= 5:
                return HttpResponseForbidden("Rate limit exceeded: 5 messages per minute")
            cache.incr(key)
        return self.get_response(request)

class RolePermissionMiddleware:
    """Restricts specific actions to admin or host roles"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/admin-action/' in request.path:
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Login required")
            if hasattr(request.user, 'role') and request.user.role not in ['admin', 'host']:
                return HttpResponseForbidden("Admins or hosts only")
        return self.get_response(request)
EOFcat > apps/chats/middleware/middleware.py << 'EOF'
import logging
from datetime import datetime
import pytz
from django.http import HttpResponseForbidden
from django.core.cache import cache
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('requests.log', maxBytes=1000000, backupCount=5)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

class RequestLoggingMiddleware:
    """Logs request timestamp, user (email), path, and method to requests.log"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.email if request.user.is_authenticated else "Anonymous"
        logging.info(f"{datetime.now()} - User: {user} - Path: {request.path} - Method: {request.method}")
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    """Restricts chat access outside 6 PM - 9 PM (Africa/Lagos)"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now(pytz.UTC).astimezone(pytz.timezone('Africa/Lagos'))
        hour = now.hour
        if 18 <= hour < 21:
            return self.get_response(request)
        return HttpResponseForbidden("Chat access restricted outside 6 PM - 9 PM")

class OffensiveLanguageMiddleware:
    """Limits chat messages to 5 per minute per IP address"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and '/chat/' in request.path:
            ip = request.META.get('REMOTE_ADDR')
            key = f"rate_{ip}"
            count = cache.get_or_set(key, 0, 60)
            if count >= 5:
                return HttpResponseForbidden("Rate limit exceeded: 5 messages per minute")
            cache.incr(key)
        return self.get_response(request)

class RolePermissionMiddleware:
    """Restricts specific actions to admin or host roles"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/admin-action/' in request.path:
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Login required")
            if hasattr(request.user, 'role') and request.user.role not in ['admin', 'host']:
                return HttpResponseForbidden("Admins or hosts only")
        return self.get_response(request)
