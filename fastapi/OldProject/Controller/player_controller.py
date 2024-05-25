from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, APIRouter
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from Repository.database import SessionLocal, engine
from Domain.player import PlayerBase, PlayerModel
from Service.player_service import PlayersService
from Repository.initial_input import players_list
# from Repository.repository import PlayersRepository
#anaconda fastapi
#uvicorn main:cpp -reload

# app = FastAPI()
router = APIRouter()

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


serv = PlayersService()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.post('/players', response_model=PlayerModel)
async def create_player(player: PlayerBase):
    new_player = player.dict()
    if new_player['name'] == '':
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if new_player['age'] == '':
        raise HTTPException(status_code=400, detail="Age cannot be empty")
    if new_player['club'] == '':
        raise HTTPException(status_code=400, detail="Club cannot be empty")
    if not new_player['age'].isdigit():
        raise HTTPException(status_code=400, detail="Age must be a number")
    if int(new_player['age']) < 0:
        raise HTTPException(status_code=400, detail="Age must be a positive number")
    if int(new_player['age']) > 100:
        raise HTTPException(status_code=400, detail="Age must be less than 100")
    if serv.if_player_exists(new_player):
        raise HTTPException(status_code=400, detail="Player already exists")
    return serv.create_player(new_player)

@router.get('/players', response_model = List[PlayerModel])
async def get_players():
    if serv.if_list_empty():
        raise HTTPException(status_code=404, detail="No players found")
    list_of_players = serv.get_players()
    return list_of_players

@router.get('/players/{player_id}', response_model = PlayerModel)
async def get_player(player_id: int):
    if serv.if_list_empty():
        raise HTTPException(status_code=404, detail="No players found")
    if not serv.if_player_exists_id(player_id):
        raise HTTPException(status_code=404, detail="Player not found")
    return serv.get_player(player_id)

@router.delete('/players/{player_id}', response_model = PlayerModel)
async def delete(player_id: int):
    if serv.if_list_empty():
        raise HTTPException(status_code=404, detail="No players found")
    if not serv.if_player_exists_id(player_id):
        raise HTTPException(status_code=404, detail="Player not found")
    return serv.delete_player(player_id)

@router.put('/players/{player_id}', response_model = PlayerBase)
async def edit_player(player_id: int, player: PlayerBase):
    if player.name == '':
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if player.age == '':
        raise HTTPException(status_code=400, detail="Age cannot be empty")
    if player.club == '':
        raise HTTPException(status_code=400, detail="Club cannot be empty")
    if not player.age.isdigit():
        raise HTTPException(status_code=400, detail="Age must be a number")
    if int(player.age) < 0:
        raise HTTPException(status_code=400, detail="Age must be a positive number")
    if int(player.age) > 100:
        raise HTTPException(status_code=400, detail="Age must be less than 100")
    if not serv.if_player_exists_id(player_id):
        raise HTTPException(status_code=404, detail="Player not found")
    return serv.edit_player(player_id, player)

import asyncio

async def add_fake_players():
    while True:
        interval_seconds = 5
        serv.create_fake_players()
        await manager.broadcast("New player added")
        await asyncio.sleep(interval_seconds)

@router.on_event("startup")
async def startup_event():
    print("Starting up")
    # asyncio.create_task(add_fake_players())


# list_of_players = players
# class PlayerBase(BaseModel):
#     name: str
#     age: str
#     club: str

# class PlayerCreate(PlayerBase):
#     id: int
#     class Config:
# 
# def get_db():

#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# db_dependency = Annotated[Session, Depends(get_db)]
# models.Base.metadata.create_all(bind=engine)

# @app.post('/players/', response_model=PlayerCreate)
# async def create_player(player: PlayerBase, db: db_dependency): # type: ignore
#     new_player = models.Player(**player.dict())
#     db.add(new_player)
#     db.commit()
#     db.refresh(new_player)
#     return new_player

# @app.get('/players', response_model = List[PlayerCreate])
# async def get_players(db: db_dependency, skip: int = 0, limit: int = 10): # type: ignore
#     players = db.query(models.Player).offset(skip).limit(limit).all()
#     return players

