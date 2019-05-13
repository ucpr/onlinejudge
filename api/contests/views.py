import json
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core import serializers
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponse, Http404
from django.forms.models import model_to_dict

from rest_framework import authentication, permissions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters import rest_framework as filters

import pika

from .permission import (
        IsRegistedContest,
        IsActiveContest,
        IsScheduleContest,
        IsActive,
    )

from .serializers import (
        ProblemSerializer,
        ContestsSerializer,
        ContestSerializer,
        SubmittionsSerializer,
        RegistContestUserSerializer,
        StandingSerializer,
    )
from .models import Contest, Problem, Submittion, RegistContestUser, Standing


class ContestsView(generics.ListAPIView, generics.CreateAPIView):
    """ Contestの一覧を返すView(is_open=True)

    # GET
    コンテストの一覧を返します
    query_params:
    is_schedule, is_activeでfilter, 指定しない場合は全部

    # POST (admin)
    コンテストを追加します
    """
    queryset = Contest.objects.all()
    serializer_class = ContestsSerializer

    def get_queryset(self):
        querys = self.request.query_params
        if querys.get("is_schedule"):
            obj = Contest.objects.filter(is_open=True, is_schedule=True)
        elif querys.get("is_active"):
            obj = Contest.objects.filter(is_open=True, is_active=True)
        else:
            obj = Contest.objects.filter(is_open=True)
        return obj


class ContestView(generics.ListAPIView):
    """ Contestの情報を返すview

    # GET
    コンテストの詳細を返します
    """
    permission_classes = (IsRegistedContest, )
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
    permission_classes = (IsActiveContest, )
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
    permission_classes = (IsActiveContest, )
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
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsActiveContest, )
    queryset = Submittion.objects.all()
    serializer_class = SubmittionsSerializer

    def perform_create(self, serializer):
        contest_tag = self.request.query_params.get("contest_tag")
        problem_tag = self.request.query_params.get("problem_tag")
        source_code = self.request.query_params.get("source_code")
        author = self.request.query_params.get("author")
        language = self.request.query_params.get("language")
        serializer.save()
        id_ = serializer.data.get("id")
        self.add_job(problem_tag, id_, source_code, author, language)
#        return submit

    def add_job(self, problem_tag, id_, source_code, author, language):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="mq"))
        channel = connection.channel()
        channel.queue_declare(queue='judge_queue')

        body = {
            "problem_tag": problem_tag,
            "id": id_,
            "source_code": source_code,
            "author": author,
            "language": language,
        }
        channel.basic_publish(exchange='',
                              routing_key='judge_queue',
                              body=json.dumps(body))
        connection.close()


class RegistContestView(generics.CreateAPIView):
    """ コンテストに参加登録するためのview
    """
    authentication_classes = (JSONWebTokenAuthentication, )
    queryset = RegistContestUser.objects.all()
    serializer_class = RegistContestUserSerializer


class StandingView(generics.ListAPIView):
    """ コンテストのランキングを返します """
    queryset = Submittion.objects.all()
    serializer_class = SubmittionsSerializer


class SubmittionsView(generics.ListAPIView):
    """ 提出一覧を返します """
    permission_classes = (IsActiveContest, )
    queryset = Submittion.objects.all()
    serializer_class = SubmittionsSerializer

    def get_queryset(self):
        contest_tag = self.kwargs.get("contest_tag")
        if Contest.objects.filter(contest_tag=contest_tag,
                                  is_active=True).exists():
            # is_activeがTrueなら自分のsubmittionしか返さない
            username = self.request.user.username
            return Submittion.objects.filter(contest_tag=contest_tag,
                                             author=username)
        else:
            return Submittion.objects.filter(contest_tag=contest_tag)


class StandingsView(generics.ListAPIView):
    """ コンテストのランキングを返します """
    permission_classes = (IsScheduleContest, )
    queryset = Standing.objects.all()
    serializer_class = StandingSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_fields = ('scores', 'last_ac_time')


class DetailsSubmittionView(generics.ListAPIView):
    """ 提出の詳細を返します """
    permission_classes = (IsActive, )
    queryset = Submittion.objects.all()
    serializer_class = SubmittionsSerializer

    def get_queryset(self):
        id_ = self.kwargs.get("problem_id")
        return Submittion.objects.filter(id=id_)
