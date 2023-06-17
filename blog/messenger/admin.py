from django.contrib import admin

# Register your models here.
from .models import Messenger

class MessengerAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "content", "timestamp", "read"]

admin.site.register(Messenger, MessengerAdmin)