import sys
from judge_server.src.receive_mq import RecieveMQ


# rabbitMQからメーセージを受け取ってcode_runnerコンテナで実行
def main():
    mq = RecieveMQ()
    mq.start_receiving()


if __name__ == '__main__':
    main()
