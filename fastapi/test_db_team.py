import unittest
from fastapi.testclient import TestClient
import main
# pytest -p no:warnings .\test_db_team.py
# powershell
app = TestClient(main.app)

class TestMain(unittest.TestCase):
    def test_create_team(self):
        response = app.post('/teams', json = {
            "name": "U Cluj",
            "country": "Romania",
            "number_of_trophies": 3
        })
        assert response.status_code == 200

        response = app.post('/teams', json = {
            "name": "U Cluj",
            "country": "Romania",
            "number_of_trophies": 3
        })
        assert response.status_code == 400
        assert response.json() == {"detail": "Team already exists"}

        response = app.post('/teams', json = {
            "name": "CFR Cluj",
            "country": "Romania",
            "number_of_trophies": -4
        })
        assert response.status_code == 400
        assert response.json() == {"detail": "Number of trophies must be a positive number"}
    
    def test_edit_team(self):
        response = app.put('/teams/3', json = {
            "name": "U C",
            "country": "Romania",
            "number_of_trophies": 5
        })
        assert response.status_code == 200
        assert response.json() == {
            "name": "U C",
            "country": "Romania",
            "number_of_trophies": 5,
            "id": 3,
            "players": []
        }
        response = app.put('/teams/25', json = {
            "name": "U C",
            "country": "Romania",
            "number_of_trophies": 5
        })
        assert response.status_code == 404
        assert response.json() == {"detail": "Team not found"}
    
    def test_get_team(self):
        response = app.get('/teams/3')
        assert response.status_code == 200
        assert response.json() == {
            "name": "U C",
            "country": "Romania",
            "number_of_trophies": 5,
            "id": 3,
            "players": []
        }
        response = app.get('/teams/25')
        assert response.status_code == 404
        assert response.json() == {"detail": "Team not found"}
        
    
    def test_delete_team(self):
        response = app.delete('/teams/4')
        assert response.status_code == 200
        assert response.json() == {
            "name": "U Cluj",
            "country": "Romania",
            "number_of_trophies": 3,
            "id": 4,
            "players": []
        }
        response = app.delete('/teams/5')
        assert response.status_code == 404
        assert response.json() == {"detail": "Team not found"}

    def test_get_teams(self):
        response = app.get('/teams')
        assert response.status_code == 200
    
    def test_create_player(self):
        response = app.post('/players/?team_id=7', json = {
            "name": "Gigi",
            "age": 30,
        })
        assert response.status_code == 200
        assert response.json() == {
            "name": "Gigi",
            "age": 30,
            "id": 7,
            "team_id": 7
        }

        response = app.post('/players/?team_id=7', json = {
            "name": "Gigi",
            "age": 30,
        })
        assert response.status_code == 400
        assert response.json() == {"detail": "Player already exists"}
    
    def test_edit_player(self):
        response = app.put('/players/2', json = {
            "name": "Gigel",
            "age": 53,
        })
        assert response.status_code == 200
        response = app.put('/players/25', json = {
            "name": "Gigel",
            "age": 53,
        })
        assert response.status_code == 404
        assert response.json() == {"detail": "Player not found"}
    
    def test_delete_player(self):
        response = app.delete('/players/7')
        assert response.status_code == 200
        assert response.json() == {
            "name": "Gigi",
            "age": 30,
            "id": 7,
            "team_id": 7
        }
        response = app.delete('/players/25')
        assert response.status_code == 404
        assert response.json() == {"detail": "Player not found"}
    
    def test_get_player(self):
        response = app.get('/players/2')
        assert response.status_code == 200
        response = app.get('/players/25')
        assert response.status_code == 404
        assert response.json() == {"detail": "Player not found"}