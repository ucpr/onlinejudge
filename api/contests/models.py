from django.db import models
from django.utils.timezone import now


# Create your models here.
class Problem(models.Model):
    """
    contest_tag そのコンテストの問題のtag
    problem_path 問題のpath
    answer_path テストケースや回答のpath
    """
    contest_tag = models.CharField(max_length=15)
    problem_path = models.CharField(max_length=50, unique=True)
    answer_path = models.CharField(max_length=50, unique=True)
    pass


class Contest(models.Model):
    """
    is_open コンテストを表示するかしないか
    is_active 現在開催中のコンテストか
    title コンテストのタイトル
    tag コンテストのタグ
    start_date コンテストの開始時刻
    contest_time コンテスト時間
    writer 問題のwriter
    top_page トップページ
    """
    is_open = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=30, unique=True)
    tag = models.CharField(max_length=15)
    start_date = models.DateField(default=now)
    contest_time = models.IntegerField()
    writer = models.CharField(max_length=30)
    top_page = models.CharField(max_length=100)
