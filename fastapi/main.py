from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import SessionLocal, engine
from passlib.context import CryptContext
# uvicorn main:app --reload
# python fastapi env
# from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://localhost:3000/players",
    "http://localhost:8000",
    "ws://localhost:8000/ws",
    "ws://localhost:8000/players",
    "ws://localhost:8000/players/ws",
    "ws://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    # allow_methods=["POST", "GET", "DELETE", "PUT", "FETCH", "axios"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: str):
        for connection in self.active_connections:
            await connection.send_text(data)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/players/{team_id}", response_model=schemas.Player)
def create_player(team_id: int, player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_name(db, player_name=player.name)
    if db_player:
        raise HTTPException(status_code=400, detail="Player already exists")
    elif not player.name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    elif not player.age:
        raise HTTPException(status_code=400, detail="Age cannot be empty")
    # elif not player.age.isdigit():
    #     raise HTTPException(status_code=400, detail="Age must be a number")
    elif int(player.age) < 0:
        raise HTTPException(status_code=400, detail="Age must be a positive number")
    elif int(player.age) > 100:
        raise HTTPException(status_code=400, detail="Age must be less than 100")
    return crud.create_player(db=db, player=player, team_id=team_id)

@app.get("/players/", response_model=List[schemas.Player])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    players = crud.get_players(db, skip=skip, limit=limit)
    if not players:
        raise HTTPException(status_code=404, detail="No players found")
    return players

@app.get("/players/{player_id}", response_model=schemas.Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id=player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@app.put("/players/{player_id}", response_model=schemas.Player)
def update_player(player_id: int, player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id=player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud.edit_player(db=db, player=player, player_id=player_id)

@app.delete("/players/{player_id}", response_model=schemas.Player)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id=player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    return crud.delete_player(db=db, player_id=player_id)

@app.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = crud.get_team_by_name(db, team_name=team.name)
    if db_team:
        raise HTTPException(status_code=400, detail="Team already exists")
    elif not team.name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    elif not team.country:
        raise HTTPException(status_code=400, detail="Country cannot be empty")
    elif not team.number_of_trophies:
        team.number_of_trophies = 0
    #     raise HTTPException(status_code=400, detail="Number of trophies cannot be empty")
    # elif not team.number_of_trophies.isdigit():
    #     raise HTTPException(status_code=400, detail="Number of trophies must be a number")
    elif int(team.number_of_trophies) < 0:
        raise HTTPException(status_code=400, detail="Number of trophies must be a positive number")
    return crud.create_team(db=db, team=team)

@app.get("/teams/", response_model=List[schemas.Team])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teams = crud.get_teams(db, skip=skip, limit=limit)
    if not teams:
        raise HTTPException(status_code=404, detail="No teams found")
    return teams

@app.get("/teams/{team_id}", response_model=schemas.Team)
def read_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@app.put("/teams/{team_id}", response_model=schemas.Team)
def update_team(team_id: int, team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return crud.edit_team(db=db, team=team, team_id=team_id)

@app.delete("/teams/{team_id}", response_model=schemas.Team)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id=team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return crud.delete_team(db=db, team_id=team_id)

import asyncio

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(manager.broadcast("Server is up"))


# jwt code here
ouath2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/register")
def register_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) 
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
    
@app.get("/veify_token/{token}")
async def verify_user_token(token: str = Depends(ouath2_scheme)):
    if not crud.verify_token(token = token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"message": "Token is valid"}
    
        




