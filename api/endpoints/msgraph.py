import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from core.config.obo_flow import generate_obo_token
from core.auth.permissions import AdminPermission, UserPermission

class MSGraphUsersView(APIView):
    permission_classes = [HasAPIKey | AdminPermission ]

    def get(self, request):
        obo_token = generate_obo_token(request.auth)

        # setup headers dict
        auth_header = {"Authorization": f"Bearer {obo_token}"}

        # perform graph request
        response = requests.get("https://graph.microsoft.com/v1.0/users", headers=auth_header)

        return Response(response.json())