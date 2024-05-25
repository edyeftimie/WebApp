import unittest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from Controller.team_controller import router
from Repository.initial_input import teams_list
app = router
client = TestClient(app)

class TestMain(unittest.TestCase):
    def test_create_team(self):
        try:
            response = client.post('/teams', json = {
                "name": "U Cluj",
                "country": "Romania",
                "number_of_trophies": "3"
            })
        except HTTPException as e:
            assert False
        else:
            assert response.status_code == 200
            assert response.json() == {
                "name": "U Cluj",
                "country": "Romania",
                "number_of_trophies": "3",
                "id": 11
            }
        try:
            response = client.post('/teams', json = {
                "name": "U Cluj",
                "country": "Romania",
                "number_of_trophies": "3"
            })
        except HTTPException as e:
            assert e.status_code == 400
            assert e.detail == "Team already exists"
    
    def test_get_teams(self):
        response = client.get('/teams')
        assert response.status_code == 200
        assert response.json() == teams_list
    
    def test_get_team(self):
        try:
            response = client.get('/teams/2')
        except HTTPException as e:
            assert False
        else:
            assert response.status_code == 200
            assert response.json() == {
                "name": "Inter Miami",
                "country": "USA",
                "number_of_trophies": "2",
                "id": 2
        }

        try:
            response = client.get('/teams/66')
        except HTTPException as e:
            assert e.status_code == 404
            assert e.detail == "Team not found"
    
    def test_delete_team(self):
        try:
            response = client.delete('/teams/1')
            print (response.json())
        except HTTPException as e:
            assert False
        else:
            assert response.status_code == 200
            assert response.json() == {
                "name": "Al Nassr",
                "country": "Saudi Arabia",
                "number_of_trophies": "5",
                "id": 1
            }
        try:
            response = client.delete('/teams/66')
        except HTTPException as e:
            assert e.status_code == 404
            assert e.detail == "Team not found"
    
    def test_edit_team(self):
        try:
            response = client.put('/teams/3', json = {
                "name": "AlHilal",
                "country": "SaudiArabia",
                "number_of_trophies": "16"
            })
        except HTTPException as e:
            assert False
        else:
            assert response.status_code == 200
            assert response.json() == {
                "name": "AlHilal",
                "country": "SaudiArabia",
                "number_of_trophies": "16",
            }
            