import requests

ENDPOINT = "http://127.0.0.1:8000"

def test_can_call_endpoint():
    response = requests.post(ENDPOINT + "/create-task", json={"title": "test", "description": "test"})
    assert response.status_code == 200

def test_can_create_task():
    payload = {
        "title": "Fastapi",
        "description": "Learning Fastapi", 
        "completed": False,
    }
    create_task_response = requests.post(ENDPOINT + "/create-task", json=payload)
    assert create_task_response.status_code == 200

    data = create_task_response.json()
    print(data)

    task_id = data["id"]
    get_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")

    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["title"] == payload["title"]
    assert get_task_data["description"] == payload["description"]
    assert get_task_data["completed"] == payload["completed"]

def test_can_create_task_():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    
    data = create_task_response.json()
    print(data)

    task_id = data["id"]
    get_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")
    assert get_task_response.status_code == 200

    get_task_data = get_task_response.json()
    assert get_task_data["title"] == payload["title"]
    assert get_task_data["description"] == payload["description"]
    assert get_task_data["completed"] == payload["completed"]

def create_task(payload):
    return requests.post(ENDPOINT + "/create-task", json=payload)

def new_task_payload():
    return {
        "title": "my test content",
        "description": "test description",
        "completed": False,
    }