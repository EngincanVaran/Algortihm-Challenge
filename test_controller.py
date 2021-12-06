from fastapi.testclient import TestClient
from controller import app
import json

# to run tests

# pip3 install pytest
# pytest

client = TestClient(app)

CUSTOM_SOLVER_PATH = "/solver"
VROOM_SOLVER_PATH = "/vroom"
DUMMY_INPUT_FILE = "input.json"


def test_custom_solver_no_request_body():
    response = client.post(CUSTOM_SOLVER_PATH, json={})
    assert response.status_code == 422


def test_custom_solver_only_algorithm():
    response = client.post(
        CUSTOM_SOLVER_PATH,
        json={
            'algorithm': 'greedy'
        })
    assert response.status_code == 422


def test_custom_solver_only_datasource():
    response = client.post(
        CUSTOM_SOLVER_PATH,
        json={
            'datasource': DUMMY_INPUT_FILE
        })
    assert response.status_code == 422


def test_custom_solver_invalid_datasource():
    response = client.post(
        CUSTOM_SOLVER_PATH,
        json={
            'datasource': 'input2.json',
            'algorithm': 'greedy'
        })
    assert response.status_code == 400
    assert response.json() == {"detail": "Datasource Not Found"}


def test_custom_solver_invalid_algorithm():
    response = client.post(
        CUSTOM_SOLVER_PATH,
        json={
            'datasource': DUMMY_INPUT_FILE,
            'algorithm': 'greed'
        })
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid Algorithm"}


def test_custom_solver_valid_greedy():
    response = client.post(
        CUSTOM_SOLVER_PATH,
        json={
            'datasource': DUMMY_INPUT_FILE,
            'algorithm': 'greedy'
        })
    assert response.status_code == 200
    assert response.json() != None


def test_custom_solver_valid_brute_force():
    response = client.post(
        CUSTOM_SOLVER_PATH,
        json={
            'datasource': DUMMY_INPUT_FILE,
            'algorithm': 'brute-force'
        })
    assert response.status_code == 200
    assert response.json() != None


def test_vroom_empty_input():
    response = client.post(
        VROOM_SOLVER_PATH,
        json={})
    assert response.status_code == 400


def test_vroom_empty_input():
    response = client.post(
        VROOM_SOLVER_PATH,
        json={})
    assert response.status_code == 400
    assert response.json() != None


def test_vroom_valid_input():
    input_file = open(DUMMY_INPUT_FILE)
    request = json.load(input_file)
    response = client.post(
        VROOM_SOLVER_PATH,
        json=request)
    assert response.status_code == 200
    assert response.json() != None
