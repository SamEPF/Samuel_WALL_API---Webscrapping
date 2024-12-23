import pytest
from fastapi.testclient import TestClient
from src.api.routes.data import router

@pytest.fixture
def client() -> TestClient:
    from main import get_application
    app = get_application()
    app.include_router(router)
    return TestClient(app)

# Test if the repsonse is 200 and dosn't validate the test if there is an error in the response.

class TestDataRoutes:
    def test_download_csv(self, client):
        response = client.get("/data/download-dataset")
        assert response.status_code == 200
        json_response = response.json()
        assert "message" in json_response or "error" in json_response
        if "error" in json_response:
            pytest.fail(f"Error in response: {json_response['error']}")

    def test_load_dataset(self, client):
        response = client.get("/data/load-dataset")
        assert response.status_code == 200
        json_response = response.json()
        assert "data" in json_response or "error" in json_response
        if "error" in json_response:
            pytest.fail(f"Error in response: {json_response['error']}")

    def test_process_dataset(self, client):
        response = client.get("/data/process-dataset")
        assert response.status_code == 200
        json_response = response.json()
        assert "processed_data" in json_response or "error" in json_response
        if "error" in json_response:
            pytest.fail(f"Error in response: {json_response['error']}")

    def test_split_dataset(self, client):
        response = client.get("/data/split-dataset")
        assert response.status_code == 200
        json_response = response.json()
        assert "train" in json_response or "error" in json_response
        assert "test" in json_response or "error" in json_response
        if "error" in json_response:
            pytest.fail(f"Error in response: {json_response['error']}")

    def test_train_model(self, client):
        response = client.get("/data/train-model")
        assert response.status_code == 200
        json_response = response.json()
        assert "message" in json_response or "error" in json_response
        if "error" in json_response:
            pytest.fail(f"Error in response: {json_response['error']}")

    def test_predict(self, client):
        response = client.post("/data/predict", json={"data": [[5.1, 3.5, 1.4, 0.2]]})
        assert response.status_code == 200
        json_response = response.json()
        assert "predictions" in json_response or "error" in json_response
        if "error" in json_response:
            pytest.fail(f"Error in response: {json_response['error']}")

    def test_predict_test_data(self, client):
        response = client.get("/data/predict-test-data")
        assert response.status_code == 200
        json_response = response.json()
        assert "predictions" in json_response or "error" in json_response
        if "error" in json_response:
            pytest.fail(f"Error in response: {json_response['error']}")