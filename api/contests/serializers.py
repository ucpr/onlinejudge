from django.utils.timezone import now
from rest_framework import serializers

from .models import Contest
from .models import Problem
from .models import Submittion
from .models import RegistContestUser


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

    class Meta:
        model = Submittion
        fields = '__all__'

    def create(self, validate_data):
        data = validate_data
        data["status"] = "WJ"
        data["warning"] = ""
        data["error"] = ""
        data["time"] = 0
        data["memory"] = 0
        data["byte"] = 0
        data["date"] = now()
        data["is_judge"] = False
        submit = Submittion(**data)
        submit.save()
        return submit


class RegistContestUserSerializer(serializers.ModelSerializer):
    """ 参加登録 """

    class Meta:
        model = RegistContestUser
        fields = '__all__'
