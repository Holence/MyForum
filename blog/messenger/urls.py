from django.urls import path

from .views import messenger_view, messenger_messagesbox_view, messenger_post_view

app_name="messenger"

urlpatterns = [
    path('', messenger_view, name="base"),
    path('messagesbox/', messenger_messagesbox_view, name="messagesbox"),
    path('post/', messenger_post_view, name="post")
]
