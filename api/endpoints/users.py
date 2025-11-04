import secrets
import string

from rest_framework.response import Response
from rest_framework.views import APIView
from core.auth.permissions import AdminPermission, UserPermission

class GeneratePasswordView(APIView):
    permission_classes = [ AdminPermission ]

    def get(self, request):
        password_requirement = string.ascii_letters + string.digits + string.punctuation
        password_length = 16
        password = "".join(secrets.choice(password_requirement) for _ in range(password_length))

        password_data = {
            "password": password
        }

        return Response(password_data)