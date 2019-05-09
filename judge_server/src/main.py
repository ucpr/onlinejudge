from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from receive_mq import RecieveMQ


DB_USER = "daizu"
DB_PASSWORD = "daizuhogehoge"
DB_HOST = "postgres"
DB_NAME = "postgres"

db_engine = create_engine("postgres://{}:{}@{}/{}".format(
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_NAME
    ),
    encoding="utf-8"
)

Session = sessionmaker(bind=db_engine)
db_session = Session()


# rabbitMQからメーセージを受け取ってcode_runnerコンテナで実行
def main():
    mq = RecieveMQ(db_session=db_session)
    mq.start_receiving()


if __name__ == '__main__':
    main()
