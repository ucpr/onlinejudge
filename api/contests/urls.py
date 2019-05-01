from django.urls import path
from rest_framework import routers

from .views import ContestsView, ContestView, ProblemsView, ProblemView


urlpatterns = [
    path('contests/', ContestsView.as_view()),
    path('contests/<str:contest_tag>/', ContestView.as_view()),
    path('contests/<str:contest_tag>/problems/', ProblemsView.as_view()),
    path('contests/<str:contest_tag>/problems/<int:id>/', ProblemView.as_view()),
]
