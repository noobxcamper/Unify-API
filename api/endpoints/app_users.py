import logging

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from core.auth.permissions import AdminRole, IsAuthenticated, get_user_access, ITRole
from core.models import AppUsers
from core.utils import generate_password, create_audit_log
from serializers import AppUserSerializer, AppUserPatchSerializer

# Logging and auditing
audit_category = "Administration"
logger = logging.getLogger(__name__)

class AppUsersView(APIView):
    permission_classes = [ AdminRole ]

    def get(self, request):
        user = AppUsers.objects.all()
        serializer = AppUserSerializer(user, many=True)

        return Response(serializer.data)

    def patch(self, request):
        user_id = request.query_params.get('id')

        user = AppUsers.objects.get(oid=user_id)
        serializer = AppUserPatchSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            create_audit_log(
                request,
                category=audit_category,
                action="Roles Changed",
                meta={
                    'oid': user.oid,
                    'name': user.name,
                    'roles': request.data.get('roles'),
                    'permissions': request.data.get('permissions'),
                }
            )

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
        access = get_user_access(request.user.oid)

        return Response(access)