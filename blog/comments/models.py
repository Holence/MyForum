from django.db import models
from django.urls import reverse
from articles.models import Article
from accounts.models import Account
from martor.models import MartorField

# Create your models here.
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="article_comments")
    author = models.ForeignKey(Account, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="user_comments")
    content = MartorField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(Account, blank=True, related_name="upvote_comments")
    downvotes = models.ManyToManyField(Account, blank=True, related_name="downvote_comments")
    reply_to = models.ForeignKey("self", on_delete=models.DO_NOTHING, blank=True, null=True, related_name="reply")

    def get_absolute_url(self):
        return self.article.get_absolute_url()+"#"+self.get_unique_id()
    
    def get_post_url(self):
        return reverse("comments:post")
    
    def get_reply_url(self):
        return reverse("comments:reply")

    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"id": self.id})

    def get_vote_url(self):
        return reverse("comments:vote", kwargs={"id": self.id})

    def get_unique_id(self):
        return f"{self.__class__.__name__}_{self.id}"
