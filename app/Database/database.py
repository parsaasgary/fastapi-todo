from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


import os


from ..config import  CREDENTIALS_EVV_DIR

load_dotenv(dotenv_path= CREDENTIALS_EVV_DIR)
database_url = os.getenv("DATABASE_URL")
test_database_url = os.getenv("DATABASE_TEST_URL")

engine = create_engine(test_database_url 
                       , pool_size= 10 
                       , max_overflow=30)

session = sessionmaker(bind = engine 
                       ,autocommit = False 
                       ,autoflush = False  )

Base = declarative_base()


