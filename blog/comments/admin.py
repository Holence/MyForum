from django.contrib import admin
from django.db import models

# Register your models here.
from .models import Comment
from martor.widgets import AdminMartorWidget

class CommentAdmin(admin.ModelAdmin):
    list_display = ["content", "article", "author", "timestamp"]
    search_fields = ["content"]
    raw_id_fields = ["article", "author", "reply_to"]
    list_filter = ["article", "author"]
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    autocomplete_fields = ["upvotes", "downvotes"]
    

admin.site.register(Comment, CommentAdmin)