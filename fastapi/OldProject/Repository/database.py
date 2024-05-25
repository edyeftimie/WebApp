from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# create a database URL fro SQLAlchemy
URL_DB = 'sqlite:///./database.db'
# create an engine
engine = create_engine(URL_DB, connect_args={'check_same_thread': False})
# create a session, not a database session yet
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# create a base class
Base = declarative_base()




