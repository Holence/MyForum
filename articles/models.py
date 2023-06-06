from django.db import models
from django.utils.text import slugify


# Create your models here.
class Article(models.Model):
    title = models.CharField(unique=True, max_length=128)
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
            articles = Article.objects.filter(slug__exact=self.slug).exclude(id=self.id)
            if articles:
                articles = Article.objects.filter(slug__contains=self.slug+"_").exclude(id=self.id)
                self.slug = self.slug+"_"+str(articles.count()+1)
        
        super().save(*args, **kwargs)

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
