from fastapi import APIRouter, HTTPException
from typing import List
from Domain.team import TeamBase, TeamModel
from Service.team_service import TeamService



router = APIRouter()

serv = TeamService()

@router.post('/teams', response_model=TeamModel)
async def create_team(team: TeamBase):
    new_team = team.dict()
    if new_team['name'] == '':
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if new_team['country'] == '':
        raise HTTPException(status_code=400, detail="Country cannot be empty")
    if new_team['number_of_trophies'] == '':
        raise HTTPException(status_code=400, detail="Number of trophies cannot be empty")
    if not new_team['number_of_trophies'].isdigit():
        raise HTTPException(status_code=400, detail="Number of trophies must be a number")
    if int(new_team['number_of_trophies']) < 0:
        raise HTTPException(status_code=400, detail="Number of trophies must be a positive number")
    if serv.if_team_exists(new_team):
        raise HTTPException(status_code=400, detail="Team already exists")
    return serv.create_team(new_team)

@router.get('/teams', response_model = List[TeamModel])
async def get_teams():
    if serv.if_list_empty():
        raise HTTPException(status_code=404, detail="No teams found")
    list_of_teams = serv.get_teams()
    return list_of_teams

@router.get('/teams/{team_id}', response_model = TeamModel)
async def get_team(team_id: int):
    if serv.if_list_empty():
        raise HTTPException(status_code=404, detail="No teams found")
    if not serv.if_team_exists_id(team_id):
        raise HTTPException(status_code=404, detail="Team not found")
    return serv.get_team(team_id)

@router.delete('/teams/{team_id}', response_model = TeamModel)
async def delete(team_id: int):
    if serv.if_list_empty():
        raise HTTPException(status_code=404, detail="No teams found")
    if not serv.if_team_exists_id(team_id):
        raise HTTPException(status_code=404, detail="Team not found")
    return serv.delete_team(team_id)

@router.put('/teams/{team_id}', response_model = TeamBase)
async def edit_team(team_id: int, team: TeamBase):
    if team.name == '':
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if team.country == '':
        raise HTTPException(status_code=400, detail="Country cannot be empty")
    if team.number_of_trophies == '':
        raise HTTPException(status_code=400, detail="Number of trophies cannot be empty")
    if not team.number_of_trophies.isdigit():
        raise HTTPException(status_code=400, detail="Number of trophies must be a number")
    if int(team.number_of_trophies) < 0:
        raise HTTPException(status_code=400, detail="Number of trophies must be a positive number")
    if not serv.if_team_exists_id(team_id):
        raise HTTPException(status_code=404, detail="Team not found")
    return serv.edit_team(team_id, team)
