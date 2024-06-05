from pydantic import BaseModel
from typing import List

class PlayerBase(BaseModel):
    name: str
    age: int

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    team_id: int
    created_by: int

    class Config:
        orm_mode = True

class TeamBase(BaseModel):
    name: str
    country: str
    number_of_trophies: int

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    players: List[Player] = []
    created_by: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    players: List[Player] = []
    teams: List[Team] = []

    class Config:
        orm_mode = True
