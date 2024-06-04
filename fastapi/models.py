from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(250), unique=True, index=True)
    hashed_password = Column(String(250))

    players = relationship("Player", back_populates="user")
    teams = relationship("Team", back_populates="user")

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, index=True)
    age = Column(Integer)
    team_id = Column(Integer, ForeignKey("teams.id"))
    created_by = Column(Integer, ForeignKey("users.id"))

    team = relationship("Team", back_populates="players")
    user = relationship("User", back_populates="players")

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, index=True)
    country = Column(String(250))
    number_of_trophies = Column(Integer)
    created_by = Column(Integer, ForeignKey("users.id"))

    players = relationship("Player", back_populates="team")
    user = relationship("User", back_populates="teams")

# slqlite migration to mysql

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import engine

mysql_engine = create_engine('mysql+pymysql://root:admin@localhost:3306/sqldb', echo=True)

SessionLocalMySQL = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

SQLite_Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
sqlite_session = SQLite_Session()

MySQL_Session = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)
mysql_session = MySQL_Session()


Base.metadata.create_all(bind=mysql_engine)

tables = [User, Player, Team]
for table in tables:
    records = sqlite_session.query(table).all()
    for record in records:
        mysql_session.merge(record)

mysql_session.commit()

sqlite_session.close()
mysql_session.close()
    
