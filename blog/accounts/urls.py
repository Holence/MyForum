from django.urls import path

from .views import accounts_detail_view, accounts_edit_view, change_password_view

app_name="accounts"

urlpatterns = [
    path('edit/', accounts_edit_view, name="edit"),
    path('password/', change_password_view, name="password"),
    path('profile/<str:username>/', accounts_detail_view, name="detail"),
]
