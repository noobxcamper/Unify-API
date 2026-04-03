"""
Expose django admin models as API endpoints for retrieval via a custom frontend.
"""
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey

from api.serializers import AuditLogSerializer, ApiKeySerializer
from core.auth.permissions import AdminRole
from core.models import AuditLog

# Logging and auditing
audit_category = "Administration"

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
    permission_classes = [ AdminRole ]

    def get(self, request):
        AuditLog.objects.create(
            oid = request.user.oid,
            name = request.user.name,
            email = request.user.email,
            endpoint = "AdminUsers",
            action = "Retrieved users"
        )

        users = User.objects.all().values("id", "username", "email", "is_active", "is_staff", "is_superuser")

        return Response({
            'users': users
        }, status=200)

class AdminAPIKeys(APIView):
    permission_classes = [ AdminRole ]

    def get(self, request):
        keys = APIKey.objects.all()
        serializer = ApiKeySerializer(keys, many=True)

        return Response(serializer.data, status=200)

    def post(self, request):
        APIKey.objects.create_key(
            name = request.data.get('name'),
            expiry_date = request.data.get('expiry_date'),
        )

        return Response(status=204)

    def patch(self, request):
        key_id = request.query_params.get('id')
        key = APIKey.objects.get(id=key_id)

        serializer = ApiKeySerializer(key, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        AuditLog.objects.create(
            oid = request.user.oid,
            name = request.user.name,
            email = request.user.email,
            category = audit_category,
            action = "Revoked API key",
            additional_details = f"Target key: {key_id}"
        )

        return Response(status=204)

    def delete(self, request):
        key_id = request.query_params.get('id')
        APIKey.objects.get(id=key_id).delete()

        AuditLog.objects.create(
            oid = request.user.oid,
            name = request.user.name,
            email = request.user.email,
            category = audit_category,
            action = "Deleted API key",
            additional_details = f"Target key: {key_id}"
        )

        return Response(status=204)

class AdminAuditLogs(APIView):
    permission_classes = [ AdminRole ]

    def get(self, request):
        audit_logs = AuditLog.objects.all()
        serializer = AuditLogSerializer(audit_logs, many=True)

        return Response(serializer.data)