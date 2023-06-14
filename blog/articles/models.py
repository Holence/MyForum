from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from accounts.models import Account
from martor.models import MartorField

# Create your models here.
class Article(models.Model):
    
    author = models.ForeignKey(Account, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="user_articles")
    title = models.CharField(unique=True, max_length=128)
    slug = models.SlugField(unique=True, allow_unicode=True)
    content = MartorField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    upvotes = models.ManyToManyField(Account, blank=True, related_name="upvote_articles")
    downvotes = models.ManyToManyField(Account, blank=True, related_name="downvote_articles")

    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"slug": self.slug})
    
    def get_edit_url(self):
        return reverse("articles:edit", kwargs={"slug": self.slug})
    
    def get_delete_url(self):
        return reverse("articles:delete", kwargs={"slug": self.slug})
    
    def get_vote_url(self):
        return reverse("articles:vote", kwargs={"slug": self.slug})
    
    def get_unique_id(self):
        return f"{self.__class__.__name__}_{self.id}"
    
    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.title, allow_unicode=True)
        articles = Article.objects.filter(slug__exact=self.slug).exclude(id=self.id)
        if articles:
            articles = Article.objects.filter(slug__contains=self.slug+"_").exclude(id=self.id)
            self.slug = self.slug+"_"+str(articles.count()+1)
    
        super().save(*args, **kwargs)
    
    def get_comment_list(self):
        
        comments = []
        def deepin(comment, offset):
            if not comment.content:
                if comment.reply.all():
                    # 删除的评论，且有被回复，则显示（Deleted Content）
                    comments.append([comment, offset])
            else:
                comments.append([comment, offset])
            
            if comment.reply.all():
                for reply in comment.reply.all():
                    deepin(reply, offset+80)

        offset=20
        for comment in self.article_comments.order_by('timestamp'):
            if not comment.reply_to:
                deepin(comment, offset)
        return comments

    def __str__(self) -> str:
        return self.title

# Signal

# from django.db.models.signals import pre_save, post_save
# def article_pre_save(*args, **kwargs):
#     print("PRE")
#     print(args, kwargs)

# def article_post_save(*args, **kwargs):
#     print("POST")
#     print(args, kwargs)

# pre_save.connect(receiver=article_pre_save, sender=Article)
# post_save.connect(receiver=article_post_save, sender=Article)
