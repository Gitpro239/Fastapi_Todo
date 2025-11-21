import requests
import uuid

ENDPOINT = "http://127.0.0.1:8000"

def test_can_call_endpoint():
    response = requests.get(ENDPOINT+ "/list-tasks")
    assert response.status_code == 200

def test_can_list_tasks():
    n = 2
    for _ in range(n):
        payload = new_task_payload()
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    
    list_tasks_response = list_tasks("task_id")
    assert list_tasks_response.status_code == 200

    data = list_tasks_response.json()
    assert isinstance(data, list)
    assert len(data) >= n
    print(data)

def create_task(payload):
    return requests.post(ENDPOINT + "/create-task", json=payload)

def list_tasks(task_id):
    return requests.get(ENDPOINT + "/list-tasks")

def new_task_payload():
    title = f"test_task_{uuid.uuid4().hex}"
    description = f"test_description_{uuid.uuid4().hex}"
    
    print(f"creating task {title} with description{description}")

    return {
        "title": title,
        "description": description,
        "completed": False,
    }