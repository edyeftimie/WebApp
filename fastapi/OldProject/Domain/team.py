from Repository.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country = Column(String)
    number_of_trophies = Column(String)
    # players = relationship("Player", back_populates="club")
    
class TeamBase(BaseModel):
    name: str
    country: str
    number_of_trophies: str

class TeamModel(TeamBase):
    id : int
    class Config:
        from_attributes = True