from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import PurchaseOrders, ApprovalSettings, Changes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}

class PurchaseOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrders
        fields = '__all__'

class ApprovalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalSettings
        fields = '__all__'

class ChangesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Changes
        fields = '__all__'