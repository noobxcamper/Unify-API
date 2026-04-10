from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from core.auth.permissions import AdminRole, IsAuthenticated, get_roles, get_permissions, ITRole
from core.utils import generate_password


class GeneratePasswordView(APIView):
    permission_classes = [ AdminRole | ITRole | HasAPIKey ]

    def get(self, request):
        password_data = {
            "password": generate_password()
        }

        return Response(password_data)

class CurrentUserRolesView(APIView):
    permission_classes = [ IsAuthenticated ]

    def get(self, request):
        roles = get_roles(request.user.oid)
        permissions = get_permissions(request.user.oid)

        return Response({
            "roles": roles,
            "permissions": permissions
        })