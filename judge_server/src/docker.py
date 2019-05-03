# rabbitMQからのメッセージを解釈して指定のcode_runnerコンテナを走らせる
import docker
import json
import sys
from judge_server.src.judge_result import JudgeResult


# 暫定
LANGUAGES = [
    "c",
    "cpp",
    "java",
    "python"
]


def read_message_from_rabbitmq(body: dict):
    data = json.loads(body)
    language = select_language(data["language"])

    if language is None:
        return JudgeResult("ERROR", "Cannot run with specified language")

    # TODO: docker走らす系の処理


def select_language(language: str):
    if language not in LANGUAGES:
        sys.stderr.write(
            "[ERROR]: Cannot run with specified language. {}".format(language)
        )
        return None
    else:
        return language
