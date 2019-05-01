from .models import Contest
from .models import Problem
from rest_framework import serializers


class ProblemSerializer(serializers.ModelSerializer):
    # contest_tag = serializers.CharField(required=True)

    class Meta:
        model = Problem
        fields = '__all__'


class ContestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contest
        fields = '__all__'


class ContestSerializer(serializers.ModelSerializer):
    """ Contestの詳細 """

    class Meta:
        model = Contest
        fields = '__all__'
