from django.contrib import admin

# Register your models here.
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ["content", "article", "user", "timestamp"]
    raw_id_fields = ["article", "user"]
    

admin.site.register(Comment, CommentAdmin)