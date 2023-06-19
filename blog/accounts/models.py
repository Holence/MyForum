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
    
    # related_name逆向表，太方便了
    following = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="follower")

    def __str__(self) -> str:
        return self.user.username

    def get_avatar_url(self):
        if self.avatar:
            return settings.MEDIA_URL + str(self.avatar)
        else:
            return settings.STATIC_URL + "img/avatar.svg"

    def get_absolute_url(self):
        return reverse("accounts:detail", kwargs={"username": self.user.username})
    
    def get_follow_url(self):
        return reverse("accounts:follow", kwargs={"username": self.user.username})
    
    @property
    def proper_name(self):
        if not self.user.first_name and not self.user.last_name:
            return self.user.username
        else:
            return self.user.first_name+" "+self.user.last_name
    
    @property
    def sorted_article_set(self):
        return self.user_articles.order_by('-updated')

    @property
    def unread_message_count(self):
        return self.received_messages.filter(read=False).count()

    @property
    def unread_information_count(self):
        return self.user_informations.filter(read=False).count()
