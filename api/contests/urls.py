from django.conf.urls import url
from rest_framework import routers

from .views import ContestsView


urlpatterns = [
    url('contests/', ContestsView.as_view()),
]
