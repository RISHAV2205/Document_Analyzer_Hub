from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL='postgresql://postgres:1234@localhost/FastAPI'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

session_local=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():  #dependency on session
    db=session_local()
    try:
        yield db
    finally:
        db.close()
