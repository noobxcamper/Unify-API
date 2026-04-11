from django.db import models

def default_roles():
    return ['User']

def default_permissions():
    return ['User.Read']

class AppUser(models.Model):
    oid = models.CharField(max_length=128, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    roles = models.JSONField(default=default_roles)
    permissions = models.JSONField(default=default_permissions)

class AuditLog(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    request_id = models.CharField(max_length=40)
    remote_ip = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    api_key_used = models.BooleanField(default=False)
    user_details = models.JSONField(default=dict)
    meta = models.JSONField(default=dict)