from django.db import models
from accounts.models import Account

# Create your models here.
class Information(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="user_informations")
    info = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

