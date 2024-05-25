from sqlalchemy.orm import Session

import models, schemas

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def get_team_by_name(db: Session, team_name: str):
    return db.query(models.Team).filter(models.Team.name == team_name).first()

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()

def create_team(db: Session, team: schemas.TeamCreate):
    db_team = models.Team(name=team.name, country=team.country, number_of_trophies=team.number_of_trophies)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team
    
def delete_team(db: Session, team_id: int):
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    db.delete(db_team)
    db.commit()
    return db_team

def edit_team(db: Session, team_id: int, team: schemas.TeamCreate):
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    db_team.name = team.name
    db_team.country = team.country
    db_team.number_of_trophies = team.number_of_trophies
    db.commit()
    db.refresh(db_team)
    return db_team

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()

def get_player_by_name(db: Session, player_name: str):
    return db.query(models.Player).filter(models.Player.name == player_name).first()

def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Player).offset(skip).limit(limit).all()

def create_player(db: Session, player: schemas.PlayerCreate, team_id: int):
    db_player = models.Player(name=player.name, age=player.age, team_id=team_id)
    #db_player = models.Player(**player.dict(), team_id=team_id)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def delete_player(db: Session, player_id: int):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    db.delete(db_player)
    db.commit()
    return db_player

def edit_player(db: Session, player: schemas.PlayerCreate, player_id: int):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    db_player.name = player.name
    db_player.age = player.age
    db.commit()
    db.refresh(db_player)
    return db_player