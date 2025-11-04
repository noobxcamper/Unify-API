"""
Expose django admin models as API endpoints for retrieval via a custom frontend.
"""
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey

from core.auth.permissions import AdminPermission, IsSuperuserStrict

class AdminAuthenticate(APIView):
    """
    Authenticates the user with the django admin backend.

    Default django admin portal only.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({
                "detail": "Login successful",
            }, status=200)
        else:
            return Response({
                "detail": "Invalid credentials"
            }, status=401)

class AdminAuthCheck(APIView):
    """
    Checks if the user is authenticated.

    Default django admin portal only.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"is_authenticated": request.user.is_authenticated}, status=200)

class AdminUsers(APIView):
    permission_classes = [ AdminPermission ]

    def get(self, request):
        users = User.objects.all().values("id", "username", "email", "is_active", "is_staff", "is_superuser")

        return Response({
            'users': users
        }, status=200)

class AdminAPIKeys(APIView):
    permission_classes = [ AdminPermission ]

    def get(self, request):
        keys = APIKey.objects.all().values("id", "prefix", "name", "hashed_key", "created", "expiry_date", "revoked")

        return Response({
            "keys": keys
        }, status=200)

    def patch(self, request):
        key_id = request.data.get('id')
        key = APIKey.objects.get(id=key_id)
        key.revoked = True
        key.save()

        return Response(status=204)