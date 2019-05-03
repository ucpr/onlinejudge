from django.urls import path
from rest_framework import routers

from .views import (
    ContestsView,
    ContestView,
    ProblemsView,
    ProblemView,
    SubmitView,
)


urlpatterns = [
    path('contests/', ContestsView.as_view()),
    path('contests/<str:contest_tag>/', ContestView.as_view()),
    path('contests/<str:contest_tag>/problems/', ProblemsView.as_view()),
    path('contests/<str:contest_tag>/problems/<str:problem_tag>/', ProblemView.as_view()),
    path('contests/<str:contest_tag>/submit/', SubmitView.as_view()),
]
