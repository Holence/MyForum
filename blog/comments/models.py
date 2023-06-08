from django.db import models
from django.urls import reverse
from articles.models import Article
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"id": self.id})
