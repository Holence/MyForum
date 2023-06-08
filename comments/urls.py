from django.urls import path

from .views import comment_delete_view

app_name="comments"

urlpatterns = [
    path('<int:id>/delete/', comment_delete_view, name="delete"),
]
