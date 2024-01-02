import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from fileshare.settings import get_db_config


conf = get_db_config()

username = conf.USERNAME
password = conf.PASSWORD
host = conf.HOST
port = conf.PORT
database_name = conf.NAME
encoded_password = urllib.parse.quote(password)


DATABASE_URL: str = f"postgresql+psycopg2://{username}:{encoded_password}@{host}:{port}/{database_name}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()