"""
This module contains the tests for the dashboard endpoints in the FastAPI app.
"""
from fastapi.testclient import TestClient
#Import the FastAPI app from the main module
from api.main import app
#Import the models graph and usage graph
from api.apps.dashboard.models import UsageGraph



# Create a test client using the FastAPI app
client = TestClient(app)

# Test the get-usage-graph endpoint
def test_get_usage_graph_3003():
    response = client.get("/dashboard/graph/usage")
    assert response.status_code == 200
    assert len(response.json()["data"]) == len(response.json()["labels"])
    #Check if the data is greater than or equal to 0
    for i in response.json()["data"]:
        assert i >= 0


# Test the get-connection-status-graph endpoint
def test_get_connection_status_graph_3004():
    response = client.get("/dashboard/graph/connection_status")
    assert response.status_code == 200
    # Check if the length of the data is equal to the length of the labels
    assert len(response.json()["data"]) == len(response.json()["labels"])
    #Check if the sum of the data is equal to 100
    assert sum(response.json()["data"]) == 100

# Test the get-lex-users endpoint
def test_get_lex_users():
    response = client.get("/dashboard/data/lex_users")
    assert response.status_code == 200
    assert response.json() == 5

# Test the get-ongoing-call-data endpoint
# Precondition: The call data must be valid and not empty
# Dependencies: The get-ongoing-call-data endpoint must be implemented
# Postcondition: The call data must be returned
def test_get_ongoing_call_data_3005():
    response = client.get("/dashboard/data/calls")
    assert response.status_code == 200
    assert response.json()["costumers"] >= 0
    assert response.json()["agents"] >= 0
    assert response.json()["agents_in_break"] >= 0
    # rating should be between 0 and 5
    assert response.json()["rating"] >= 0 and response.json()["rating"] <= 5

# Test the get-reconnected-calls endpoint
def test_get_reconnected_calls():
    response = client.get("/dashboard/data/reconnected")
    assert response.status_code == 200
    assert response.json() == 5

# Test the get-angry-calls endpoint
def test_get_angry_calls():
    response = client.get("/dashboard/data/angry")
    assert response.status_code == 200
    #Check if the response is an integer greater than or equal to 0
    assert int(response.json()) >= 0 

# Test the data rerouted-calls endpoint
def test_get_rerouted_calls():
    response = client.get("/dashboard/data/rerouted")
    assert response.status_code == 200
    #Check if the response is an integer greater than or equal to 0
    assert int(response.json()) >= 0
