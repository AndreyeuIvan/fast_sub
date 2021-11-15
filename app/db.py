#from .config import setting

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


#SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.db_user}@{setting.db_host}:{setting.db_port}/{setting.db_name}'


SQLALCHEMY_DATABASE_URL = f'postgresql://noname@localhost:5432/subeer'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
