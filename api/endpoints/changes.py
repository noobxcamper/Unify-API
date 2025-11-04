from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from api.serializers import ChangesSerializer
from core.auth.permissions import AdminPermission
from core.models import Changes

class ChangesView(APIView):
    permission_classes = [ HasAPIKey | AdminPermission ]

    def get(self, request, change_id=None):
        if change_id is None:
            changes = Changes.objects.all()
            serializer = ChangesSerializer(changes, many=True)

            return Response(serializer.data)

        try:
            changes = Changes.objects.get(change_id=change_id)
            serializer = ChangesSerializer(changes, data=request.data, partial=True)

            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except:
            error_response = {
                "error": [{
                    "error_code": "InvalidQuery",
                    "message": "could not find change with the change id specified"
                }]
            }
            return Response(error_response, status=400)