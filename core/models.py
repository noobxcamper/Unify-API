from django.db import models

def default_roles():
    return ['User']

def default_permissions():
    return ['User.Read']

class User(models.Model):
    oid = models.CharField(max_length=128, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    roles = models.JSONField(default=default_roles)
    permissions = models.JSONField(default=default_permissions)

class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    oid = models.CharField(max_length=128)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    category = models.CharField(max_length=100)
    action = models.CharField(max_length=100)
    additional_details = models.CharField(max_length=2000, null=True, blank=True)