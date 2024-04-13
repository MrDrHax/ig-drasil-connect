"""
This module contains the tests for the actions endpoints in the FastAPI app.
"""
from fastapi.testclient import TestClient
#Import the FastAPI app from the main module
from api.main import app


# Create a test client using the FastAPI app
client = TestClient(app)


#test the start-call endpoint
#Precondition: The phone number must be valid and not empty
#Dependencies: The start-call endpoint must be implemented
#Expected Result: The test should fail if the phone number is invalid
def test_start_call_3000():
    response = client.post("/actions/start-call?phone_number=zzz")
    assert response.status_code == 200

    
#test the end-call endpoint
def test_end_call():
    response = client.post("/actions/end-call?call_id=1234567890")
    assert response.status_code == 200
    assert response.json() == {"message": "Call Ended: 1234567890"}


#test the create-contact endpoint
def test_create_contact():
    # TODO Fix endpoint to use json instead of query parameters
    # Make a contact with a 10 digit phone number
    response = client.post("/actions/create-contact?contact_name=John Doe&phone_number=1234567890")
    assert response.status_code == 200


#test the get-call-details endpoint 
#Precondition: The call ID must be valid and not empty
#Postcondition: The call details must be returned
def test_get_call_details_3001():
    response = client.get("/actions/calls-details/123456789")
    assert response.status_code == 200
    assert response.json() == {
        "call_id": "1234567890",
        "name": "Jane Doe",
        "number": "5521457834",
        "call_subject": "product information"
    }
    
    
#test the agent-availability endpoint
def test_agent_availability_3002():
    response = client.get("/actions/agent-availability")
    assert response.status_code == 200
    assert response.json() == [
        {"agent_id": "123", "availability": "Available"},
        {"agent_id": "456", "availability": "Unavailable"},
        {"agent_id": "789", "availability": "Available"},
    ]
    # Check if the list contains agents with availability status
    assert len(response.json()) < 0