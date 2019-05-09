# rabbitMQからのメッセージを解釈して指定のcode_runnerコンテナを走らせる
import docker
import json
import os
import sys
import shutil
import tarfile
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
    COMMAND = "python /runner/main.py"
    DIRECTORY_PATH = "./"

    def __init__(self, submit_data: SubmitData):
        self.submit_data = submit_data
        self.container_name = 'code_runner_' + self.submit_data.language
        self.directory_name = 'judge_' + self.submit_data.id

    def make_judge_directory(self):
        os.mkdir(self.DIRECTORY_PATH + self.directory_name)
        with open("{}/code.{}".format(
                self.DIRECTORY_PATH + self.directory_name,
                FILENAME_EXTENTIONS[self.submit_data.language]
                ), 'w') as f:
            f.write(self.submit_data.source_code)
        # TODO: テストケースを用意する
        # fetch_problem_tests()
        shutil.copyfile(
            './testcases.tar.gz',
            self.DIRECTORY_PATH + self.directory_name + '/testcases.tar.gz'
            )

    def fetch_problem_testcases(self):
        # テストケースとかは何かで圧縮してDBのBinaryFieldってとこにいれることにしたので
        # DBはpostgreSQL bytea型
        # contest_tag, problem_tagでfilterしてとる
        pass

    def update_submit_status(self):
        # submit_idはユニークなものだからUPDATEでいい
        pass

    def run_container(self):
        # TODO: Network Block
        output = self.client.containers.run(
            self.container_name,
            command=self.COMMAND,
            volumes={
                os.getcwd() + '/' + self.directory_name + '/': {
                    'bind': '/problem',
                    'mode': 'rw'
                }
            }
        )
        print(json.loads(output))

if __name__ == '__main__':
    # data = {
    #     "submit_id": "some_submit_id",
    #     "contest_tag": "some_contest_tag",
    #     "problem_tag": "some_problem_tag",
    #     "source_code": "print('some_source_code')",
    #     "language": "python"
    # }
    data = SubmitData(
        "123456",
        "some_problem_tag",
        "print('some_source_code')",
        "mitohato",
        "python"
    )
    client = DockerClient(data)
    # client.make_judge_directory()
    client.run_container()
