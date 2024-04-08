from fastapi.testclient import TestClient
#Import the FastAPI app from the main module
from api.main import app


# Create a test client using the FastAPI app
client = TestClient(app)


#test the start-call endpoint
def test_start_call():
    response = client.post("/actions/start-call?phone_number=1234567890")
    assert response.status_code == 200
    assert response.json() == {"message": "Call Started: 1234567890"}