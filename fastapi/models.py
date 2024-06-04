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