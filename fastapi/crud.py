from sqlalchemy.orm import Session

import models, schemas

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def get_team_by_name(db: Session, team_name: str):
    return db.query(models.Team).filter(models.Team.name == team_name).first()

def get_teams(db: Session, skip: int = 0, limit: int = 100, current_user: schemas.UserBase = None):
    if current_user is None:
        return db.query(models.Team).offset(skip).limit(limit).all()
    else:
        username = current_user["sub"]
        user_id = get_user_id_by_username(db, username)
        return db.query(models.Team).filter(models.Team.created_by == user_id).offset(skip).limit(limit).all()

def create_team(db: Session, team: schemas.TeamCreate, current_user: schemas.UserBase):
    user_id = get_user_id_by_username(db, current_user["sub"])
    db_team = models.Team(name=team.name, country=team.country, number_of_trophies=team.number_of_trophies, created_by=user_id)
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

def get_players(db: Session, skip: int = 0, limit: int = 100, current_user: schemas.UserBase = None):
    if current_user is None:
        return db.query(models.Player).offset(skip).limit(limit).all()
    else:
        # print (f"current_user: {current_user}")
        username = current_user["sub"]
        # print (f"username: {username}")
        user_id = get_user_id_by_username(db, username)
        return db.query(models.Player).filter(models.Player.created_by == user_id).offset(skip).limit(limit).all()

def create_player(db: Session, player: schemas.PlayerCreate, team_id: int, current_user: schemas.UserBase):
    user_id = get_user_id_by_username(db, current_user["sub"])
    db_player = models.Player(name=player.name, age=player.age, team_id=team_id, created_by=user_id)
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

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "cheie_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 #min

def create_user(db: Session, user: schemas.UserBase):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return "completed"

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

from datetime import datetime, timedelta, timezone
import jwt

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    # expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"decoded payload: {payload}")
        # username: str = payload.get("sub")
        # if username is None:
        #     return None
        return payload
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        print(f"token: {token}")
        return None
    
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_id_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user.id

def get_username_from_token(token: str):
    payload = verify_token(token)
    return payload.get("sub")
