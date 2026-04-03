from django.db import models
from django.utils import timezone

class OBOAccessToken(models.Model):
    oid = models.CharField(primary_key=True, max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    access_token = models.TextField()

    def is_valid(self):
        return self.expires_at > timezone.now()

class EmailSettings(models.Model):
    email_host = models.CharField(max_length=50,default="smtp.office365.com")
    email_port = models.IntegerField(default=587)
    email_use_tls = models.BooleanField(default=True)
    email_username = models.CharField(max_length=50, null=False, blank=False)
    email_password = models.CharField(max_length=50, null=False, blank=False)
    
class ApprovalSettings(models.Model):
    approval_type = models.CharField(max_length=50, null=False, blank=False)
    approver1 = models.JSONField(null=False, blank=False)
    approver2 = models.JSONField(null=True, blank=True)
    allow_email_notifications = models.BooleanField(default=False, null=False, blank=False)

class ZohoToken(models.Model):
    access_token = models.TextField(default="")
    refresh_token = models.TextField(default="1000.3fdf4848d0a324a00ca98e7759583f0c.bc5484982c4b2a1b568b1b98543679cf") # this refresh token does not expire
    expires_at = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
class PurchaseOrders(models.Model):
    order_number = models.AutoField(primary_key=True)
    date_submitted = models.DateField(auto_now_add=True)
    supplier = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=1000, null=False, blank=False)
    justification = models.CharField(max_length=1000, null=False, blank=False)
    quantity = models.IntegerField(default=1, null=False, blank=False)
    unit_price = models.FloatField(default=0, null=False, blank=False)
    ship_to = models.CharField(max_length=50, null=False, blank=False)
    notes = models.TextField(max_length=500, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    address1 = models.CharField(max_length=50, null=True, blank=True)
    address2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

class Changes(models.Model):
    change_id = models.AutoField(primary_key=True)
    requester = models.CharField(max_length=50, null=False, blank=False)
    subject = models.CharField(max_length=50, null=False, blank=False)
    change_type = models.IntegerField(null=False, blank=False, default=0)   # 0 = minor, 1 = standard, 2 = major, 3 = emergency
    status = models.IntegerField(null=False, blank=False, default=0)        # 0 = open, 1 = closed, 2 = on hold
    priority = models.IntegerField(null=False, blank=False, default=0)      # 0 = low, 1 = medium, 2 = high, 3 = urgent
    impact = models.IntegerField(null=False, blank=False, default=0)        # 0 = low, 1 = medium, 2 = high
    risk = models.IntegerField(null=False, blank=False, default=0)          # 0 = low, 1 = medium, 2 = high
    team = models.CharField(max_length=50, null=False, blank=False)
    agent = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=1000, null=False, blank=False)