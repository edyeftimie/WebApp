from pydantic import BaseModel

class PlayerBase(BaseModel):
    name: str
    age: int

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    team_id: int

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
    players: list[Player] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    password: str