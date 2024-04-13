"""
This module contains the tests for the extras endpoints in the FastAPI app.
"""

from fastapi.testclient import TestClient
#Import the FastAPI app from the main module
from api.main import app

# Create a test client using the FastAPI app
client = TestClient(app)

# Test the route-call endpoint
# Precondition: The call ID and agent ID must be valid and not empty
# Dependencies: The route-call endpoint must be implemented
# Input: 123, 456
def test_route_call_3006():
    response = client.post("/extras/route/123/456")
    assert response.status_code == 200
    assert response.json() == "failure"


# Test the get-agentID endpoint
def test_get_agentID():
    response = client.get("/extras/agentID")
    assert response.status_code == 200
    assert response.json() == "1"

# Test the get-IAM endpoint
def test_get_IAM():
    response = client.get("/extras/IAM?deviceID=123456")
    assert response.status_code == 200
    assert response.json() == "example.com/IAM"


# Test the get-IAM-callback endpoint
def test_get_IAM_callback():
    response = client.get("/extras/IAM/callback")
    assert response.status_code == 200
    assert response.json() == {
        "token": "example_token",
        "refresh": "example_refresh",
        "deviceID": "example_deviceID"
    }

# Test the get-IAM-refresh with invalid values
def test_get_IAM_refresh():
    response = client.get("/extras/IAM/refresh?refresh=123&deviceID=example_deviceID")
    assert response.status_code/100 != 2


# Test the get-AI-summary endpoint
def test_get_AI_summary_3007():
    response = client.get("/extras/AI/summary/abc")
    assert response.status_code == 200


# Test the get-AI-transcript endpoint
def test_get_AI_transcript():
    response = client.get("/extras/AI/transcript/123")
    assert response.status_code == 200
    assert response.json() == "This is a test transcript of the call."

# Test the AI-sentiment endpoint
def test_get_AI_sentiment():
    response = client.get("/extras/AI/sentiment/123")
    assert response.status_code == 200
    assert response.json() == "This is a test sentiment of the call."

# Test the lex QA endpoint who recieve a string list
def test_get_lex():
    response = client.get("/extras/lex/QA")
    assert response.status_code == 200
    assert response.json() == ["How did the call go?", "Was the agent helpful?", "Would you like to leave a comment?"]
    # Check if the response is a list of strings
    assert isinstance(response.json(), list)
    for i in response.json():
        assert isinstance(i, str)
    # Check if the response list is not empty value
    assert len(response.json()) > 0 

  
# Test the lex QA endpoint who recieve a string list
def test_post_lex_3008():
    payload = {
        "answers": ["Answer 1", "Answer 2", "Answer 3"],
        "questions": ["Question 1", 12345, "Question 3"]
    }
    response = client.post("/extras/lex/QA", json=payload)
    assert response.status_code == 200