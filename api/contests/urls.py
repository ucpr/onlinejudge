from django.conf.urls import url
from rest_framework import routers

from .views import ContestsView, ContestView


urlpatterns = [
    url('contests/', ContestsView.as_view()),
    url('contests/<str:contest_tag>', ContestView.as_view()),
]
