from django.http import HttpResponseForbidden
from django.core.cache import cache
from datetime import time
import logging
# import profanity_check

logger = logging.getLogger('django')
logging.basicConfig(filename='requests.log', level=logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"{request.method} {request.path} {request.user}")
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = time.localtime().tm_hour
        if request.path.startswith('/chat/') and (current_hour < 18 or current_hour >= 21):
            return HttpResponseForbidden("Access restricted: Chat only available from 6 PM to 9 PM WAT")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and '/chat/' in request.path:
            message = request.data.get('message_body', '')
            # Disabled profanity check due to dependency issues
            # if profanity_check.predict([message])[0] > 0.5:
            #     return HttpResponseForbidden("Offensive language detected")
        return self.get_response(request)

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/chat/admin-action/') and request.user.is_authenticated:
            if request.user.role not in ['admin', 'host']:
                return HttpResponseForbidden("Admin or moderator access required")
        return self.get_response(request)
