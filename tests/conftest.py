# first run application server then test
import requests

ENDPOINT = "http://127.0.0.1:8000"

response = requests.get(ENDPOINT + "/api")

data = response.json()
print(data)

status_code = response.status_code
print(status_code)

def test_can_call_endpoint():
    response = requests.get(ENDPOINT + "/api")
    assert response.status_code == 200
