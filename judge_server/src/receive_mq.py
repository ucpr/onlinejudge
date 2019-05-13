import pika
import json
import sys
from docker_client import DockerClient
from judge_result import JudgeResult
from submit_data import SubmitData


# 暫定
LANGUAGES = [
    "c",
    "cpp",
    "java",
    "python"
]


class RecieveMQ():
    # 後で変える
    RABBITMQ_HOST = "mq"
    QUEUE_NAME = "judge_queue"

    def __init__(self, *, host=RABBITMQ_HOST, queue=QUEUE_NAME, db_session=None):
        # useQuery(body)でcallback関数でrabbitMQから受け取ったbodyを処理する
        # それはそうとネーミングセンスがない
        self.queue = queue
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.callback,
            auto_ack=True
        )
        
        self.db_session = db_session

    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        submit_data = SubmitData(
            data["id"],
            data["problem_tag"],
            data["source_code"],
            data["author"],
            data["language"]
        )

        if self.check_language_exists(submit_data.language):
            return JudgeResult("WA", "Cannot run with specified language")

        # TODO: docker走らす系の処理
        docker_client = DockerClient(submit_data)
        res = docker_client.fetch_problem_testcases(self.db_session)
        print(res)

    def check_language_exists(self, language: str) -> bool:
        if language not in LANGUAGES:
            sys.stderr.write(
                "[ERROR]: Cannot run with specified language. {}".format(
                    language)
            )
            return False
        else:
            return True

    def start_receiving(self):
        self.channel.start_consuming()
