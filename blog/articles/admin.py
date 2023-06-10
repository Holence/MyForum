from django.contrib import admin
from django.db import models

# Register your models here.
from .models import Article
from martor.widgets import AdminMartorWidget

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "timestamp", "updated"]
    search_fields = ["title", "content"]
    raw_id_fields = ["author"]
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

admin.site.register(Article, ArticleAdmin)