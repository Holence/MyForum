from django.urls import path

from .views import comment_post_view, comment_reply_view, comment_delete_view, comment_vote_view

app_name="comments"

urlpatterns = [
    path('post/', comment_post_view, name="post"),
    path('reply/', comment_reply_view, name="reply"),
    path('<int:id>/delete/', comment_delete_view, name="delete"),
    path('<int:id>/vote/', comment_vote_view, name="vote"),
]
