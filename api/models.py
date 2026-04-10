from django.db import models

class EmailSettings(models.Model):
    email_host = models.CharField(max_length=255, default="smtp.office365.com")
    email_port = models.PositiveSmallIntegerField(default=587)
    email_use_tls = models.BooleanField(default=True)
    email_username = models.CharField(max_length=255)
    email_password = models.CharField(max_length=255)

class ZohoToken(models.Model):
    access_token = models.TextField(default="")
    refresh_token = models.TextField(default="1000.3fdf4848d0a324a00ca98e7759583f0c.bc5484982c4b2a1b568b1b98543679cf")
    expires_at = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

class Changes(models.Model):
    class ChangeStatus(models.IntegerChoices):
        CLOSED = 0
        OPEN = 1
        ON_HOLD = 3
        AWAITING_APPROVAL = 4
        IN_PROGRESS = 5
        TESTING = 6

    class ChangeLevel(models.IntegerChoices):
        LOW = 0
        MEDIUM = 1
        HIGH = 2
        URGENT = 3

    change_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    requester = models.EmailField(max_length=255, null=True, blank=True)
    approver = models.EmailField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=ChangeStatus.choices, default=ChangeStatus.OPEN)
    priority = models.PositiveSmallIntegerField(choices=ChangeLevel.choices, default=ChangeLevel.LOW)
    impact = models.PositiveSmallIntegerField(choices=ChangeLevel.choices, default=ChangeLevel.LOW)
    risk = models.PositiveSmallIntegerField(choices=ChangeLevel.choices, default=ChangeLevel.LOW)
    implementation_date = models.DateTimeField(null=True, blank=True)
    requires_downtime = models.BooleanField(default=False)