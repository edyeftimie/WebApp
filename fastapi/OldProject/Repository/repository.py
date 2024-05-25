from Repository.initial_input import players_list, teams_list
from faker import Faker
from faker.providers import BaseProvider

class TeamsRepository:
    def __init__(self):
        self.teams = []
        self.fake = Faker()
        self.fake.add_provider(MyProvider)
        
    def set_initial_values(self):
        self.teams = teams_list
    
    def generate_id(self):
        if len(self.teams) == 0:
            return 1
        return self.teams[-1]['id'] + 1
    
    def generate_fake_teams(self):
        team = {
            'name': self.fake.club().__str__(),
            'country': self.fake.country().__str__(),
            'number_of_trophies': self.fake.random_int(min=0, max=10).__str__()
        }
        return team

class PlayersRepository:
    def __init__(self):
        self.players = []
        self.fake = Faker()
        self.fake.add_provider(MyProvider)
        
    def set_initial_values(self):
        self.players = players_list
    
    def generate_id(self):
        if len(self.players) == 0:
            return 1
        return self.players[-1]['id'] + 1
    
    def generate_fake_players(self):
        player = {
            'name': self.fake.name().__str__(),
            'age': self.fake.random_int(min=18, max=40).__str__(),
            'club': self.fake.club().__str__()
        }
        return player

class MyProvider(BaseProvider):
    def club(self):
        clubs = ['Al Nassr', 'Inter Miami', 'Al Hilal', 'Barcelona', 'Manchester City', 'Real Madrid', 'Liverpool', 'Bayern Munich', 'Chelsea', 'FCSB', 'CFR Cluj',
                 'Dinamo Bucuresti', 'Steaua Bucuresti', 'Rapid Bucuresti', 'Universitatea Craiova', 'FC Botosani', 'FC Voluntari', 'FC Arges', 'FC Hermannstadt', 'Farul Constanta',
                 'Borrusia Dortmund', 'Paris Saint Germain', 'Juventus', 'AC Milan', 'AS Roma', 'Atletico Madrid', 'Sevilla', 'Valencia', 'Villareal', 'Real Sociedad', 'Real Betis',
                 ]
        return self.random_element(clubs)