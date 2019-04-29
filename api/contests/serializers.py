from .models import Contest
from .models import Problem
from rest_framework import serializers


class ProblemSerializer(serializers.ModelSerializer):
    contest_tag = serializers.CharField(required=True)
    problem_path = serializers.CharField(required=True)
    answer_path = serializers.CharField(required=True)

    class Meta(object):
        model = Problem
        fields = (
            'contest_tag',
            'problem_path',
            'answer_path',
        )


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
#    is_open = serializers.BooleanField(required=True)
#    is_active = serializers.BooleanField(required=True)
#    title = serializers.CharField(required=True)
#    tag = serializers.CharField(required=True)
#    start_date = serializers.DateField(required=True)
#    contest_time = serializers.IntegerField(required=True)
#    writer = serializers.CharField(required=True)
#
#    class Meta(object):
#        model = Contest
#        fields = (
#            'is_open',
#            'is_active',
#            'title',
#            'tag',
#            'start_date',
#            'contest_time',
#            'writer',
#        )
#
