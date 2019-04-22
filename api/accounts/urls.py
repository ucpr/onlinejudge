from django.conf.urls import include, url
from rest_framework import routers

from .views import AuthRegister

urlpatterns = [
    url('register/$', AuthRegister.as_view()),
]
