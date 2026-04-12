"""
Expose django admin models as API endpoints for retrieval via a custom frontend.
"""
import logging

from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey
from rest_framework_api_key.permissions import HasAPIKey

from serializers import AuditLogSerializer, ApiKeySerializer, RoleSerializer
from core.auth.permissions import AdminRole
from core.models import Roles, AuditLogs
from core.utils import create_audit_log

# Logging and auditing
audit_category = "Administration"
logger = logging.getLogger(__name__)

class Authenticate(APIView):
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

class AuthCheck(APIView):
    """
    Checks if the user is authenticated.

    Default django admin portal only.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"is_authenticated": request.user.is_authenticated}, status=200)

class DjangoUsers(APIView):
    permission_classes = [ AdminRole ]

    def get(self, request):
        users = User.objects.all().values("id", "username", "email", "is_active", "is_staff", "is_superuser")

        create_audit_log(
            request,
            category=audit_category,
            action="Retrieved Django Users",
            meta={}
        )

        return Response({'users': users})

class APIKeys(APIView):
    permission_classes = [ AdminRole | HasAPIKey ]

    def get(self, request):
        keys = APIKey.objects.all()
        serializer = ApiKeySerializer(keys, many=True)

        return Response(serializer.data, status=200)

    def post(self, request):
        key, generated_key = APIKey.objects.create_key(
            name = request.data.get('name'),
            expiry_date = request.data.get('expiry_date'),
        )

        create_audit_log(
            request,
            category = audit_category,
            action = "Created API Key",
            meta={
                'key_name': key.name,
                'key_prefix': key.prefix,
                'expiry_date': key.expiry_date,
            }
        )

        return Response({ 'name': key.name, 'key': generated_key }, status=200)

    def patch(self, request):
        key_id = request.query_params.get('id')
        key = APIKey.objects.get(id=key_id)

        serializer = ApiKeySerializer(key, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        print(serializer.data)

        create_audit_log(
            request,
            category = audit_category,
            action = "Updated API Key",
            meta={
                'key_name': key.name,
                'key_prefix': key.prefix,
                'expiry_date': key.expiry_date.isoformat(),
                'revoked': key.revoked,
            }
        )

        return Response(status=204)

    def delete(self, request):
        key_id = request.query_params.get('id')
        key = APIKey.objects.get(id=key_id)
        key.delete()

        create_audit_log(
            request,
            category = audit_category,
            action = "Deleted API Key",
            meta={
                'key_name': key.name,
                'key_prefix': key.prefix,
            }
        )

        return Response(status=204)

class Logs(APIView):
    permission_classes = [ AdminRole ]

    def get(self, request):
        audit_logs = AuditLogs.objects.all()
        serializer = AuditLogSerializer(audit_logs, many=True)

        return Response(serializer.data)

class AvailableRoles(APIView):
    permission_classes = [ AdminRole ]

    def get(self, request):
        roles = Roles.objects.all()
        serializer = RoleSerializer(roles, many=True)

        return Response(serializer.data)