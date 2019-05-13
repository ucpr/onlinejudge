from django.urls import path
from rest_framework import routers

from .views import AuthRegister

urlpatterns = [
    path('register/', AuthRegister.as_view()),
]
