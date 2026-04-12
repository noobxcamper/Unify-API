from django_celery_beat.models import PeriodicTask
from rest_framework import serializers

class CeleryTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = '__all__'

class CeleryTasksPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = '__all__'