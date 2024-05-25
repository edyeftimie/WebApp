from Repository.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(String)
    club = Column(String)
    # club_id = Column(Integer, ForeignKey('teams.id'))
    # club = relationship("Team", back_populates="players")

class PlayerBase(BaseModel):
    name: str
    age: str
    club: str

class PlayerModel(PlayerBase):
    id : int
    class Config:
        from_attributes = True