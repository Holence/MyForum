from django.urls import path

from .views import messenger_view, messenger_messagesbox_view, messenger_messageslist_view

app_name="messenger"

urlpatterns = [
    path('', messenger_view, name="base"),
    path('messagesbox/', messenger_messagesbox_view, name="messagesbox"),
    path('messageslist/', messenger_messageslist_view, name="messageslist"),
]
