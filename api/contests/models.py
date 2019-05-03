from django.db import models
from django.utils.timezone import now


# Create your models here.
class Problem(models.Model):
    """
    contest_tag そのコンテストの問題のtag
    problem_name 問題の名前
    time_limit 時間制限 (sec)
    memory_limit メモリ制限 (MB)
    problem 問題の本文
    _input 入力
    output 出力
    example_input_output 入出力例
    """
    contest_tag = models.CharField(max_length=15)
    problem_name = models.CharField(max_length=20)
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField(default=256)
    problem = models.TextField()
    input = models.TextField()
    output = models.TextField()
    example_input_output = models.TextField()
    answer = models.BinaryField()
    foriegn_key = models.ForeignKey(Contest, on_delete=models.CASCADE)


class Contest(models.Model):
    """
    is_open コンテストを表示するかしないか
    is_active 現在開催中のコンテストか
    title コンテストのタイトル
    tag コンテストのタグ
    start_date コンテストの開始時刻
    contest_time コンテスト時間
    start_time コンテストの開始時間
    writer 問題のwriter
    top_page トップページ
    """
    is_open = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=30, unique=True)
    tag = models.CharField(max_length=15)
    start_date = models.DateField(default=now)
    start_time = models.TimeField()
    contest_time = models.IntegerField()
    writer = models.CharField(max_length=30)
    top_page = models.TextField()
