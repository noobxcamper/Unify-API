import logging

from django_celery_beat.models import PeriodicTask
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CeleryTasksPatchSerializer
from core.auth.permissions import AdminRole, AutomationAdminRole

# Logging and auditing
audit_category = "Automations"
logger = logging.getLogger(__name__)

class AutomationTasks(APIView):
    permission_classes = [ AdminRole | AutomationAdminRole | AllowAny ]

    def get(self, request):
        tasks = PeriodicTask.objects.all()
        serializer = CeleryTasksPatchSerializer(tasks, many=True)

        return Response(serializer.data)