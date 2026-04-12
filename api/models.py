from django.db import models

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