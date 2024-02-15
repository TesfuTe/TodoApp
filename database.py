from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'  # this is for sqlite

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/TodoApplicationDatabase' # for postgresql

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:@127.0.0.1:3306/todoapplicationdatabase'  # for mysql


# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
#                        'check_same_thread': False})  # this is for sqlite

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # for mysql and for postgresql

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
