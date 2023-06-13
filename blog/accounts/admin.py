from django.contrib import admin

# Register your models here.
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    autocomplete_fields = ["following"]

admin.site.register(Account, AccountAdmin)