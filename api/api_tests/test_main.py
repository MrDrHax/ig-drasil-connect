from fastapi.testclient import TestClient
#Import the FastAPI app from the main module
from api.main import app


# Create a test client using the FastAPI app
client = TestClient(app)

#test the root endpoint
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World  >_<"}


