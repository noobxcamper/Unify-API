from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from api.tasks import print_task

import json

@api_view(['GET'])
@permission_classes([AllowAny])
def test_task(request):
    print_task.delay("Hello from celery!")

    return Response({"status": "queued"})

@api_view(['POST'])
@permission_classes([AllowAny])
def schedule_task(request):
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=10,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.create(
        interval=schedule,
        name="print-hello-every-10-seconds",
        task="api.tasks.print_task",
        args=json.dumps(["Hello from scheduled task!"]),
        enabled=True,
    )

    return Response({"status": "task scheduled"})