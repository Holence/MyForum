from django.contrib import admin

# Register your models here.
from .models import Messenger

class MessengerAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "content", "timestamp", "read"]
    list_filter = ["sender", "receiver", "read"]

admin.site.register(Messenger, MessengerAdmin)