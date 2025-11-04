from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from api.serializers import ApprovalSettingsSerializer
from core.models import ApprovalSettings
from core.auth.permissions import AdminPermission

class ApprovalSettingsView(APIView):
    permission_classes = [HasAPIKey | AdminPermission ]

    def get(self, request):
        approval_settings = ApprovalSettings.objects.first()
        serializer = ApprovalSettingsSerializer(approval_settings)

        return Response(serializer.data, status=200)

    def post(self, request):
        return None

    def patch(self, request):
        approval_settings = ApprovalSettings.objects.first()
        serializer = ApprovalSettingsSerializer(approval_settings, request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)