from django.urls import path

from .views import comment_delete_view, comment_vote_view

app_name="comments"

urlpatterns = [
    path('<int:id>/delete/', comment_delete_view, name="delete"),
    path('<int:id>/vote/', comment_vote_view, name="vote")
]
