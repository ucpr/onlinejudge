from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core import serializers
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, Http404

from rest_framework import authentication, permissions, generics
from rest_framework_jwt.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView

from .serializers import (
        ProblemSerializer,
        ContestsSerializer,
        ContestSerializer,
        SubmittionsSerializer,
        RegistContestUserSerializer,
    )
from .models import Contest, Problem, Submittion, RegistContestUser


class ContestsView(generics.ListAPIView, generics.CreateAPIView):
    """ Contestの一覧を返すView(is_open=True)

    # GET
    コンテストの一覧を返します

    # POST (admin)
    コンテストを追加します
    """
    queryset = Contest.objects.all()
    serializer_class = ContestsSerializer

    def get_queryset(self):
        obj = Contest.objects.filter(is_open=True)
        return obj


class ContestView(generics.ListAPIView):
    """ Contestの情報を返すview

    # GET
    コンテストの詳細を返します
    """
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    lookup_url_kwarg = "contest_tag"

    def get_queryset(self):
        if 'contest_tag' in self.kwargs:
            tag = self.kwargs.get("contest_tag")
            return Contest.objects.filter(contest_tag=tag, is_open=True)


class ProblemsView(generics.ListAPIView, generics.CreateAPIView):
    """ Contestの問題の情報を返すview

    if is_active and is_open:
        if 参加登録:
            200 OK
        else:
            PermissionError
    if is_open and not is_active: 誰でも見れる状態
        200 OK

    # GET
    コンテストの問題の情報を返します (制約など)
    """
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    def get_queryset(self):
        if 'contest_tag' in self.kwargs:
            tag = self.kwargs.get("contest_tag")
            return Problem.objects.filter(contest_tag=tag)


class ProblemView(generics.ListAPIView):
    """ 問題の詳細を返すview

    required: is_active and 参加登録 is True

    # GET
    問題の詳細を返す
    """
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    lookup_url_kwarg = ['problem_tag', 'contest_tag']

    def get_queryset(self):
        if 'contest_tag' in self.kwargs and 'problem_tag' in self.kwargs:
            contest_tag = self.kwargs.get("contest_tag")
            problem_tag = self.kwargs.get("problem_tag")
            return Problem.objects.filter(contest_tag=contest_tag, problem_tag=problem_tag)


class SubmitView(generics.CreateAPIView):
    """ 回答提出用のView

    # POST
    回答を提出する

    require:
        problem_tag
        source_code
        author
        language
    """
    queryset = Submittion.objects.all()
    serializer_class = SubmittionsSerializer


class RegistContestView(generics.CreateAPIView):
    """ コンテストに参加登録するためのview
    """
    queryset = RegistContestUser.objects.all()
    serializer_class = RegistContestUserSerializer
