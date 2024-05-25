import unittest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from Controller.player_controller import router
# import Domain.player as player
from Repository.initial_input import players_list
app = router
client = TestClient(app)
#pytest -p no:warnings .\unit_tests.py 
#python -W ignore::DeprecationWarning -m unittest .\unit_tests.py

class TestMain(unittest.TestCase):
    def test_create_player(self):
        response = client.post('/players', json = {
            "name": "Ronaldo",
            "age": "36",
            "club": "Juventus"
        })
        assert response.status_code == 200
        assert response.json() == {
            "name": "Ronaldo",
            "age": "36",
            "club": "Juventus",
            "id": 12
        }
        try:
            response = client.post('/players', json = {
                "name": "Cristiano Ronaldo",
                "age": "36",
                "club": "Juventus"
            })
        except HTTPException as e:
            assert e.status_code == 400
            assert e.detail == "Player already exists"
        try:
            response = client.post('/players', json = {
                "name": "Ronaldinho",
                "age": "alpha",
                "club": "Legend"
            })
        except HTTPException as e:
            print (e)
            assert e.status_code == 400
            assert e.detail == "Age must be a number"
    
    def test_get_players(self):
        response = client.get('/players')
        assert response.status_code == 200
        assert response.json() == players_list
    
    def test_get_player(self):
        response = client.get('/players/2')
        assert response.status_code == 200
        assert response.json() == {
            "name": "Lionel Messi",
            "age": "36",
            "club": "Inter Miami",
            "id": 2
        }
        try:
            response = client.get('/players/22')
        except HTTPException as e:
            assert e.status_code == 404
            assert e.detail == "Player not found"
    
    def test_delete_player(self):
        response = client.delete('/players/1')
        assert response.status_code == 200
        assert response.json() == {
            "name": "Cristiano Ronaldo",
            "age": "38",
            "club": "Al Nassr",
            "id": 1
        }
        try:
            response = client.delete('/players/22')
        except HTTPException as e:
            assert e.status_code == 404
            assert e.detail == "Player not found"

    def test_edit_player(self):
        response = client.put('/players/3', json = {
            "name" : "Neymar Jr",
            "age": "29",
            "club": "PSG"
        })
        assert response.status_code == 200
        assert response.json() == {
            "name": "Neymar Jr",
            "age": "29",
            "club": "PSG",
            # "id": 3
        }
        try:
            response = client.put('/players/22', json = {
                "name": "Lionel Messi",
                "age": "35",
                "club": "Inter Miami"
            })
        except HTTPException as e:
            assert e.status_code == 404
            assert e.detail == "Player not found"

if __name__ == '__main__':
    unittest.main()