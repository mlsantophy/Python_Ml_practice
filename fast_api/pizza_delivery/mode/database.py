from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg2


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/pizza_delivery"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={},future=True
)


Base=declarative_base()

Session=sessionmaker()
