from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_weather_view, name="get_weather"),
]
