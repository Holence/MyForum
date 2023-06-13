from django.urls import path

from .views import article_detail_view, article_search_view, article_create_view, article_edit_view, article_delete_view, article_vote_view

app_name="articles"

urlpatterns = [
    path('search/', article_search_view, name="search"),
    path('create/', article_create_view, name="create"),
    path('<str:slug>/', article_detail_view, name="detail"),
    path('<str:slug>/edit/', article_edit_view, name="edit"),
    path('<str:slug>/delete/', article_delete_view, name="delete"),
    path('<str:slug>/vote/', article_vote_view, name="vote"),
]
