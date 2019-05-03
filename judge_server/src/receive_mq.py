import pika


class RecieveMQ():
    # 後で変える
    RABBITMQ_HOST = "localhost"
    QUEUE_NAME = "queue"

    def __init__(self, *, host=RABBITMQ_HOST, queue=QUEUE_NAME, useQuery=None):
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
        self.useQuery = useQuery if useQuery is not None \
            else lambda x: print(x)

    def callback(self, ch, method, properties, body):
        self.useQuery(body)

    def start_receiving(self):
        self.channel.start_consuming()
