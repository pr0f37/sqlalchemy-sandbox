from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import event
from sqlalchemy import URL

from sqlalchemy_sandbox.config import DBConfig, app_config


def db_connection_string(config: DBConfig):
    return URL.create(
        "postgresql+psycopg",
        username=config.user,
        password=config.password,
        host=config.host,
        port=config.port,
        database=config.db,
    )


def connection_strings():
    return {
        db: db_connection_string(config) for db, config in app_config.DATABASES.items()
    }


sessions = {
    db: sessionmaker(create_engine(conn_string))
    for db, conn_string in connection_strings().items()
}


@event.listens_for(Engine, "connect")
def receive_connect(dbapi_connection, connection_record):
    print("--- [NEW PHYSICAL CONNECTION OPENED] ---")
    print(dbapi_connection)
    print(connection_record)


@event.listens_for(Engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    print("--- [CONNECTION CHECKED OUT FROM POOL] ---")
    print(dbapi_connection)
    print(connection_record)
    print(connection_proxy)
