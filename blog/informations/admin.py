from django.contrib import admin

# admin site中添加LogEntry
# 没法设置project层面的admin.py，只好寄宿在这里了
from django.contrib.admin.models import LogEntry
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ["user", "action_flag", "object_repr", "content_type", "action_time", "change_message"]
    search_fields = ["user__username", "object_repr"]
    list_filter = ["user", "action_flag", "content_type"]

admin.site.register(LogEntry, LogEntryAdmin)

# Register your models here.
from .models import Information
class InformationAdmin(admin.ModelAdmin):
    list_display = ["user", "info", "timestamp", "read"]
    search_fields = ["user__username", "info"]
    list_filter = ["user", "read"]

admin.site.register(Information, InformationAdmin)
