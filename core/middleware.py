from rest_framework_api_key.models import APIKey

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