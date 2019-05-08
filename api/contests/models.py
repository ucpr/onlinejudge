from django.db import models
from django.utils.timezone import now


# Create your models here.
class Contest(models.Model):
    """
    is_open コンテストを表示するかしないか
    is_active 現在開催中のコンテストか
    is_schedule 予定のコンテストか
    title コンテストのタイトル
    contest_tag コンテストのタグ
    start_date_time コンテストの開始時刻
    end_date_time コンテストの終了時刻
    writer 問題のwriter
    top_page トップページ
    """
    is_open = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_schedule = models.BooleanField(default=True)
    title = models.CharField(max_length=30, unique=True)
    contest_tag = models.CharField(max_length=15)
    start_date_time = models.DateTimeField(default=now)
    end_date_time = models.DateTimeField(default=now)
    writer = models.CharField(max_length=30)
    top_page = models.TextField()

    def contest_time(self):
        t = self.end_date_time - self.start_date_time
        return r.hours

    def __str__(self):
        return self.title + " [" + self.contest_tag + "]"


class Problem(models.Model):
    """
    contest_tag そのコンテストの問題のtag
    problem_name 問題の名前
    problem_tag 問題のタグ
    problem_tag 問題の順番
    problem_order 問題の順番
    time_limit 時間制限 (sec)
    memory_limit メモリ制限 (MB)
    problem 問題の本文
    _input 入力
    output 出力
    example_input_output 入出力例
    """
    contest_tag = models.CharField(max_length=15)
    problem_name = models.CharField(max_length=20)
    problem_tag = models.CharField(max_length=15)
    score = models.IntegerField()
    problem_order = models.IntegerField()
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField(default=256)
    problem = models.TextField()
    input = models.TextField()
    output = models.TextField()
    example_input_output = models.TextField()
    answer = models.BinaryField()
#    foriegn_key = models.ForeignKey(Contest, on_delete=models.CASCADE)

    def __str__(self):
        return "(" + str(self.problem_order) + ") " + self.problem_name + \
                " [" + self.problem_tag + "]" + " from " + self.contest_tag


class Submittion(models.Model):
    """
    problem_tag 問題のタグ
    source_code 提出されたソースコード
    status judgeの結果
    warning コンパイル時のwarning
    error エラー

    author 提出したユーザー
    language 言語
    time 実行時間
    memory メモリ使用量
    byte ソースコードのサイズ
    date 提出した日付
    is_judged ジャッジされたかのフラグ
    """
    contest_tag = models.CharField(max_length=15)
    problem_tag = models.CharField(max_length=15)
    source_code = models.TextField()
    author = models.CharField(max_length=10)
    language = models.CharField(max_length=10)

    status = models.CharField(max_length=5, blank=True)
    warning = models.TextField(blank=True)
    error = models.TextField(blank=True)
    time = models.FloatField(blank=True)
    memory = models.IntegerField(blank=True)
    byte = models.IntegerField(blank=True)
    date = models.DateTimeField(blank=True)
    is_judge = models.BooleanField(default=False, blank=True)
#    foriegn_key = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return self.contest_tag + "." + self.problem_tag + " by " + self.author


class RegistContestUser(models.Model):
    """ コンテストの参加登録
    """
    contest_tag = models.CharField(max_length=15)
    username = models.CharField(max_length=15)

    def __str__(self):
        return "[" + self.contest_tag + "] " + self.username


class Standing(models.Model):
    """ コンテストのランキング

    - problem_hoge_timeはproblem_hoge_scoreがACなら書き換えない
    - ランキングは基本Scoreをみて、同じだったらtime
    - last_ac_timeはACごとに書き換える
    """
    # これはactiveのときで登録してる人が投げた結果をあれする
    contest_tag = models.CharField(max_length=15)
    username = models.CharField(max_length=15)

    problem_a_status = models.CharField(max_length=5)
    problem_a_score = models.CharField(max_length=5)
    problem_a_wrong = models.CharField(max_length=5)
    problem_a_time = models.IntegerField()

    problem_b_status = models.CharField(max_length=5)
    problem_b_score = models.CharField(max_length=5)
    problem_b_wrong = models.CharField(max_length=5)
    problem_b_time = models.IntegerField()

    problem_c_status = models.CharField(max_length=5)
    problem_c_score = models.CharField(max_length=5)
    problem_c_wrong = models.CharField(max_length=5)
    problem_c_time = models.IntegerField()

    problem_d_status = models.CharField(max_length=5)
    problem_d_score = models.CharField(max_length=5)
    problem_d_wrong = models.CharField(max_length=5)
    problem_d_time = models.IntegerField()

    problem_e_status = models.CharField(max_length=5)
    problem_e_score = models.CharField(max_length=5)
    problem_e_wrong = models.CharField(max_length=5)
    problem_e_time = models.IntegerField()

    problem_f_status = models.CharField(max_length=5)
    problem_f_score = models.CharField(max_length=5)
    problem_f_wrong = models.CharField(max_length=5)
    problem_f_time = models.IntegerField()

    scores = models.IntegerField()
    last_ac_time = models.IntegerField()

    def __str__(self):
        return self.contest_tag + " " + self.username

