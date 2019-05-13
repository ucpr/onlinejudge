import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy.dialects.postgresql import BYTEA



Base = sqlalchemy.ext.declarative.declarative_base()

class Problem(Base):
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
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    contest_tag = sqlalchemy.Column(sqlalchemy.String(15))
    problem_name = sqlalchemy.Column(sqlalchemy.String(20))
    problem_tag = sqlalchemy.Column(sqlalchemy.String(15))
    score = sqlalchemy.Column(sqlalchemy.Integer)
    problem_order = sqlalchemy.Column(sqlalchemy.Integer)
    time_limit = sqlalchemy.Column(sqlalchemy.Integer)
    memory_limit = sqlalchemy.Column(sqlalchemy.Integer)
    problem = sqlalchemy.Column(sqlalchemy.Text)
    input = sqlalchemy.Column(sqlalchemy.Text)
    output = sqlalchemy.Column(sqlalchemy.Text)
    example_input_output = sqlalchemy.Column(sqlalchemy.Text)
    answer = sqlalchemy.Column(BYTEA)
    __tablename__ = "contests_problem"

    def __init__(self):
        super(Base, self).__init__()
        self.memory_limit = 256
