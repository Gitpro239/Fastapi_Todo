import requests

ENDPOINT = "http://127.0.0.1:8000"

def test_can_update_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    task_id = create_task_response.json()["id"]
    new_payload = {
        "title": "my updated content",
        "completed": True,
    }
    update_task_response = update_task(task_id, new_payload)
    assert update_task_response.status_code == 200
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["title"] == new_payload["title"]
    assert get_task_data["completed"] == new_payload["completed"]


def create_task(payload):
    return requests.post(ENDPOINT + "/create-task", json=payload)

def update_task(task_id, payload):
    return requests.put(ENDPOINT + f"/update-task/{task_id}", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def new_task_payload():
    return {
        "title": "my test content",
        "description": "test description",
        "completed": False,
    }