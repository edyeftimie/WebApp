from sqlalchemy.orm import Session
from Domain.player import PlayerBase, PlayerModel
from Domain.team import TeamBase, TeamModel
from Repository.database import Base

def get_team(db: Session, team_id: int):
    return db.query(TeamModel).filter(TeamModel.id == team_id).first()

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TeamModel).offset(skip).limit(limit).all()

def get_player(db: Session, player_id: int):
    return db.query(PlayerModel).filter(PlayerModel.id == player_id).first()

def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PlayerModel).offset(skip).limit(limit).all()

def create_team(db: Session, team: TeamBase):
    db_team = TeamModel(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def create_player(db: Session, player: PlayerBase):
    db_player = PlayerModel(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def delete_team(db: Session, team_id: int):
    db_team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    db.delete(db_team)
    db.commit()
    return db_team

def delete_player(db: Session, player_id: int):
    db_player = db.query(PlayerModel).filter(PlayerModel.id == player_id).first()
    db.delete(db_player)
    db.commit()
    return db_player

def edit_team(db: Session, team_id: int, team: TeamBase):
    db_team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    db_team.name = team.name
    db_team.country = team.country
    db_team.number_of_trophies = team.number_of_trophies
    db.commit()
    db.refresh(db_team)
    return db_team

def edit_player(db: Session, player_id: int, player: PlayerBase):
    db_player = db.query(PlayerModel).filter(PlayerModel.id == player_id).first()
    db_player.name = player.name
    db_player.age = player.age
    db_player.club = player.club
    db.commit()
    db.refresh(db_player)
    return db_player



