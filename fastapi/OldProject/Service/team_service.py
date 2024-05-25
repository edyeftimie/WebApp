from Repository.repository import TeamsRepository
from fastapi import HTTPException
from Domain.team import TeamBase, TeamModel

class TeamService:
    def __init__(self):
        self.repo = TeamsRepository()
        self.repo.set_initial_values()
        # for i in range(20):
        #     team = self.repo.generate_fake_teams()
        #     team['id'] = int
        #     self.create_team(team)
    
    def if_team_exists(self, team: TeamBase):
        for tm in self.repo.teams:
            if tm['name'] == team['name']:
                return True
        return False
    
    def if_team_exists_id(self, team_id: int):
        for tm in self.repo.teams:
            if tm['id'] == team_id:
                return True
        return False
    
    def if_list_empty(self):
        if len(self.repo.teams) == 0:
            return True
        return False
    
    def create_team(self, team: TeamBase):
        team['id'] = self.repo.generate_id()
        self.repo.teams.append(team)
        return team
    
    def get_teams(self):
        return self.repo.teams
    
    def get_team(self, team_id: int):
        for team in self.repo.teams:
            if team['id'] == team_id:
                return team
        return TeamBase()
    
    def delete_team(self, team_id: int):
        for team in self.repo.teams:
            if team['id'] == team_id:
                delete_team = self.repo.teams.pop(self.repo.teams.index(team))
                return delete_team
        return TeamBase()
    
    def edit_team(self, team_id: int, team: TeamBase):
        for i in range(len(self.repo.teams)):
            if self.repo.teams[i]['id'] == team_id:
                self.repo.teams[i]['name'] = team.name
                self.repo.teams[i]['country'] = team.country
                self.repo.teams[i]['number_of_trophies'] = team.number_of_trophies
                return self.repo.teams[i]
        return TeamBase()