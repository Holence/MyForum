from django.db import models
from django.db import models
from accounts.models import Account
from martor.models import MartorField

# Create your models here.
class Messenger(models.Model):
    class Meta:  
        verbose_name_plural = 'Messenger'
    
    sender = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name="sent_messages")
    receiver = models.ForeignKey(Account, on_delete=models.DO_NOTHING, related_name="received_messages")
    content = MartorField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
