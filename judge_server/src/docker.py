# rabbitMQからのメッセージを解釈して指定のcode_runnerコンテナを走らせる
import docker
import json
import sys
from judge_result import JudgeResult


# 暫定
LANGUAGES = [
    "c",
    "cpp",
    "java",
    "python"
]


def read_message_from_rabbitmq(body: dict):
    data = json.loads(body)
    language = data["language"]

    if check_language_exists(language):
        return JudgeResult("ERROR", "Cannot run with specified language")

    # TODO: docker走らす系の処理


def check_language_exists(language: str) -> bool:
    if language not in LANGUAGES:
        sys.stderr.write(
            "[ERROR]: Cannot run with specified language. {}".format(language)
        )
        return False
    else:
        return True


def run_container():
    pass
