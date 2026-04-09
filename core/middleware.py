from rest_framework_api_key.models import APIKey
import uuid

class APIKeyDetectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.is_api_key = False
        request.api_key = None

        auth = request.headers.get("Authorization", "")

        if auth.startswith("Api-Key "):
            raw_key = auth.split(" ", 1)[1]
            try:
                api_key = APIKey.objects.get_from_key(raw_key)
                request.is_api_key = True
                request.api_key = api_key
            except APIKey.DoesNotExist:
                pass

        return self.get_response(request)

class AuditMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            remote_ip = x_forwarded_for.split(",")[0].strip()
        else:
            remote_ip = request.META.get("REMOTE_ADDR")

        request.request_id = str(uuid.uuid4())
        request.remote_ip = remote_ip
        request.user_agent = request.META.get("HTTP_USER_AGENT")

        return self.get_response(request)