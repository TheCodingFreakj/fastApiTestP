import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Valid payload test
def test_list_view_success():
    payload = {"batchid": "id0101", "payload": [[1, 2], [3, 4]]}

    response = client.post('/items', json=payload)
    mockedResponse = {
    "batchid": "010101",
    "response": [
        3,
        7
    ],
    "status": "complete",
    "started_at": "2024-05-31T18:17:18.091231",
    "end_at": "2024-05-31T18:17:18.945897"
   }

    assert response.status_code == 200
    assert response.json()["response"]== [3,7]

# Invalid payload test
def test_list_view_invalid_payload():
    payload = {"batchid": "id0101", "payload": "invalid_payload"}

    response = client.post('/items', json=payload)

    assert response.status_code == 422
    assert "Input should be a valid list" in response.json()["detail"][0]["msg"]

# Empty payload test
def test_list_action_empty_payload():
    payload = {"batchid": "id0101", "payload": []}

    response = client.post('/items', json=payload)

    assert response.status_code == 200
    assert response.json()["response"]== []

# Invalid payload format test
def test_list_action_invalid_payload_format():
    payload = {"batchid": "id0101", "invalid_payload_key": [[1, 2], [3, 4]]}

    response = client.post('/items', json=payload)

    assert response.status_code == 422
    assert  response.json()["detail"][0]["msg"] == "Field required"