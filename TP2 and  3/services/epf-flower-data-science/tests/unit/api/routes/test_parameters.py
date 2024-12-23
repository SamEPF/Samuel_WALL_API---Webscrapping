import pytest
from fastapi.testclient import TestClient
from src.api.routes.parameters import router

@pytest.fixture
def client() -> TestClient:
    from main import get_application
    app = get_application()
    app.include_router(router)
    return TestClient(app)

# Test if the repsonse is 200 and dosn't validate the test if there is an error in the response.

class TestParametersRoutes:
    def test_create_firestore_collection(self, client):
        response = client.get("/parameters/create-firestore-collection")
        assert response.status_code == 200
        json_response = response.json()
        assert "message" in json_response or "error" in json_response
        if "error" in json_response:
            pytest.fail(f"Error in response: {json_response['error']}")

    def test_retrieve_parameters(self, client):
        response = client.get("/parameters/retrieve-parameters")
        assert response.status_code == 200
        json_response = response.json()
        assert "parameters" in json_response or "error" in json_response
        if "error" in json_response:
            pytest.fail(f"Error in response: {json_response['error']}")

    def test_update_parameters(self, client):
        response = client.post("/parameters/update-parameters", json={"n_estimators": 200, "criterion": "entropy"})
        assert response.status_code == 200
        json_response = response.json()
        assert "message" in json_response or "error" in json_response
        if "error" in json_response:
            pytest.fail(f"Error in response: {json_response['error']}")