from django.urls import path

from .views import messenger_view, messenger_messages_view

app_name="messenger"

urlpatterns = [
    path('', messenger_view, name="base"),
    path('messages', messenger_messages_view, name="messages")
]
