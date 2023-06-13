from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name: str, max_length = None) -> str:
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return super().get_available_name(name, max_length)

# Create your models here.
def image_upload_to_path(account, file_name):
    return f"avatar/user_{account.user.id}.jpg"

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=256, null=True, blank=True)
    bio = models.TextField(max_length=512, null=True, blank=True)
    avatar = models.ImageField(upload_to=image_upload_to_path, storage=OverwriteStorage(), null=True, blank=True)
    following = models.ManyToManyField("self", blank=True, symmetrical=False)

    def get_avatar_url(self):
        return settings.MEDIA_URL + str(self.avatar)

    def get_profile_url(self):
        return reverse("accounts:detail", kwargs={"username": self.user.username})
    
    @property
    def sorted_article_set(self):
        return self.user_articles.order_by('updated')

    def __str__(self) -> str:
        return self.user.username