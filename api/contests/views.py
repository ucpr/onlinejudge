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
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView

from .serializers import ProblemSerializer, ContestsSerializer, ContestSerializer
from .models import Contest, Problem


class ContestsView(generics.ListAPIView, generics.CreateAPIView):
    """ Contestの一覧を返すView

    # GET
    コンテストの一覧を返します

    # POST (admin)
    コンテストを追加します
    """
    queryset = Contest.objects.all()
    serializer_class = ContestsSerializer


class ContestView(generics.ListAPIView):
    """ Contestの情報を返すview

    # GET
    コンテストの詳細を返します
    """
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer

    def get_queryset(self):
        if 'contest_tag' in self.request.query_params:
            tag = self.request.query_params.get("contest_tag")
        return Contest.objects.filters(tag=tag)


#class AuthRegister(generics.CreateAPIView):
#    permission_classes = (permissions.AllowAny,)
#    queryset = Account.objects.all()
#    serializer_class = AccountSerializer
#
#    @transaction.atomic
#    def post(self, request, format=None):
#        serializer = AccountSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
