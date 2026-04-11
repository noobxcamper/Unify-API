from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from core.models import AppUser
from core.auth.permissions import AdminRole, IsAuthenticated, get_roles, get_permissions, ITRole
from core.utils import generate_password
from serializers import AppUserSerializer, AppUserPatchSerializer


class AppUsersView(APIView):
    permission_classes = [ AdminRole ]

    def get(self, request):
        user = AppUser.objects.all()
        serializer = AppUserSerializer(user, many=True)

        return Response(serializer.data)

    def patch(self, request):
        user_id = request.query_params.get('id')

        user = AppUser.objects.get(oid=user_id)
        serializer = AppUserPatchSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=204)

        return Response(serializer.errors, status=400)

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