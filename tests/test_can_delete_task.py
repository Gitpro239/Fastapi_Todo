import requests

ENDPOINT = "http://127.0.0.1:8000"

def test_can_delete_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["id"]

    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404
    print(get_task_response.json())

def create_task(payload):
    return requests.post(ENDPOINT + "/create-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")

def new_task_payload():
    return {
        "title": "my test content",
        "description": "test description",
        "completed": False,
    }