from django.contrib import admin
from django.db import models

# Register your models here.
from .models import Comment
from martor.widgets import AdminMartorWidget

class CommentAdmin(admin.ModelAdmin):
    list_display = ["content", "article", "user", "timestamp"]
    raw_id_fields = ["article", "user"]
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }
    

admin.site.register(Comment, CommentAdmin)