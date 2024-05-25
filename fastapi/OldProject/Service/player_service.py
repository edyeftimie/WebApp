from Repository.repository import PlayersRepository
from fastapi import HTTPException
from Domain.player import PlayerBase, PlayerModel

class PlayersService:
    def __init__(self):
        self.repo = PlayersRepository()
        self.repo.set_initial_values()
        # for i in range(20):
        #     player = self.repo.generate_fake_players()
        #     player['id'] = int
        #     self.create_player(player)
    
    def if_player_exists(self, player: PlayerBase):
        for pl in self.repo.players:
            if pl['name'] == player['name']:
                return True
        return False
    
    def if_player_exists_id(self, player_id: int):
        for pl in self.repo.players:
            if pl['id'] == player_id:
                return True
        return False
    
    def if_list_empty(self):
        if len(self.repo.players) == 0:
            return True
        return False
    
    def create_player(self, player: PlayerBase):
        # for pl in list_of_players:
        player['id'] = self.repo.generate_id()
        # player['id'] = PlayersRepository.generate_id()
        self.repo.players.append(player)
        # list_of_players.append(player)
        return player
    
    def get_players(self):
        return self.repo.players
        # return Service.players
    
    def get_player(self, player_id: int):
        for player in self.repo.players:
            if player['id'] == player_id:
                return player
        return PlayerBase()
    
    def delete_player(self, player_id: int):
        for player in self.repo.players:
            if player['id'] == player_id:
                delete_player = self.repo.players.pop(self.repo.players.index(player))
                return delete_player
        return PlayerBase()
    
    def edit_player(self, player_id: int, player: PlayerBase):
        for i in range(len(self.repo.players)):
            if self.repo.players[i]['id'] == player_id:
                self.repo.players[i]['name'] = player.name
                self.repo.players[i]['age'] = player.age
                self.repo.players[i]['club'] = player.club
                return self.repo.players[i]
        return PlayerBase()
    
    def create_fake_players(self):
        for i in range (10):
            player = self.repo.generate_fake_players()
            player['id'] = self.repo.generate_id()
            self.repo.players.append(player)
        

            