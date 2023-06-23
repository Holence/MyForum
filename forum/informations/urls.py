from django.urls import path

from .views import informations_view

app_name="informations"

urlpatterns = [
    path('', informations_view, name="base"),
]
