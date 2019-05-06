# rabbitMQからのメッセージを解釈して指定のcode_runnerコンテナを走らせる
import docker
import json
import os
import sys
from judge_result import JudgeResult
from SubmitData import SubmitData


# 暫定
LANGUAGES = [
    "c",
    "cpp",
    "java",
    "python"
]

FILENAME_EXTENTIONS = {
    "c": "c",
    "cpp": "cpp",
    "java": "java",
    "python": "py"
}


class DockerClient():
    client = docker.from_env()
    COMMAND = "python3 judge.py"
    DIRECTORY_PATH = "./"

    def __init__(self, submit_data: SubmitData):
        self.submit_data = submit_data
        self.container_name = 'code_runner_' + self.submit_data.language
        self.directory_name = 'judge_' + self.submit_data.submit_id

    def make_judge_directory(self):
        os.mkdir(self.DIRECTORY_PATH + self.directory_name)
        with open("{}/main.{}".format(
                self.DIRECTORY_PATH + self.directory_name,
                FILENAME_EXTENTIONS[self.submit_data.language]
                )) as f:
            f.write(self.submit_data.source_code)
        # TODO: テストケースを用意する
        # テストケースとかは何かで圧縮してDBのBinaryFieldってとこにいれることにしたので
        # DBはpostgreSQL

    def run_container(self, language: str, command: str):
        # TODO: Time Limit
        # TODO: Memory Limit
        # TODO: Network Block
        # TODO: directory mount
        self.client.containers.run(
            self.container_name,
            command=self.COMMAND
        )


# この関数強い 関数名変えたほうがよさそう
def read_message_from_rabbitmq(body: dict):
    data = json.loads(body)
    submit_data = SubmitData(
        data["submission_id"],
        data["contest_tag"],
        data["problem_tag"],
        data["source_code"],
        data["language"]
    )

    if check_language_exists(submit_data.language):
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
