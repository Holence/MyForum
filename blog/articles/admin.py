from django.contrib import admin

# Register your models here.
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author", "timestamp", "updated"]
    search_fields = ["title", "content"]
    raw_id_fields = ["author"]

admin.site.register(Article, ArticleAdmin)