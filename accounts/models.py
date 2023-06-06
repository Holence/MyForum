from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    url = models.CharField(max_length=256, null=True, blank=True)
    bio = models.TextField(max_length=512, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
