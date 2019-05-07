from django.urls import path
from rest_framework import routers

from .views import (
    ContestsView,
    ContestView,
    ProblemsView,
    ProblemView,
    SubmitView,
    RegistContestView,
    SubmittionsView,
    StandingsView
)


urlpatterns = [
    path('contests/', ContestsView.as_view()),
    path('contests/<str:contest_tag>/', ContestView.as_view()),
    path('contests/<str:contest_tag>/problems/', ProblemsView.as_view()),
    path('contests/<str:contest_tag>/problems/<str:problem_tag>/', ProblemView.as_view()),
    path('contests/<str:contest_tag>/submit/', SubmitView.as_view()),
    path('contests/<str:contest_tag>/register/', RegistContestView.as_view()),
    path('contests/<str:contest_tag>/submittions/', SubmittionsView.as_view()),
    path('contests/<str:contest_tag>/standings/', StandingsView.as_view()),
]
