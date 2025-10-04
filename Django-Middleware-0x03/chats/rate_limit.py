from django.http import HttpResponseForbidden
from django.core.cache import cache
import time

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and '/chat/' in request.path:
            ip = request.META.get('REMOTE_ADDR')
            key = f"rate_limit:{ip}"
            requests = cache.get(key, [])
            current_time = time.time()
            requests = [t for t in requests if current_time - t < 60]
            if len(requests) >= 5:
                return HttpResponseForbidden("Rate limit exceeded: 5 messages per minute")
            requests.append(current_time)
            cache.set(key, requests, timeout=60)
        return self.get_response(request)
