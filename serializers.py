import pytz
from rest_framework import serializers
from rest_framework_api_key.models import APIKey
from api.models import Changes
from core.models import AuditLogs, AppUsers, Roles

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUsers
        fields = '__all__'

class AppUserPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUsers
        fields = ['roles', 'permissions']

    def validate(self, attrs):
        if "roles" and "permissions" in attrs:
            roles = attrs['roles']
            permissions = attrs['permissions']

            if "User" not in roles:
                raise serializers.ValidationError("Deleting the default role 'User' is not allowed.")

        else:
            raise serializers.ValidationError("Missing roles or permissions data.")

        return attrs

class ChangesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Changes
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLogs
        fields = '__all__'

class ApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = '__all__'