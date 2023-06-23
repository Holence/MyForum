from django.urls import path

from .views import accounts_detail_view, accounts_edit_view, change_password_view, accounts_follow_view, accounts_infopage_view

app_name="accounts"

urlpatterns = [
    path('edit/', accounts_edit_view, name="edit"),
    path('password/', change_password_view, name="password"),
    path('infopage/', accounts_infopage_view, name="infopage"),
    path('follow/<str:username>/', accounts_follow_view, name="follow"),
    path('profile/<str:username>/', accounts_detail_view, name="detail"),
]
