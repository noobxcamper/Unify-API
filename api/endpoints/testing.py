from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.tasks import offboarding_task
from django.utils import timezone
import datetime

@api_view(['GET'])
@permission_classes([AllowAny])
def test_get(request):
    return Response("Test succeeded!", status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def test_schedule(request):
    offboarding_task.apply_async(
        args=["Test Message"],
        eta=timezone.now() + datetime.timedelta(seconds=10)
    )

    return Response(status=204)