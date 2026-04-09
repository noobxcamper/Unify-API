import pytz
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_api_key.models import APIKey
from api.models import Changes
from core.models import AuditLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}

class ChangesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Changes
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

class ApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = '__all__'