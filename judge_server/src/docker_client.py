# rabbitMQからのメッセージを解釈して指定のcode_runnerコンテナを走らせる
import docker
import json
import os
import sys
from judge_result import JudgeResult
from submit_data import SubmitData


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
