from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import Controller.player_controller as player_controller
import Controller.team_controller as team_controller

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "ws://localhost:8000/ws",
    "ws://localhost:8000/players",
    "ws://localhost:8000/players/ws",
    "ws://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET", "DELETE", "PUT", "FETCH", "axios"],
    allow_headers=["*"],
)

app.include_router(player_controller.router)
app.include_router(team_controller.router)
# app.include_router(player_controller.router)

@app.get('/')
async def read_root():
    return {"Hello": "World"}
