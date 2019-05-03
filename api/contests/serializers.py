from .models import Contest
from .models import Problem
from .models import Submittion
from rest_framework import serializers


class ProblemSerializer(serializers.ModelSerializer):

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


class SubmittionsSerializer(serializers.ModelSerializer):
    """ 問題の提出 """

    def create(self, validate_data):
        # TODO: validate_dataから初期で必要ないやつはnullで初期化する
        return Submittion(**validate_data)

    class Meta:
        model = Submittion
        fields = '__all__'
